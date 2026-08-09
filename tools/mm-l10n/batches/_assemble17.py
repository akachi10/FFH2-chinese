#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Assemble batch-17.tsv col 4 from _b17_out/s*.out.tsv (key<TAB>chinese).
Cols 1-3 byte-for-byte. Strict parity: LINK-open TARGET multiset, [\\LINK] close
count, all bracket markers, literal \\n / \\t counts must match source per row.
Run: python3 _assemble17.py            # verify
     python3 _assemble17.py --write    # write (backs up)
"""
import sys, os, re, glob, csv, shutil, collections

BASE = os.path.dirname(os.path.abspath(__file__))
SRC  = os.path.join(BASE, "batch-17.tsv")
OUTDIR = os.path.join(BASE, "_b17_out")
WRITE = "--write" in sys.argv

# load translations
zh = {}; dups = []
for p in sorted(glob.glob(os.path.join(OUTDIR, "s*.out.tsv"))):
    for ln, line in enumerate(open(p, encoding="utf-8"), 1):
        line = line.rstrip("\n")
        if not line: continue
        parts = line.split("\t")
        if len(parts) != 2:
            sys.exit(f"{p} line {ln}: {len(parts)} cols")
        k, v = parts
        if "\t" in v or "\r" in v:
            sys.exit(f"{p} line {ln}: real TAB/CR in translation")
        if k in zh: dups.append(k)
        zh[k] = v
if dups: sys.exit("DUPS: " + ", ".join(dups[:20]))

# marker extractors
LINK_OPEN = re.compile(r"\[LINK=[^\]]*\]")      # full open incl target
LINK_CLOSE = re.compile(r"\[\\+LINK\]")          # close, 1+ backslashes
BRACK = re.compile(r"\[[^\]]*\]")                # any bracket marker
def ms(pat, s): return collections.Counter(pat.findall(s))
def lit(s, sub): return s.count(sub)

raw = open(SRC, encoding="utf-8", newline="").read()
assert "\r" not in raw
lines = raw.split("\n"); trailing = ""
if lines and lines[-1] == "": lines = lines[:-1]; trailing = "\n"

out = [lines[0]]
missing = []; fails = []
for i, line in enumerate(lines[1:], 2):
    cols = line.split("\t")
    if len(cols) != 4: sys.exit(f"src line {i}: {len(cols)} cols")
    fp, key, en, old = cols
    if key not in zh:
        missing.append((i, key)); out.append(line); continue
    cn = zh[key]
    # LINK open target multiset
    if ms(LINK_OPEN, en) != ms(LINK_OPEN, cn):
        de, dc = ms(LINK_OPEN, en), ms(LINK_OPEN, cn)
        diff_e = {k: v for k, v in de.items() if dc.get(k,0)!=v}
        diff_c = {k: v for k, v in dc.items() if de.get(k,0)!=v}
        fails.append(("LINKOPEN", i, key, diff_e, diff_c))
    # LINK close count
    if len(LINK_CLOSE.findall(en)) != len(LINK_CLOSE.findall(cn)):
        fails.append(("LINKCLOSE", i, key, len(LINK_CLOSE.findall(en)), len(LINK_CLOSE.findall(cn))))
    # all brackets multiset
    if ms(BRACK, en) != ms(BRACK, cn):
        de, dc = ms(BRACK, en), ms(BRACK, cn)
        diff_e = {k: v for k, v in de.items() if dc.get(k,0)!=v}
        diff_c = {k: v for k, v in dc.items() if de.get(k,0)!=v}
        fails.append(("BRACKET", i, key, diff_e, diff_c))
    # literal escapes \n \t
    for esc in ("\\n", "\\t"):
        if lit(en, esc) != lit(cn, esc):
            fails.append(("LITERAL"+esc, i, key, lit(en, esc), lit(cn, esc)))
    # forbidden
    if "&#x" in cn: fails.append(("ENTITY", i, key, "&#x", ""))
    if "\n" in cn or "\t" in cn: fails.append(("REALWS", i, key, "", ""))
    out.append("\t".join([fp, key, en, cn]))

print(f"translations loaded: {len(zh)}")
print(f"source data rows: {len(lines)-1}")
print(f"missing (empty col4): {len(missing)}")
for i, k in missing: print("   MISS", i, k)
print(f"FAILs: {len(fails)}")
for f in fails[:80]: print("   FAIL", f[0], "line", f[1], f[2], "en=", f[3], "cn=", f[4])

if WRITE:
    if fails: sys.exit("REFUSING to write: FAILs present")
    if missing: sys.exit("REFUSING to write: missing translations")
    shutil.copy2(SRC, SRC + ".bak-assemble")
    open(SRC, "w", encoding="utf-8", newline="").write("\n".join(out) + trailing)
    print(f"WROTE {SRC}")
else:
    print("(verify-only; pass --write to apply)")
