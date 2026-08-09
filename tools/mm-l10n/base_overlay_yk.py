#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
YK 基础游戏文本 -> MM 覆盖包(第 0 列中文化)

背景:MM 在语言槽 0(English)下运行(MNAI DLL 槽 5 必崩),我们的 12,725 条 MM
译文已写入第 0 列;但界面上大量文本属于**基础游戏 key**(YK 本体 Text 文件,第 0
列是英文原文、第 5 列是现成中文),不在 MM 覆盖范围内,故仍显示英文。

本工具把 YK 本体的 26 个文本文件(原版 16 + BtS 10)做"第 5 列中文抄进第 0 列"
变换,产出追加覆盖文件(YKBase_*.xml)放进 MM 覆盖包——mod 内文本按 Tag 覆盖基础
游戏,基础 key 也就全中文了。

规则:
  - 源文件为 GB2312 声明 + 原始 GB2312 字节(部分为实体混排),按 GBK 解码;
  - 每条 TEXT:第 0 列与第 5 列均取源第 5 列(Chinese)内容;源中文列缺失/为空
    则保留英文(兜底不留空);
  - MM 已定义的 Tag 一律跳过(MM 覆盖包已有更贴合 MM 语境的译文,且避免 mod 内
    同 key 加载顺序之争);
  - 输出纯 ASCII(非 ASCII -> &#x 实体)、GB2312 声明、每条恰好 7 子节点。

内置校验:输出可解析、纯 ASCII、结构 7 节点、第 0 列==第 5 列、Tag 不与 MM 冲突。

用法:
  python3 base_overlay_yk.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from convert_yk6 import (ROOT, OUT_DIR, SRC_DIR, local, esc, col_shape,
                         render_col, find_col)
import xml.etree.ElementTree as ET

BASE_DIRS = [
    ("/c/Civilization4/Assets/XML/Text", "C:/Civilization4/Assets/XML/Text"),
    ("/c/Civilization4/Beyond the Sword/Assets/XML/Text",
     "C:/Civilization4/Beyond the Sword/Assets/XML/Text"),
]


def parse_texts_gbk(path):
    raw = open(path, "rb").read().decode("gbk")
    if raw.startswith("<?xml"):
        raw = raw[raw.index("?>") + 2:]
    root = ET.fromstring(raw)
    return [el for el in root if local(el.tag) == "TEXT"]


def mm_tag_set():
    tags = set()
    for f in os.listdir(SRC_DIR):
        if not f.lower().endswith(".xml"):
            continue
        raw = open(os.path.join(SRC_DIR, f), "rb").read().decode("latin-1")
        if raw.startswith("<?xml"):
            raw = raw[raw.index("?>") + 2:]
        for el in ET.fromstring(raw):
            if local(el.tag) != "TEXT":
                continue
            t = find_col(el, "Tag")
            if t is not None and t.text:
                tags.add(t.text.strip())
    return tags


def is_empty_shape(shape):
    kind, payload = shape
    if kind == "PLAIN":
        return payload.strip() == ""
    return all((v or "").strip() == "" for _, v in payload
               if _ == "Text") if payload else True


def convert_base_file(src_path, out_name, mm_tags):
    texts = parse_texts_gbk(src_path)
    blocks = []
    skipped = 0
    fallback = 0
    for el in texts:
        tag_el = find_col(el, "Tag")
        tag = (tag_el.text or "").strip() if tag_el is not None else ""
        if not tag:
            continue
        if tag in mm_tags:
            skipped += 1
            continue
        eng = find_col(el, "English")
        chi = find_col(el, "Chinese")
        eng_shape = col_shape(eng) if eng is not None else ("PLAIN", "")
        chi_shape = col_shape(chi) if chi is not None else None
        if chi_shape is None or is_empty_shape(chi_shape):
            chi_shape = eng_shape
            fallback += 1
        blocks.append("\n".join([
            "\t<TEXT>",
            "\t\t<Tag>%s</Tag>" % esc(tag),
            render_col("English", chi_shape),
            "\t\t<L1/>",
            "\t\t<L2/>",
            "\t\t<L3/>",
            "\t\t<L4/>",
            render_col("Chinese", chi_shape),
            "\t</TEXT>",
        ]))
    body = "\n".join([
        '<?xml version="1.0" encoding="GB2312"?>',
        '<Civ4GameText xmlns="http://www.firaxis.com">',
        "\n".join(blocks),
        "</Civ4GameText>",
        "",
    ])
    with open(os.path.join(OUT_DIR, out_name), "w", encoding="ascii", newline="\n") as f:
        f.write(body)
    return len(blocks), skipped, fallback


def verify(out_name, mm_tags):
    problems = []
    path = os.path.join(OUT_DIR, out_name)
    raw_b = open(path, "rb").read()
    if any(b > 0x7F for b in raw_b):
        problems.append("非 ASCII 字节")
    raw = raw_b.decode("ascii")
    if raw.startswith("<?xml"):
        raw = raw[raw.index("?>") + 2:]
    for el in ET.fromstring(raw):
        if local(el.tag) != "TEXT":
            continue
        names = [local(c.tag) for c in el]
        tag = (find_col(el, "Tag").text or "?")
        if names != ["Tag", "English", "L1", "L2", "L3", "L4", "Chinese"]:
            problems.append("%s: 子节点序列 %s" % (tag, names))
            continue
        if col_shape(find_col(el, "English")) != col_shape(find_col(el, "Chinese")):
            problems.append("%s: 第0列!=第5列" % tag)
        if tag.strip() in mm_tags:
            problems.append("%s: 与 MM key 冲突" % tag)
    return problems


def main():
    mm_tags = mm_tag_set()
    print("MM key 总数: %d" % len(mm_tags))
    total = 0
    fail = 0
    for posix_dir, _ in BASE_DIRS:
        d = posix_dir if os.path.isdir(posix_dir) else posix_dir.replace("/c/", "C:/")
        for f in sorted(os.listdir(d)):
            if not f.lower().endswith(".xml"):
                continue
            out_name = "YKBase_%s" % f
            try:
                n, sk, fb = convert_base_file(os.path.join(d, f), out_name, mm_tags)
            except Exception as e:
                print("[FAIL] %s: %s" % (f, e))
                fail += 1
                continue
            probs = verify(out_name, mm_tags)
            if probs:
                fail += 1
                print("[FAIL] %s:" % out_name)
                for p in probs[:8]:
                    print("    - %s" % p)
            else:
                total += n
                print("[OK] %-50s %5d 条(跳过 MM 重复 %d,英文兜底 %d)" % (out_name, n, sk, fb))
    print("=" * 60)
    print("合计 %d 条;FAIL %d" % (total, fail))
    return 1 if fail else 0


if __name__ == "__main__":
    sys.exit(main())
