#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fill chinese column of batch-02.tsv from TRANS dict, keyed by key.
Columns 1-3 are copied byte-for-byte from the original; only column 4 is set.
Fails loudly if any key is missing a translation or duplicated."""
import io, sys

SRC = "batch-02.tsv"
TRANS = {}  # key -> chinese (populated below)

def load_trans():
    import _trans_b02_data as d
    return d.T

def main():
    T = load_trans()
    with io.open(SRC, "r", encoding="utf-8", newline="") as f:
        lines = f.read().split("\n")
    # preserve trailing newline structure
    out = []
    header = lines[0]
    out.append(header)
    missing = []
    seen = set()
    body = lines[1:]
    # drop a possible trailing empty line from split
    trailing_empty = False
    if body and body[-1] == "":
        trailing_empty = True
        body = body[:-1]
    for ln in body:
        parts = ln.split("\t")
        if len(parts) < 3:
            raise SystemExit("bad row (fewer than 3 cols): %r" % ln)
        file_, key, english = parts[0], parts[1], parts[2]
        # english may itself have been split if it contained real tabs -> must not
        if len(parts) > 4:
            raise SystemExit("row has >4 tab-fields, real tab in english? key=%s" % key)
        zh = T.get(key)
        if zh is None:
            missing.append(key)
            zh = ""
        if key in seen:
            raise SystemExit("duplicate key in file: %s" % key)
        seen.add(key)
        if "\t" in zh or "\n" in zh.replace("\\n",""):
            raise SystemExit("chinese has real tab/newline: %s" % key)
        out.append("\t".join([file_, key, english, zh]))
    if missing:
        sys.stderr.write("MISSING %d keys:\n" % len(missing))
        for k in missing[:50]:
            sys.stderr.write("  " + k + "\n")
        raise SystemExit(1)
    txt = "\n".join(out)
    if trailing_empty:
        txt += "\n"
    with io.open(SRC, "w", encoding="utf-8", newline="") as f:
        f.write(txt)
    print("OK wrote %d body rows" % (len(out)-1))

if __name__ == "__main__":
    main()
