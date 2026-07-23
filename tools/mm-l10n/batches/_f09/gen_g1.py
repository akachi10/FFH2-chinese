# -*- coding: utf-8 -*-
# Generates g1.out.tsv (linenum<TAB>chinese) for the 19 mana-PEDIA rows.
# Strategy: build Chinese by string-replacing visible English tokens inside the
# English source, leaving every [LINK=...], [\\LINK], [NEWLINE], [TAB], [ICON_*],
# [PARAGRAPH*] marker byte-for-byte intact. Then hand-translate the prose tails.
import re, io, os
BASE=os.path.dirname(os.path.abspath(__file__))
src={}
for line in open(os.path.join(BASE,"g1.tsv"),encoding='utf-8'):
    c=line.rstrip("\n").split("\t")
    src[int(c[0])]=(c[2],c[3])   # linenum -> (key, english)

CL="["+chr(92)+chr(92)+"LINK]"   # [\\LINK]

# ---- shared visible-text replacements applied to the spell-list header block ----
# order matters: longer keys first
COMMON=[
 ("Death Affinity","死亡亲和"),("Undeath Affinity","不死亲和"),
 ("Chaos Affinity","混乱亲和"),
 ("Death I","死亡 I"),("Death II","死亡 II"),("Death III","死亡 III"),
 ("Undeath I","不死 I"),("Undeath II","不死 II"),("Undeath III","不死 III"),
 ("Channeling I","引导 I"),("Channeling II","引导 II"),("Channeling III","引导 III"),("Channeling IV","引导 IV"),
 ("Arcane units","秘法单位"),("Adepts","术士"),
 ("Affinity for this sphere","对该领域的亲和"),
]
# We won't fully auto-translate; instead each row is authored below with full CN.
out={}
