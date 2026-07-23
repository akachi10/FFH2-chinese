#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Assemble batch-20.tsv col4 from _f20/*.out.tsv (linenum<TAB>chinese).
Keyed by source LINE NUMBER (robust to duplicate keys). Cols 1-3 byte-preserved.
Validates placeholder multiset (case-sensitive) + LINK open/close byte-exact parity."""
import sys, re, os
BASE=os.path.dirname(os.path.abspath(__file__))
SRC=os.path.join(BASE,"batch-20.tsv")
FRAGS=["h1","h2","h3","h4","h5"]
PLACE=re.compile(r'%[sSdDfF][0-9]')
OPEN="[LINK="
CLOSE="["+chr(92)+chr(92)+"LINK]"

zh={}
for f in FRAGS:
    p=os.path.join(BASE,"_f20",f+".out.tsv")
    if not os.path.exists(p): sys.exit("MISSING "+p)
    for ln,line in enumerate(open(p,encoding='utf-8'),1):
        line=line.rstrip("\n")
        if line=="":continue
        parts=line.split("\t")
        if len(parts)!=2: sys.exit(f"{f} line{ln}: need 2 cols got {len(parts)}: {line[:80]!r}")
        num,cn=parts
        if "\t" in cn or "\n" in cn: sys.exit(f"{f} line{ln}: real tab/newline in cn")
        num=int(num)
        if num in zh: sys.exit(f"dup line {num} across fragments")
        zh[num]=cn

raw=open(SRC,encoding='utf-8',newline='').read()
assert "\r" not in raw,"source has CR"
lines=raw.split("\n")
trailing="\n" if lines and lines[-1]=="" else ""
if trailing:lines=lines[:-1]
out=[lines[0]]
missing=[];problems=[]
for i,line in enumerate(lines[1:],2):
    c=line.split("\t")
    if len(c)!=4: sys.exit(f"src line {i}: {len(c)} cols")
    fpath,key,en,_=c
    cn=zh.get(i,"")
    if i not in zh: missing.append((i,key))
    else:
        if sorted(PLACE.findall(en))!=sorted(PLACE.findall(cn)):
            problems.append(f"L{i} {key}: PH EN={sorted(PLACE.findall(en))} CN={sorted(PLACE.findall(cn))}")
        if en.count(OPEN)!=cn.count(OPEN) or en.count(CLOSE)!=cn.count(CLOSE):
            problems.append(f"L{i} {key}: LINK EN o{en.count(OPEN)}/c{en.count(CLOSE)} CN o{cn.count(OPEN)}/c{cn.count(CLOSE)}")
    out.append("\t".join([fpath,key,en,cn]))
result="\n".join(out)+trailing
print(f"src data rows={len(lines)-1} loaded={len(zh)} missing={len(missing)} problems={len(problems)}")
for i,k in missing[:40]: print("  MISSING L%d %s"%(i,k))
for p in problems[:60]: print("  "+p)
if "--write" in sys.argv:
    if missing: sys.exit("REFUSE write: missing rows")
    if problems: sys.exit("REFUSE write: validation problems")
    open(SRC,"w",encoding='utf-8',newline='').write(result)
    print("WROTE",SRC)
else:
    print("(dry run; --write to apply)")
