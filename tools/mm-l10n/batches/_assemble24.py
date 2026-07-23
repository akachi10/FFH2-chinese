#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Assemble batch-24.tsv col 4 from _b24_out/s*.out.tsv (key<TAB>chinese).
Cols 1-3 byte-for-byte. Parity: placeholders (case-sensitive), LINK open/close,
all bracket markers, source HTML entities (&#NNN;). No &#x-style leak, no real ws.
Run: python3 _assemble24.py [--write]
"""
import sys, os, re, glob, csv, shutil, collections

BASE = os.path.dirname(os.path.abspath(__file__))
SRC  = os.path.join(BASE, "batch-24.tsv")
OUTDIR = os.path.join(BASE, "_b24_out")
WRITE = "--write" in sys.argv

zh = {}; dups = []
for p in sorted(glob.glob(os.path.join(OUTDIR, "s*.out.tsv"))):
    for ln, line in enumerate(open(p, encoding="utf-8"), 1):
        line = line.rstrip("\n")
        if not line: continue
        parts = line.split("\t")
        if len(parts) != 2: sys.exit(f"{p} line {ln}: {len(parts)} cols")
        k, v = parts
        if "\t" in v or "\r" in v: sys.exit(f"{p} line {ln}: real TAB/CR")
        if k in zh: dups.append(k)
        zh[k] = v
if dups: sys.exit("DUPS: " + ", ".join(dups[:20]))

PLACE = re.compile(r"%[sSdDfF][0-9]")            # numbered value placeholders
LINK_OPEN = re.compile(r"\[LINK=[^\]]*\]")
LINK_CLOSE = re.compile(r"\[\\+LINK\]")
BRACK = re.compile(r"\[[^\]]*\]")
ENT   = re.compile(r"&#[0-9]+;")                 # numeric HTML entities in source
def ms(pat, s): return collections.Counter(pat.findall(s))

raw = open(SRC, encoding="utf-8", newline="").read()
assert "\r" not in raw
lines = raw.split("\n"); trailing = ""
if lines and lines[-1] == "": lines = lines[:-1]; trailing = "\n"

out = [lines[0]]; missing = []; fails = []
for i, line in enumerate(lines[1:], 2):
    cols = line.split("\t")
    if len(cols) != 4: sys.exit(f"src line {i}: {len(cols)} cols")
    fp, key, en, old = cols
    if key not in zh:
        missing.append((i, key)); out.append(line); continue
    cn = zh[key]
    if ms(PLACE, en) != ms(PLACE, cn):
        fails.append(("PLACE", i, key, dict(ms(PLACE,en)), dict(ms(PLACE,cn))))
    if len(LINK_OPEN.findall(en)) != len(LINK_OPEN.findall(cn)):
        fails.append(("LINKOPEN", i, key, len(LINK_OPEN.findall(en)), len(LINK_OPEN.findall(cn))))
    if len(LINK_CLOSE.findall(en)) != len(LINK_CLOSE.findall(cn)):
        fails.append(("LINKCLOSE", i, key, len(LINK_CLOSE.findall(en)), len(LINK_CLOSE.findall(cn))))
    # bracket multiset -> WARN (排版重排允许), but report
    eb, cb = ms(BRACK, en), ms(BRACK, cn)
    if eb != cb:
        diff_e = {k:v for k,v in eb.items() if cb.get(k,0)!=v}
        diff_c = {k:v for k,v in cb.items() if eb.get(k,0)!=v}
        fails.append(("BRACKET", i, key, diff_e, diff_c))
    # source numeric entities must be preserved
    if ms(ENT, en) != ms(ENT, cn):
        fails.append(("ENTITY", i, key, dict(ms(ENT,en)), dict(ms(ENT,cn))))
    if "&#x" in cn: fails.append(("HEXLEAK", i, key, "&#x", ""))
    if "\n" in cn or "\t" in cn: fails.append(("REALWS", i, key, "", ""))
    out.append("\t".join([fp, key, en, cn]))

print(f"translations loaded: {len(zh)}")
print(f"source data rows: {len(lines)-1}")
print(f"missing: {len(missing)}")
for i,k in missing[:60]: print("   MISS", i, k)
print(f"FAILs: {len(fails)}")
for f in fails[:80]: print("   FAIL", f[0], "line", f[1], f[2], "en=", f[3], "cn=", f[4])

if WRITE:
    if fails: sys.exit("REFUSING to write: FAILs present")
    if missing: sys.exit("REFUSING to write: missing")
    shutil.copy2(SRC, SRC + ".bak-assemble")
    open(SRC, "w", encoding="utf-8", newline="").write("\n".join(out) + trailing)
    print(f"WROTE {SRC}")
else:
    print("(verify-only; pass --write to apply)")
