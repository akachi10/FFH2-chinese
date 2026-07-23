#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fill chinese column of batch-11.tsv. Preserves cols 1-3 byte-for-byte."""
import os
SRC = os.path.join(os.path.dirname(__file__), "batch-11.tsv")
TRANS = {}
def add(d):
    for k, v in d.items():
        if k in TRANS: raise SystemExit("DUP KEY: " + k)
        TRANS[k] = v
# chunks appended below
