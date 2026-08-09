#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
YK 中文版 6 列格式转换器

背景:英克(YK)官方简中版 Civ4(日版 CyberFront 底子)按**位置**读取文本列,
运行时实际取第 5 号位。已验证格式(ffh2_041_o_ch 补丁 + YK 正版 BtS 文本):
每条 TEXT 固定 7 个子节点:

    <Tag> <English> <L1/> <L2/> <L3/> <L4/> <Chinese>

DLL 源码(CvInfos.cpp CvGameText::read)证实:语言数由第一条学习且遇短即永久
收缩,故**每条必须齐 6 列**,标签名无所谓、位置是一切。

本工具把两份输入合成 YK 格式覆盖包:
  - English 列 <- MM源码 基线的 English 列(原文,含 Text/Gender/Plural 嵌套保形)
  - Chinese 列 <- MM汉化MOD 的 English 列(上一轮 Sprint 的全部译文,同样保形)
  - L1~L4 空占位;原 French/German/Italian/Spanish 列丢弃(YK 格式如此)
  - 非 ASCII 一律 &#x 数字实体,文件字节纯 ASCII;声明 GB2312(与已验证补丁一致)

转换后内置校验(不通过则退出码非 0):
  - 输出纯 ASCII、可解析、每条恰好 7 子节点且顺序正确、L1~L4 全空
  - Tag 序列与两份输入逐条一致
  - 往返等价:English 列内容 == 基线,Chinese 列内容 == 译文(含嵌套子节点逐项比对)

用法:
  python3 convert_yk6.py            # 全量 111 文件 -> MM汉化MOD-YK/
  python3 convert_yk6.py FILE.xml   # 只转指定文件(调试)
"""

import os
import sys
import xml.etree.ElementTree as ET

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SRC_DIR = os.path.join(ROOT, "MM源码", "Assets", "XML", "Text")
TRANS_DIR = os.path.join(ROOT, "MM汉化MOD", "Assets", "XML", "Text")
OUT_DIR = os.path.join(ROOT, "MM汉化MOD-YK", "Assets", "XML", "Text")

NS = "{http://www.firaxis.com}"
COL_CHILD_OK = {"Text", "Gender", "Plural"}

# 中文双列模式:MM 自带的 MNAI DLL 在语言索引 5 读文本时崩溃(2026-07-23 事件日志
# 0xc0000005 实证),语言索引 0 则完全正常。故把中文同时写入第 0 列(English 位),
# 玩家语言保持 English 即可见中文;第 5 列仍写中文,留待 DLL 修复后启用。
CH_IN_COL0 = True

# MM 的 Misc Text.xml 把 5 号语言槽命名为 Finnish;在 DLL 修复前选中它必崩,
# 改名为警示文案(勿选此项)保护玩家。
LANG5_KEY = "TXT_KEY_LANGUAGE_5"
LANG5_WARN = "勿选此项"  # 勿选此项


def local(tag):
    # 剥任意 {uri} 前缀:MM 源文件存在带空格的笔误 xmlns("http://www. firaxis. com"),
    # 只按标准 NS 剥会把整文件 2,567 条静默跳过
    return tag.rsplit("}", 1)[-1] if tag.startswith("{") else tag


def esc(s):
    """文本节点转义:&<> + 非 ASCII -> &#x 实体。"""
    out = []
    for ch in s:
        if ch == "&":
            out.append("&amp;")
        elif ch == "<":
            out.append("&lt;")
        elif ch == ">":
            out.append("&gt;")
        elif ord(ch) > 127:
            out.append("&#x%X;" % ord(ch))
        else:
            out.append(ch)
    return "".join(out)


def parse_texts(path):
    """解析一个 Civ4GameText 文件,返回 TEXT 元素列表(ET Element)。

    输出文件声明 GB2312(expat 不支持该编码名)但字节纯 ASCII,故一律按
    ASCII 读入并剥掉 xml 声明后从字符串解析。
    """
    # latin-1 逐字节 1:1,兼容基线的 ISO-8859-1 原文与输出的纯 ASCII
    raw = open(path, "rb").read().decode("latin-1")
    if raw.startswith("<?xml"):
        raw = raw[raw.index("?>") + 2:]
    root = ET.fromstring(raw)
    return [el for el in root if local(el.tag) == "TEXT"]


def find_col(text_el, name):
    for child in text_el:
        if local(child.tag) == name:
            return child
    return None


def col_shape(el):
    """列内容规范形:(纯文本,) 或 ("NESTED", ((子名, 值), ...))。"""
    kids = [c for c in el if True]
    if not kids:
        return ("PLAIN", el.text or "")
    names = [local(c.tag) for c in kids]
    bad = [n for n in names if n not in COL_CHILD_OK]
    if bad or (el.text or "").strip():
        raise ValueError("列出现意外结构: 子节点=%s 直文=%r" % (names, el.text))
    return ("NESTED", tuple((local(c.tag), c.text or "") for c in kids))


def render_col(name, shape, indent="\t\t"):
    kind, payload = shape
    if kind == "PLAIN":
        if payload == "":
            return "%s<%s></%s>" % (indent, name, name)
        return "%s<%s>%s</%s>" % (indent, name, esc(payload), name)
    lines = ["%s<%s>" % (indent, name)]
    for child_name, val in payload:
        lines.append("%s\t<%s>%s</%s>" % (indent, child_name, esc(val), child_name))
    lines.append("%s</%s>" % (indent, name))
    return "\n".join(lines)


