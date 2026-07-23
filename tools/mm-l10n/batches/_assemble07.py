#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Assemble batch-07.tsv col 4 from _frag07/s0*.out.tsv. Cols 1-3 byte-for-byte."""
import sys, os, glob
BASE = os.path.dirname(os.path.abspath(__file__))
SRC  = os.path.join(BASE, "batch-07.tsv")
zh={}; dups=[]
for p in sorted(glob.glob(os.path.join(BASE,"_frag07","s0*.out.tsv"))):
    for ln,line in enumerate(open(p,encoding="utf-8"),1):
        line=line.rstrip("\n")
        if not line: continue
        parts=line.split("\t")
        if len(parts)!=2: sys.exit(f"{p} line {ln}: {len(parts)} cols")
        k,v=parts
        if "\t" in v or "\n" in v: sys.exit(f"{p} line {ln}: real TAB/NL")
        if k in zh: dups.append(k)
        zh[k]=v
if dups: sys.exit("DUPS: "+", ".join(dups[:20]))
raw=open(SRC,encoding="utf-8",newline="").read()
assert "\r" not in raw
lines=raw.split("\n"); trailing=""
if lines and lines[-1]=="": lines=lines[:-1]; trailing="\n"
out=[lines[0]]; missing=[]
for i,line in enumerate(lines[1:],2):
    cols=line.split("\t")
    if len(cols)!=4: sys.exit(f"src line {i}: {len(cols)} cols")
    fp,key,en,old=cols
    if key not in zh: missing.append(key); out.append(line); continue
    out.append("\t".join([fp,key,en,zh[key]]))
if missing: sys.exit(f"MISSING {len(missing)}: "+", ".join(missing[:20]))
open(SRC,"w",encoding="utf-8",newline="").write("\n".join(out)+trailing)
print(f"assembled {len(lines)-1} data rows")
