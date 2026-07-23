#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Assemble batch-07.tsv column 4 from _frag07/s*.out.tsv (key<TAB>chinese).
Columns 1-3 preserved byte-for-byte; only column 4 written.
Validates row count, column count, placeholder & bracket-marker parity.
Run:  python3 _assemble07.py            # verify only, prints report
      python3 _assemble07.py --write    # write batch-07.tsv (backs up first)
"""
import sys, re, os, shutil, collections

BASE = os.path.dirname(os.path.abspath(__file__))
SRC  = os.path.join(BASE, "batch-07.tsv")
FRAGDIR = os.path.join(BASE, "_frag07")
FRAGS = [f"s{i:02d}" for i in range(1, 9)]

WRITE = "--write" in sys.argv

# --- load translations ---
zh = {}
dups = []
for f in FRAGS:
    p = os.path.join(FRAGDIR, f + ".out.tsv")
    if not os.path.exists(p):
        pb = os.path.join(FRAGDIR, f + "b.out.tsv")
        if os.path.exists(pb):
            p = pb
        else:
            sys.exit("MISSING output: " + p + " (and no " + f + "b.out.tsv)")
    with open(p, "r", encoding="utf-8") as fh:
        for ln, line in enumerate(fh, 1):
            line = line.rstrip("\n")
            if line == "":
                continue
            parts = line.split("\t")
            if len(parts) != 2:
                sys.exit(f"{f}.out.tsv line {ln}: expected 2 cols, got {len(parts)}: {line[:80]!r}")
            k, v = parts
            if "\t" in v or "\r" in v:
                sys.exit(f"{f}.out.tsv line {ln}: translation contains real TAB/CR")
            if k in zh:
                dups.append(k)
            zh[k] = v
if dups:
    sys.exit("DUP keys across fragments: " + ", ".join(dups[:20]))

# --- read source ---
with open(SRC, "r", encoding="utf-8", newline="") as fh:
    raw = fh.read()
assert "\r" not in raw, "source has CR"
lines = raw.split("\n")
trailing = ""
if lines and lines[-1] == "":
    lines = lines[:-1]
    trailing = "\n"

PLACE = re.compile(r"%[sSdDfF][0-9]")            # numbered value placeholders (case-sensitive multiset)
BRACK = re.compile(r"\[[^\]]*\]")                 # any bracket marker
LINK  = re.compile(r"\[LINK=|\[\\+LINK\]")   # open, and close with one-or-more backslashes

def ms(pat, s):
    return collections.Counter(pat.findall(s))

out_lines = [lines[0]]
missing = []
problems = []
for i, line in enumerate(lines[1:], start=2):
    cols = line.split("\t")
    if len(cols) != 4:
        sys.exit(f"source line {i}: expected 4 cols got {len(cols)}")
    fpath, key, en, _old = cols
    if key not in zh:
        missing.append((i, key))
        out_lines.append(line)  # keep empty col4
        continue
    cn = zh[key]
    # placeholder parity (FAIL)
    if ms(PLACE, en) != ms(PLACE, cn):
        problems.append(("PLACEHOLDER", i, key, ms(PLACE, en), ms(PLACE, cn)))
    # LINK parity (FAIL)
    if len(LINK.findall(en)) != len(LINK.findall(cn)):
        problems.append(("LINK", i, key, LINK.findall(en), LINK.findall(cn)))
    # bracket marker multiset (WARN only, per validator v2)
    eb, cb = ms(BRACK, en), ms(BRACK, cn)
    if eb != cb:
        problems.append(("BRACKET-WARN", i, key, eb, cb))
    out_lines.append("\t".join([fpath, key, en, cn]))

print(f"translations loaded: {len(zh)}")
print(f"source data rows: {len(lines)-1}")
print(f"missing (empty col4): {len(missing)}")
for i, k in missing[:40]:
    print("   MISS", i, k)
fails = [p for p in problems if p[0] != "BRACKET-WARN"]
warns = [p for p in problems if p[0] == "BRACKET-WARN"]
print(f"FAIL problems (placeholder/LINK): {len(fails)}")
for p in fails[:60]:
    print("   FAIL", p[0], "line", p[1], p[2], "en=", dict(p[3]) if isinstance(p[3], collections.Counter) else p[3], "cn=", dict(p[4]) if isinstance(p[4], collections.Counter) else p[4])
print(f"BRACKET WARN (informational): {len(warns)}")
for p in warns[:60]:
    d_en = dict(p[3]); d_cn = dict(p[4])
    diff_en = {k: v for k, v in d_en.items() if d_cn.get(k, 0) != v}
    diff_cn = {k: v for k, v in d_cn.items() if d_en.get(k, 0) != v}
    print("   WARN line", p[1], p[2], "en-only/diff=", diff_en, "cn-only/diff=", diff_cn)

if WRITE:
    if fails:
        sys.exit("REFUSING to write: FAIL problems present")
    if missing:
        sys.exit("REFUSING to write: missing translations present")
    bak = SRC + ".bak-assemble"
    shutil.copy2(SRC, bak)
    with open(SRC, "w", encoding="utf-8", newline="") as fh:
        fh.write("\n".join(out_lines) + trailing)
    print(f"WROTE {SRC} (backup {bak})")
else:
    print("(verify-only; pass --write to apply)")