def convert_file(fname):
    src_texts = parse_texts(os.path.join(SRC_DIR, fname))
    trans_texts = parse_texts(os.path.join(TRANS_DIR, fname))
    if len(src_texts) != len(trans_texts):
        raise ValueError("%s: 条目数不一致 基线=%d 译文=%d" % (fname, len(src_texts), len(trans_texts)))

    blocks = []
    for i, (s_el, t_el) in enumerate(zip(src_texts, trans_texts)):
        s_tag = (find_col(s_el, "Tag").text or "").strip()
        t_tag = (find_col(t_el, "Tag").text or "").strip()
        if s_tag != t_tag:
            raise ValueError("%s #%d: Tag 错位 基线=%s 译文=%s" % (fname, i, s_tag, t_tag))
        s_eng = find_col(s_el, "English")
        t_eng = find_col(t_el, "English")
        if s_eng is None or t_eng is None:
            raise ValueError("%s %s: 缺 English 列" % (fname, s_tag))

        if s_tag == LANG5_KEY:
            eng_shape = chi_shape = ("PLAIN", LANG5_WARN)
        else:
            chi_shape = col_shape(t_eng)
            eng_shape = chi_shape if CH_IN_COL0 else col_shape(s_eng)

        blocks.append("\n".join([
            "\t<TEXT>",
            "\t\t<Tag>%s</Tag>" % esc(s_tag),
            render_col("English", eng_shape),
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
    out_path = os.path.join(OUT_DIR, fname)
    with open(out_path, "w", encoding="ascii", newline="\n") as f:
        f.write(body)
    return len(blocks)


def verify_file(fname):
    """输出结构 + 往返等价校验,返回问题列表。"""
    problems = []
    out_path = os.path.join(OUT_DIR, fname)
    raw = open(out_path, "rb").read()
    non_ascii = [b for b in raw if b > 0x7F]
    if non_ascii:
        problems.append("非 ASCII 字节 %d 个" % len(non_ascii))

    out_texts = parse_texts(out_path)
    src_texts = parse_texts(os.path.join(SRC_DIR, fname))
    trans_texts = parse_texts(os.path.join(TRANS_DIR, fname))
    if not (len(out_texts) == len(src_texts) == len(trans_texts)):
        problems.append("条目数不一致 出=%d 基线=%d 译文=%d" % (len(out_texts), len(src_texts), len(trans_texts)))
        return problems

    for i, (o_el, s_el, t_el) in enumerate(zip(out_texts, src_texts, trans_texts)):
        names = [local(c.tag) for c in o_el]
        tag = (find_col(o_el, "Tag").text or "") if find_col(o_el, "Tag") is not None else "?#%d" % i
        if names != ["Tag", "English", "L1", "L2", "L3", "L4", "Chinese"]:
            problems.append("%s: 子节点序列错误 %s" % (tag, names))
            continue
        for ln in ("L1", "L2", "L3", "L4"):
            lc = find_col(o_el, ln)
            if len(lc) or (lc.text or "").strip():
                problems.append("%s: %s 非空" % (tag, ln))
        s_tag = (find_col(s_el, "Tag").text or "").strip()
        if (tag or "").strip() != s_tag:
            problems.append("#%d: Tag 与基线不符 出=%s 基线=%s" % (i, tag, s_tag))
        try:
            if s_tag == LANG5_KEY:
                expect = ("PLAIN", LANG5_WARN)
                if col_shape(find_col(o_el, "English")) != expect or col_shape(find_col(o_el, "Chinese")) != expect:
                    problems.append("%s: 语言槽 5 警示文案未落实" % tag)
            else:
                trans_shape = col_shape(find_col(t_el, "English"))
                eng_expect = trans_shape if CH_IN_COL0 else col_shape(find_col(s_el, "English"))
                if col_shape(find_col(o_el, "English")) != eng_expect:
                    problems.append("%s: English 列与预期不等价" % tag)
                if col_shape(find_col(o_el, "Chinese")) != trans_shape:
                    problems.append("%s: Chinese 列与译文不等价" % tag)
        except ValueError as e:
            problems.append("%s: %s" % (tag, e))
    return problems


def main():
    only = sys.argv[1] if len(sys.argv) > 1 else None
    os.makedirs(OUT_DIR, exist_ok=True)
    files = sorted(f for f in os.listdir(SRC_DIR) if f.lower().endswith(".xml"))
    if only:
        files = [f for f in files if f == only]
        if not files:
            print("找不到文件: %s" % only)
            return 1

    total = 0
    fail = 0
    for fname in files:
        try:
            n = convert_file(fname)
        except Exception as e:
            print("[FAIL] %s 转换异常: %s" % (fname, e))
            fail += 1
            continue
        probs = verify_file(fname)
        if probs:
            fail += 1
            print("[FAIL] %s (%d 条):" % (fname, n))
            for p in probs[:10]:
                print("    - %s" % p)
            if len(probs) > 10:
                print("    ... 共 %d 个问题" % len(probs))
        else:
            total += n
    print("=" * 50)
    print("文件 %d/%d PASS,共 %d 条;FAIL 文件 %d" % (len(files) - fail, len(files), total, fail))
    return 1 if fail else 0


if __name__ == "__main__":
    sys.exit(main())
