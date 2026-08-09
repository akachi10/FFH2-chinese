from __future__ import annotations

import argparse
import ctypes
import json
import os
import re
import struct
import time
from collections import Counter
from ctypes import wintypes
from datetime import datetime
from pathlib import Path


PROCESS_QUERY_INFORMATION = 0x0400
PROCESS_VM_READ = 0x0010
PROCESS_VM_WRITE = 0x0020
PROCESS_VM_OPERATION = 0x0008
MEM_COMMIT = 0x1000
PAGE_NOACCESS = 0x01
PAGE_GUARD = 0x100
MAX_ADDRESS = 0x80000000
CHUNK_SIZE = 4 * 1024 * 1024
OBJECT_SIZE = 0x200

HEADER_RE = re.compile(
    r"FFH2_SAVE_DIAG_BEGIN timestamp=(\S+) turn=(-?\d+) "
    r"numUnitInfos=(\d+) mapWidth=(\d+) mapHeight=(\d+)"
)
UNIT_RE = re.compile(
    r"FFH2_SAVE_DIAG_UNIT owner=(-?\d+) id=(-?\d+) "
    r"type=(-?\d+) x=(-?\d+) y=(-?\d+)"
)


class MEMORY_BASIC_INFORMATION(ctypes.Structure):
    _fields_ = [
        ("BaseAddress", ctypes.c_void_p),
        ("AllocationBase", ctypes.c_void_p),
        ("AllocationProtect", wintypes.DWORD),
        ("PartitionId", wintypes.WORD),
        ("RegionSize", ctypes.c_size_t),
        ("State", wintypes.DWORD),
        ("Protect", wintypes.DWORD),
        ("Type", wintypes.DWORD),
    ]


def expand_path(value: str, base: Path | None = None) -> Path:
    path = Path(os.path.expandvars(value)).expanduser()
    if not path.is_absolute() and base is not None:
        path = base / path
    return path.resolve()


def load_config(path: Path) -> dict:
    if not path.is_file():
        raise RuntimeError(f"Configuration file not found: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def find_latest_log(log_directory: Path) -> Path:
    logs = [
        path
        for path in log_directory.glob("save-load-*.log")
        if path.is_file()
    ]
    if not logs:
        raise RuntimeError(f"No save-load diagnostic log in {log_directory}")
    return max(logs, key=lambda path: path.stat().st_mtime)


def u32(data: bytes, offset: int) -> int:
    return struct.unpack_from("<I", data, offset)[0]


def s32(data: bytes, offset: int) -> int:
    return struct.unpack_from("<i", data, offset)[0]


def parse_unit(data: bytes, start: int) -> dict[str, int]:
    return {
        "vtable": u32(data, start),
        "id": s32(data, start + 0x0C),
        "x": s32(data, start + 0x18),
        "y": s32(data, start + 0x1C),
        "owner": s32(data, start + 0x1E4),
        "unit_type": s32(data, start + 0x1EC),
        "unit_info_pointer": u32(data, start + 0x1F4),
    }


def iter_memory_chunks(kernel32, process):
    address = 0
    while address < MAX_ADDRESS:
        mbi = MEMORY_BASIC_INFORMATION()
        result = kernel32.VirtualQueryEx(
            process,
            ctypes.c_void_p(address),
            ctypes.byref(mbi),
            ctypes.sizeof(mbi),
        )
        if not result:
            address += 0x1000
            continue
        base = int(mbi.BaseAddress or 0)
        size = int(mbi.RegionSize)
        next_address = base + max(size, 0x1000)
        readable = (
            mbi.State == MEM_COMMIT
            and not (mbi.Protect & PAGE_NOACCESS)
            and not (mbi.Protect & PAGE_GUARD)
        )
        if readable:
            offset = 0
            while offset < size:
                request = min(CHUNK_SIZE, size - offset)
                buffer = ctypes.create_string_buffer(request)
                bytes_read = ctypes.c_size_t()
                ok = kernel32.ReadProcessMemory(
                    process,
                    ctypes.c_void_p(base + offset),
                    buffer,
                    request,
                    ctypes.byref(bytes_read),
                )
                if ok and bytes_read.value:
                    yield base + offset, buffer.raw[: bytes_read.value]
                offset += request
        address = next_address


def configure_kernel32():
    kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
    kernel32.OpenProcess.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD]
    kernel32.OpenProcess.restype = wintypes.HANDLE
    kernel32.VirtualQueryEx.argtypes = [
        wintypes.HANDLE,
        ctypes.c_void_p,
        ctypes.POINTER(MEMORY_BASIC_INFORMATION),
        ctypes.c_size_t,
    ]
    kernel32.VirtualQueryEx.restype = ctypes.c_size_t
    kernel32.ReadProcessMemory.argtypes = [
        wintypes.HANDLE,
        ctypes.c_void_p,
        ctypes.c_void_p,
        ctypes.c_size_t,
        ctypes.POINTER(ctypes.c_size_t),
    ]
    kernel32.ReadProcessMemory.restype = wintypes.BOOL
    kernel32.WriteProcessMemory.argtypes = [
        wintypes.HANDLE,
        ctypes.c_void_p,
        ctypes.c_void_p,
        ctypes.c_size_t,
        ctypes.POINTER(ctypes.c_size_t),
    ]
    kernel32.WriteProcessMemory.restype = wintypes.BOOL
    kernel32.CloseHandle.argtypes = [wintypes.HANDLE]
    kernel32.CloseHandle.restype = wintypes.BOOL
    return kernel32


