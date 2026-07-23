#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Assemble batch-15.tsv col 4 (single novella row) from _nov15_out/s01..s08.json.
Each slice file is a JSON array of Chinese paragraph strings. They are concatenated
in order and joined with [PARAGRAPH]. Cols 1-3 preserved byte-for-byte.
Run: python3 _assemble15.py            # verify
     python3 _assemble15.py --write    # write (backs up)
"""
import sys, os, json, csv, shutil

BASE = os.path.dirname(os.path.abspath(__file__))
SRC  = os.path.join(BASE, "batch-15.tsv")
OUTDIR = os.path.join(BASE, "_nov15_out")
INDIR  = os.path.join(BASE, "_nov15_in")
SLICES = [f"s{i:02d}" for i in range(1, 9)]
WRITE = "--write" in sys.argv

# expected per-slice paragraph counts (from input files)
expected = {}
for s in SLICES:
    d = json.load(open(os.path.join(INDIR, s + ".json"), encoding="utf-8"))
    expected[s] = len(d["paras"])

all_paras = []
for s in SLICES:
    p = os.path.join(OUTDIR, s + ".json")
    if not os.path.exists(p):
        sys.exit("MISSING output: " + p)
    arr = json.load(open(p, encoding="utf-8"))
    if not isinstance(arr, list):
        sys.exit(f"{s}.json is not a JSON array")
    if len(arr) != expected[s]:
        sys.exit(f"{s}.json count {len(arr)} != expected {expected[s]}")
    for j, el in enumerate(arr):
        if not isinstance(el, str):
            sys.exit(f"{s}.json[{j}] not a string")
        if "\n" in el or "\r" in el or "\t" in el:
            sys.exit(f"{s}.json[{j}] contains real newline/CR/tab")
        if "[PARAGRAPH]" in el:
            sys.exit(f"{s}.json[{j}] contains a stray [PARAGRAPH] marker")
        if "&#x" in el:
            sys.exit(f"{s}.json[{j}] contains &#x entity")
    all_paras.extend(arr)

# read source
raw = open(SRC, encoding="utf-8", newline="").read()
assert "\r" not in raw, "source has CR"
lines = raw.split("\n"); trailing = ""
if lines and lines[-1] == "":
    lines = lines[:-1]; trailing = "\n"
assert len(lines) == 2, f"expected header+1 row, got {len(lines)}"
header = lines[0]
cols = lines[1].split("\t")
assert len(cols) == 4, f"data row has {len(cols)} cols"
fp, key, en, old = cols

# source paragraph count sanity
src_paras = en.count("[PARAGRAPH]") + 1
print(f"source paragraphs: {src_paras}")
print(f"translated paragraphs: {len(all_paras)}")
if len(all_paras) != src_paras:
    sys.exit(f"PARAGRAPH COUNT MISMATCH: src {src_paras} vs cn {len(all_paras)}")

cn = "[PARAGRAPH]".join(all_paras)
print(f"cn [PARAGRAPH] count: {cn.count('[PARAGRAPH]')} (expect {src_paras-1})")
assert cn.count("[PARAGRAPH]") == src_paras - 1
assert "\n" not in cn and "\t" not in cn and "\r" not in cn, "real whitespace leaked into joined cn"
assert "&#x" not in cn

if WRITE:
    bak = SRC + ".bak-assemble"
    shutil.copy2(SRC, bak)
    out = header + "\n" + "\t".join([fp, key, en, cn]) + trailing
    open(SRC, "w", encoding="utf-8", newline="").write(out)
    print(f"WROTE {SRC} (backup {bak})")
    # verify cols1-3 unchanged
    new_cols = open(SRC, encoding="utf-8").read().split("\n")[1].split("\t")
    assert new_cols[:3] == [fp, key, en], "cols1-3 changed!"
    print("cols1-3 verified byte-identical")
else:
    print("(verify-only; pass --write to apply)")
