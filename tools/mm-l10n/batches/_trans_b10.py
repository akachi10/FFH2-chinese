#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fill chinese column of batch-10.tsv. Cols 1-3 copied byte-for-byte; only col4 set."""
import io, sys
SRC = "batch-10.tsv"

def main():
    import _trans_b10_data as d
    T = d.T
    with io.open(SRC, "r", encoding="utf-8", newline="") as f:
        lines = f.read().split("\n")
    out = [lines[0]]
    body = lines[1:]
    trailing_empty = False
    if body and body[-1] == "":
        trailing_empty = True
        body = body[:-1]
    missing = []; seen = set()
    for ln in body:
        parts = ln.split("\t")
        if len(parts) < 3:
            raise SystemExit("bad row (<3 cols): %r" % ln)
        if len(parts) > 4:
            raise SystemExit("row has >4 tab-fields (real tab in english?) key=%s" % parts[1])
        file_, key, english = parts[0], parts[1], parts[2]
        zh = T.get(key)
        if zh is None:
            missing.append(key); zh = ""
        if key in seen:
            raise SystemExit("duplicate key: %s" % key)
        seen.add(key)
        if "\t" in zh or "\n" in zh:
            raise SystemExit("chinese has real tab/newline: %s" % key)
        out.append("\t".join([file_, key, english, zh]))
    if missing:
        sys.stderr.write("MISSING %d keys:\n" % len(missing))
        for k in missing[:60]:
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