def main() -> int:
    default_config = Path(__file__).with_name("config.json")
    parser = argparse.ArgumentParser(
        description=(
            "Locate malformed CvUnit objects in a running 32-bit Civ4 process. "
            "Read-only unless --repair-type, --repair-owner and --repair-id are "
            "all supplied."
        )
    )
    parser.add_argument("--pid", required=True, type=int)
    parser.add_argument("--config", type=Path, default=default_config)
    parser.add_argument("--log", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--num-unit-infos", type=int)
    parser.add_argument("--repair-type", type=int)
    parser.add_argument("--repair-owner", type=int)
    parser.add_argument("--repair-id", type=int)
    args = parser.parse_args()

    repair_selectors = (args.repair_type, args.repair_owner, args.repair_id)
    if any(value is not None for value in repair_selectors) and not all(
        value is not None for value in repair_selectors
    ):
        parser.error(
            "--repair-type, --repair-owner and --repair-id must be supplied together"
        )

    config_path = args.config.resolve()
    config = load_config(config_path)
    config_base = config_path.parent
    log_directory = expand_path(config["log_directory"], config_base)
    report_directory = expand_path(config["report_directory"], config_base)
    log_path = args.log.resolve() if args.log else find_latest_log(log_directory)
    mode = "repair" if args.repair_type is not None else "scan"
    if args.output:
        output_path = args.output.resolve()
    else:
        stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        output_path = report_directory / (
            f"unit-memory-{mode}-{stamp}-pid-{args.pid}.json"
        )

    log_text = log_path.read_text(encoding="utf-8", errors="replace")
    marker = log_text.rfind("FFH2_SAVE_DIAG_BEGIN")
    if marker < 0:
        raise RuntimeError("No FFH2_SAVE_DIAG_BEGIN marker in current log")
    current_log = log_text[marker:]
    header_match = HEADER_RE.search(current_log)
    if not header_match:
        raise RuntimeError("Diagnostic header is missing required map metadata")
    header = {
        "timestamp": header_match.group(1),
        "turn": int(header_match.group(2)),
        "num_unit_infos": int(header_match.group(3)),
        "map_width": int(header_match.group(4)),
        "map_height": int(header_match.group(5)),
    }
    num_unit_infos = (
        args.num_unit_infos
        if args.num_unit_infos is not None
        else header["num_unit_infos"]
    )
    if num_unit_infos < 1:
        num_unit_infos = int(config["num_unit_infos_fallback"])
    max_players = int(config.get("max_players", 51))

    records = [
        {
            "owner": int(match.group(1)),
            "id": int(match.group(2)),
            "unit_type": int(match.group(3)),
            "x": int(match.group(4)),
            "y": int(match.group(5)),
        }
        for match in UNIT_RE.finditer(current_log)
    ]
    if not records:
        raise RuntimeError("No unit records in current diagnostic block")
    print(f"PARSED log={log_path} records={len(records)}", flush=True)

    kernel32 = configure_kernel32()
    process_access = PROCESS_QUERY_INFORMATION | PROCESS_VM_READ
    if args.repair_type is not None:
        process_access |= PROCESS_VM_WRITE | PROCESS_VM_OPERATION
    process = kernel32.OpenProcess(process_access, False, args.pid)
    if not process:
        raise ctypes.WinError(ctypes.get_last_error(), "OpenProcess")

    started = time.monotonic()
    try:
        sample_records = records[:40]
        learned: list[dict[str, int]] = []
        learning_chunks = 0
        learning_bytes = 0
        for chunk_address, data in iter_memory_chunks(kernel32, process):
            learning_chunks += 1
            learning_bytes += len(data)
            for record in sample_records:
                needle = struct.pack("<i", record["id"])
                pos = data.find(needle)
                while pos >= 0:
                    start = pos - 0x0C
                    if start >= 0 and start + OBJECT_SIZE <= len(data):
                        candidate = parse_unit(data, start)
                        if all(
                            candidate[key] == record[key]
                            for key in ("id", "x", "y", "owner", "unit_type")
                        ):
                            candidate["address"] = chunk_address + start
                            learned.append(candidate)
                    pos = data.find(needle, pos + 1)
            if len(learned) >= 12:
                break

        if not learned:
            raise RuntimeError(
                "Could not find logged CvUnit objects in process memory; "
                f"chunks={learning_chunks} bytes={learning_bytes}"
            )
        vtable_counts = Counter(item["vtable"] for item in learned)
        unit_vtable, vtable_hits = vtable_counts.most_common(1)[0]
        print(
            f"LEARNED vtable=0x{unit_vtable:08x} hits={vtable_hits} "
            f"examples={len(learned)}",
            flush=True,
        )

        logged_tuples = {
            (
                item["owner"],
                item["id"],
                item["unit_type"],
                item["x"],
                item["y"],
            )
            for item in records
        }
        vtable_needle = struct.pack("<I", unit_vtable)
        candidates: list[dict[str, int | bool | str]] = []
        seen_addresses: set[int] = set()
        for chunk_address, data in iter_memory_chunks(kernel32, process):
            pos = data.find(vtable_needle)
            while pos >= 0:
                if pos + OBJECT_SIZE <= len(data):
                    candidate = parse_unit(data, pos)
                    plausible = (
                        -1 <= candidate["owner"] < max_players
                        and -4096 <= candidate["unit_type"] < num_unit_infos + 4096
                        and -1 <= candidate["x"] < header["map_width"]
                        and -1 <= candidate["y"] < header["map_height"]
                        and -1 <= candidate["id"] < 100_000_000
                    )
                    address = chunk_address + pos
                    if plausible and address not in seen_addresses:
                        seen_addresses.add(address)
                        unit_tuple = (
                            candidate["owner"],
                            candidate["id"],
                            candidate["unit_type"],
                            candidate["x"],
                            candidate["y"],
                        )
                        candidate["address"] = f"0x{address:08x}"
                        candidate["logged"] = unit_tuple in logged_tuples
                        candidates.append(candidate)
                pos = data.find(vtable_needle, pos + 4)

        suspect_candidates = [
            item
            for item in candidates
            if item["unit_info_pointer"] == 0
            or item["unit_type"] < 0
            or item["unit_type"] >= num_unit_infos
        ]
        print(
            f"SCANNED candidates={len(candidates)} "
            f"suspect={len(suspect_candidates)}",
            flush=True,
        )

        repair_actions = []
        if args.repair_type is not None:
            repair_targets = [
                item
                for item in suspect_candidates
                if item["owner"] == args.repair_owner
                and item["id"] == args.repair_id
            ]
            if len(repair_targets) != 1:
                raise RuntimeError(
                    "Repair requires exactly one suspect matching "
                    f"owner={args.repair_owner} id={args.repair_id}; "
                    f"found {len(repair_targets)}"
                )
            donor = next(
                (
                    item
                    for item in candidates
                    if item["unit_type"] == args.repair_type
                    and item["unit_info_pointer"] != 0
                ),
                None,
            )
            if donor is None:
                raise RuntimeError(
                    f"No live donor CvUnit found for type {args.repair_type}"
                )
            donor_info_pointer = int(donor["unit_info_pointer"])
            item = repair_targets[0]
            address = int(str(item["address"]), 16)
            writes = [
                (address + 0x1EC, struct.pack("<i", args.repair_type), "unit_type"),
                (
                    address + 0x1F4,
                    struct.pack("<I", donor_info_pointer),
                    "unit_info_pointer",
                ),
            ]
            for write_address, raw_value, field_name in writes:
                value_buffer = ctypes.create_string_buffer(raw_value)
                bytes_written = ctypes.c_size_t()
                ok = kernel32.WriteProcessMemory(
                    process,
                    ctypes.c_void_p(write_address),
                    value_buffer,
                    len(raw_value),
                    ctypes.byref(bytes_written),
                )
                if not ok or bytes_written.value != len(raw_value):
                    raise ctypes.WinError(
                        ctypes.get_last_error(),
                        f"WriteProcessMemory {field_name}",
                    )
            action = {
                "address": item["address"],
                "owner": item["owner"],
                "id": item["id"],
                "old_unit_type": item["unit_type"],
                "new_unit_type": args.repair_type,
                "old_unit_info_pointer": item["unit_info_pointer"],
                "new_unit_info_pointer": donor_info_pointer,
                "donor_address": donor["address"],
            }
            repair_actions.append(action)
            print(
                f"REPAIRED owner={item['owner']} id={item['id']} "
                f"address={item['address']} type={args.repair_type} "
                f"info=0x{donor_info_pointer:08x}",
                flush=True,
            )

        suspect_addresses = [
            int(str(item["address"]), 16) for item in suspect_candidates[:64]
        ]
        reference_locations: dict[int, list[str]] = {
            address: [] for address in suspect_addresses
        }
        if suspect_addresses:
            needles = {
                address: struct.pack("<I", address)
                for address in suspect_addresses
            }
            for chunk_address, data in iter_memory_chunks(kernel32, process):
                for address, needle in needles.items():
                    if len(reference_locations[address]) >= 64:
                        continue
                    pos = data.find(needle)
                    while pos >= 0 and len(reference_locations[address]) < 64:
                        reference_locations[address].append(
                            f"0x{chunk_address + pos:08x}"
                        )
                        pos = data.find(needle, pos + 1)
            for item in suspect_candidates:
                address = int(str(item["address"]), 16)
                refs = reference_locations.get(address, [])
                item["reference_count_capped"] = len(refs)
                item["reference_locations"] = refs

        payload = {
            "pid": args.pid,
            "mode": mode,
            "source_log": str(log_path),
            "elapsed_seconds": round(time.monotonic() - started, 3),
            "header": header,
            "log_unit_count": len(records),
            "num_unit_infos": num_unit_infos,
            "unit_vtable": f"0x{unit_vtable:08x}",
            "learned_examples": learned,
            "candidate_count": len(candidates),
            "suspect_count": len(suspect_candidates),
            "suspect_candidates": suspect_candidates,
            "repair_actions": repair_actions,
        }
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        print(f"WROTE {output_path}", flush=True)
    finally:
        kernel32.CloseHandle(process)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
