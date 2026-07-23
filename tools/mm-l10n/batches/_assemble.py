#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Assemble batch-02.tsv column 4 from _frag/*.out.tsv (key<TAB>chinese).
Columns 1-3 preserved byte-for-byte; only column 4 written.
Validates row count, column count, placeholder & bracket-marker parity."""
import sys, re, os

BASE = os.path.dirname(os.path.abspath(__file__))
SRC  = os.path.join(BASE, "batch-02.tsv")
FRAGS = ["r01","r02","r03","r04","r05","r06"]

# --- load translations ---
zh = {}
dups = []
for f in FRAGS:
    p = os.path.join(BASE, "_frag", f + ".out.tsv")
    if not os.path.exists(p):
        sys.exit("MISSING output: " + p)
    with open(p, "r", encoding="utf-8") as fh:
        for ln, line in enumerate(fh, 1):
            line = line.rstrip("\n")
            if line == "":
                continue
            parts = line.split("\t")
            if len(parts) != 2:
                sys.exit(f"{f}.out.tsv line {ln}: expected 2 cols, got {len(parts)}: {line[:80]!r}")
            k, v = parts
            if "\t" in v or "\n" in v:
                sys.exit(f"{f}.out.tsv line {ln}: translation contains real TAB/newline")
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
# keep trailing newline behaviour: raw ended with \n -> last element ''
trailing = ""
if lines and lines[-1] == "":
    lines = lines[:-1]
    trailing = "\n"

out_lines = []
header = lines[0]
out_lines.append(header)
missing = []
PLACE = re.compile(r"%[sSdDfF][0-9]")           # numbered value placeholders
BRACK = re.compile(r"\[[^\]]*\]")                 # any bracket marker
LINK  = re.compile(r"\[LINK=|\[\\LINK\]")
problems = []
for i, line in enumerate(lines[1:], start=2):
    cols = line.split("\t")
    if len(cols) != 4:
        sys.exit(f"source line {i}: expected 4 cols got {len(cols)}")
    fpath, key, en, _old = cols
    if key not in zh:
        missing.append((i, key));
        cn = ""
    else:
        cn = zh[key]
    # ---- validation: placeholder multiset (case-sensitive) must match ----
    en_ph = sorted(PLACE.findall(en))
    cn_ph = sorted(PLACE.findall(cn))
    if cn and en_ph != cn_ph:
        problems.append(f"L{i} {key}: placeholder mismatch EN={en_ph} CN={cn_ph}")
    # ---- validation: LINK count must match exactly ----
    if cn and len(LINK.findall(en)) != len(LINK.findall(cn)):
        problems.append(f"L{i} {key}: LINK marker count mismatch EN={LINK.findall(en)} CN={LINK.findall(cn)}")
    out_lines.append("\t".join([fpath, key, en, cn]))

result = "\n".join(out_lines) + trailing

# --- report before writing ---
print(f"rows in source (excl header): {len(lines)-1}")
print(f"translations loaded: {len(zh)}")
print(f"missing keys: {len(missing)}")
for i,k in missing[:30]:
    print("  MISSING L%d %s" % (i,k))
print(f"validation problems: {len(problems)}")
for p in problems[:50]:
    print("  " + p)

if "--write" in sys.argv:
    if missing:
        sys.exit("REFUSING to write: missing keys present")
    with open(SRC, "w", encoding="utf-8", newline="") as fh:
        fh.write(result)
    print("WROTE", SRC)
else:
    print("(dry run; pass --write to apply)")
