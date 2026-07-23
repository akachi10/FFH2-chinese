# -*- coding: utf-8 -*-
import re, sys, os, importlib.util
from collections import Counter

BASE = os.path.dirname(os.path.abspath(__file__))
TSV = os.path.join(BASE, 'batch-13.tsv')

def load(mod):
    spec = importlib.util.spec_from_file_location(mod, os.path.join(BASE, mod + '.py'))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m.P

P = {}
for part in ['_g_part_a','_g_part_b','_g_part_c']:
    d = load(part)
    for k,v in d.items():
        if k in P:
            print('DUP para index across parts:', k); sys.exit(1)
        P[k] = v

# read tsv
raw = open(TSV,'r',encoding='utf-8',newline='').read()
lines = raw.split('\n')
trailing = ''
if lines and lines[-1] == '':
    lines = lines[:-1]; trailing='\n'
assert lines[0] == 'file\tkey\tenglish\tchinese', repr(lines[0])
assert len(lines) == 2, f'expected 1 data row, got {len(lines)-1}'
fcol,key,eng,chi = lines[1].split('\t')
assert key == 'TXT_KEY_LEADER_GOSEA_PEDIA', key
assert chi == '', 'chinese not empty in source'

# split english by paragraph markers, capturing markers
parts = re.split(r'(\[PARAGRAPH(?::4)?\])', eng)
texts = [parts[i] for i in range(0,len(parts),2)]
markers = [parts[i] for i in range(1,len(parts),2)]
n = len(texts)
print('english paragraphs:', n, 'markers:', len(markers))

# ensure translations exist for every paragraph index
missing = [i for i in range(n) if i not in P]
if missing:
    print('MISSING para translations:', missing); sys.exit(2)
extra = [k for k in P if k>=n]
if extra:
    print('EXTRA para keys beyond range:', extra); sys.exit(2)

# rejoin using ORIGINAL marker sequence -> guarantees marker preservation
zh_parts = []
for i in range(n):
    zh_parts.append(P[i])
    if i < len(markers):
        zh_parts.append(markers[i])
zh = ''.join(zh_parts)

# validation
problems = []
if '\t' in zh or '\n' in zh or '\r' in zh:
    problems.append('translation contains real TAB/NEWLINE/CR')
# marker multiset must match exactly
M = re.compile(r'\[[^\]]*\]')
if Counter(M.findall(eng)) != Counter(M.findall(zh)):
    problems.append('marker multiset mismatch: eng=%s zh=%s' % (dict(Counter(M.findall(eng))), dict(Counter(M.findall(zh)))))
# numeric placeholders (none expected, but check)
NUM = re.compile(r'%[sSdDfF]\d+')
if Counter(NUM.findall(eng)) != Counter(NUM.findall(zh)):
    problems.append('num placeholder mismatch')
# LINK: none expected
LINK = re.compile(r'\[LINK=[^\]]*\]')
if LINK.findall(zh):
    problems.append('unexpected LINK in zh: %s' % LINK.findall(zh))
# ordered marker sequence identical
eng_markers = M.findall(eng)
zh_markers = M.findall(zh)
if eng_markers != zh_markers:
    # find first diff
    for idx,(a,b) in enumerate(zip(eng_markers, zh_markers)):
        if a!=b:
            problems.append(f'marker order diff at {idx}: eng={a} zh={b}'); break
    else:
        problems.append(f'marker count diff {len(eng_markers)} vs {len(zh_markers)}')

if problems:
    print('=== PROBLEMS ==='); [print(p) for p in problems]; sys.exit(3)

new_line = '\t'.join([fcol, key, eng, zh])
# verify cols1-3 unchanged
c=new_line.split('\t')
assert c[0]==fcol and c[1]==key and c[2]==eng
out = lines[0] + '\n' + new_line + trailing
open(TSV,'w',encoding='utf-8',newline='').write(out)
print('OK: wrote GOSEA translation. paragraphs=%d, markers preserved=%d, ordered-identical=%s, no real WS.' % (n, len(zh_markers), eng_markers==zh_markers))
print('zh char length:', len(zh))
