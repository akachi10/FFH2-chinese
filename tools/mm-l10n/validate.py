#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""MM 汉化覆盖包静态校验工具 (M4)。

比对覆盖包 (MM汉化MOD/Assets/XML/Text/) 对 基准 (MM源码/Assets/XML/Text/)，
逐文件执行以下校验（对应硬锚点 A1/A5，校验口径 v2 · SM 2026-07-23 裁决）：

  1. 可解析          —— xml.etree 解析通过（FAIL）
  2. key 集合一致    —— 覆盖包 <Tag> 集合、条数、顺序与基准完全一致（不增/删/重排/重复）（FAIL）
  3. 数值占位符守恒  —— 每条 English 的 %s1/%d1/%s2… 数值占位符多重集与基准一致，【大小写敏感】(%d1≠%D1)（FAIL；运行时报错风险）
  4. 方括号标记       —— 口径 v2（含 LINK 方向分档）：
        · 纯排版标记（[NEWLINE]/[TAB]/[PARAGRAPH:N]/[COLOR_*]/[COLOR_REVERT]/[BOLD]/[ICON_*] 等）多重集差异 = WARN（不计退出码）
        · LINK 类（[LINK=*]/[\LINK]/[/LINK]）【按方向】：译文【缺失】基准的 LINK = WARN（剥离正常产物，显示无损）；
          译文【多出】基准没有的 LINK = FAIL（防后续翻译批引入悬空链接目标）
        · 覆盖包出现【已知合法词表之外且基准原文也无】的未知标记 = FAIL
        · 闭合标记退化（成对族 X∈{H1,H2,BOLD,LINK}：相对基准【缺失 [\X]/[/X]】同时【多出裸 [X]】）
          = FAIL（转义反斜杠/斜杠被吞的特征签名，破坏成对结构，非合理排版重排）
  5. 其他语言未触碰   —— French/German/Italian/Spanish/Finnish 列（含 Gender/Plural 子结构）解析后值与基准逐字一致（FAIL）
  6. 改动行纯 ASCII   —— 只要求覆盖包中相对基准发生改动的 English 内容纯 ASCII（中文须用 &#x 实体，锚点 A1）；
                        未改动内容以"与基准一致"为准（由检查项 5 覆盖），基准既有的非 ASCII 不判错（FAIL）
  7. 实体合法        —— 所有 &#x/&# 数字实体可解码，解码后无控制字符（除常见空白）（FAIL）

退出码：全绿(可含 WARN) 0，任一 FAIL 非 0（=FAIL 文件数，封顶 100）。WARN 不影响退出码。

用法：
  python3 validate.py [覆盖包目录] [基准目录]
默认覆盖包目录 = <repo>/MM汉化MOD/Assets/XML/Text/
默认基准目录   = <repo>/MM源码/Assets/XML/Text/
"""
import sys
import os
import re
import glob
import xml.etree.ElementTree as ET

NS = "{http://www.firaxis.com}"
LANG_COLS = ("English", "French", "German", "Italian", "Spanish", "Finnish")
OTHER_LANGS = ("French", "German", "Italian", "Spanish", "Finnish")

# 数值占位符：% 后跟字母/数字组成的 token（如 %s1 %d1 %D1 %s2_city %s1_civ_adjective %s %d %f）
RE_PLACEHOLDER = re.compile(r"%[A-Za-z0-9_]+")
# 方括号标记：[ 到 ] 之间的整段（如 [NEWLINE] [COLOR_X] [LINK=Y] [\LINK] [PARAGRAPH:2]）
RE_MARKUP = re.compile(r"\[[^\[\]]*\]")

# 已知合法标记词表（从基准 MM源码 + 官方 0.41o 汉化包的 English 列归纳，SM 修订）。
# 命中任一 = 合法；覆盖包译文里出现且不命中任一、又不在该条基准原文中的标记 = 未知标记(FAIL)。
KNOWN_MARKUP_PATTERNS = [
    re.compile(p) for p in (
        r"^\[NEWLINE\]$",
        r"^\[TAB\]$",
        r"^\[SPACE\]$",
        r"^\[PARAGRAPH(:\d+)?\]$",          # [PARAGRAPH] / [PARAGRAPH:2]
        r"^\[COLOR_[A-Z0-9_]+\]$",          # 含 [COLOR_REVERT]
        r"^\[ICON_[A-Z0-9_]+\]$",
        r"^\[LINK=[^\[\]]*\]$",
        r"^\[\\LINK\]$", r"^\[/LINK\]$",
        r"^\[BOLD\]$", r"^\[\\BOLD\]$",
        r"^\[H[12]\]$", r"^\[\\H[12]\]$",
        # 运行时替换的具名变量标记族（英雄名/文明/宗教/敌国等，含 :N 序号变体）
        r"^\[(CT_[A-Z_]+|OUR_[A-Z_]+)(:\d+|\.\d+)?\]$",
        # 复数/性别选择标记 [NUM<n>:形式1:形式2:...]（英语原文中亦有少量）
        r"^\[NUM\d+:[^\[\]]*\]$",
        # 单占位替身 [s1] [s2_civ_adjective] [d1] [f] 等（少数原文写法）
        r"^\[[sdf]\d*(_[a-z_]+)?\]$",
        r"^\[[sdf]\d*:\d+_[a-z_]+\]$",
    )
]


def placeholder_key(tok):
    """数值占位符键：大小写敏感（口径 v2，%D1 与 %d1 视为不同 → 差异即 FAIL）。"""
    return tok


def is_known_markup(tok):
    return any(p.match(tok) for p in KNOWN_MARKUP_PATTERNS)


# LINK 类标记（[LINK=*] / [\LINK] / [/LINK]）：其多重集差异按口径 v2 判 FAIL。
RE_LINK_MARKUP = re.compile(r"^\[(LINK=[^\[\]]*|\\LINK|/LINK)\]$")


def is_link_markup(tok):
    return RE_LINK_MARKUP.match(tok) is not None


# 成对标记的「闭合退化」检测：闭标记 [\X] / [/X] 的反斜杠(或斜杠)被吞，退化成裸开标记 [X]。
# 这是转义被吞的特征签名，不是合理排版重排 —— 判 FAIL。
# X 覆盖 H1/H2/BOLD 及 LINK(闭标记写法 [\LINK] 或 [/LINK])。base_name 取标记内的字母数字名。
RE_CLOSE_MARKUP = re.compile(r"^\[[\\/]([A-Za-z0-9_]+)\]$")   # [\H1] [\BOLD] [/LINK] -> 名
RE_OPEN_BARE = re.compile(r"^\[([A-Za-z0-9_]+)\]$")          # 裸开标记 [H1] [BOLD] [LINK] -> 名
# 参与「闭合退化」判定的成对标记族(base 名)。LINK 的开标记通常带 =target，故裸 [LINK] 亦属退化特征。
PAIRED_MARKUP_NAMES = {"H1", "H2", "BOLD", "LINK"}


def close_markup_name(tok):
    """闭标记 [\\X]/[/X] -> 名 X（属成对族则返回，否则 None）。"""
    m = RE_CLOSE_MARKUP.match(tok)
    if m and m.group(1) in PAIRED_MARKUP_NAMES:
        return m.group(1)
    return None


def open_bare_name(tok):
    """裸开标记 [X] -> 名 X（属成对族则返回，否则 None）。"""
    m = RE_OPEN_BARE.match(tok)
    if m and m.group(1) in PAIRED_MARKUP_NAMES:
        return m.group(1)
    return None
# 数字实体：&#123; 或 &#x1F600;
RE_NUM_ENTITY = re.compile(r"&#(x[0-9A-Fa-f]+|[0-9]+);")
# 字节层切 <English>...</English> 段（含结构化内层 <Text>），用于精准 ASCII 校验（作用于原始字节）
RE_ENGLISH_BLOCK = re.compile(rb"<English>.*?</English>", re.S)
# 字节层按 Tag 提取紧随的 English 原始块：捕获 (Tag文本, English内层原始字节)。
RE_TAG_ENGLISH_RAW = re.compile(rb"<Tag>(.*?)</Tag>\s*<English>(.*?)</English>", re.S)


# ---------- 底层工具 ----------
def repo_root():
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))


def multiset(items):
    d = {}
    for it in items:
        d[it] = d.get(it, 0) + 1
    return d


def multiset_diff(base_ms, over_ms):
    """返回 (缺失, 多余) 两个 dict：base 有 over 没有 / over 有 base 没有。"""
    missing, extra = {}, {}
    keys = set(base_ms) | set(over_ms)
    for k in keys:
        b, o = base_ms.get(k, 0), over_ms.get(k, 0)
        if o < b:
            missing[k] = b - o
        elif o > b:
            extra[k] = o - b
    return missing, extra


def lang_value(text_elem, lang):
    """取某语言列的规范化值。

    列可能是简单文本 <English>xxx</English>，
    也可能是 <English><Text>xxx</Text><Gender>..</Gender><Plural>..</Plural></English>。
    返回 (kind, value)：
      kind='absent'  该列不存在
      kind='simple'  简单文本，value=文本
      kind='struct'  结构化，value=(Text, Gender, Plural) 元组
    """
    el = text_elem.find(NS + lang)
    if el is None:
        el = text_elem.find(lang)  # 兜底：无命名空间
    if el is None:
        return ("absent", None)
    sub_text = el.find(NS + "Text")
    if sub_text is None:
        sub_text = el.find("Text")
    if sub_text is not None:
        def g(tag):
            c = el.find(NS + tag)
            if c is None:
                c = el.find(tag)
            return None if c is None else (c.text or "")
        return ("struct", (sub_text.text or "", g("Gender"), g("Plural")))
    return ("simple", el.text or "")


def english_content(text_elem):
    """取 English 列用于占位符/标记比对的文本（结构化则取内层 Text）。"""
    kind, val = lang_value(text_elem, "English")
    if kind == "absent":
        return ""
    if kind == "struct":
        return val[0] or ""
    return val or ""


def tag_of(text_elem):
    t = text_elem.find(NS + "Tag")
    if t is None:
        t = text_elem.find("Tag")
    return None if t is None else (t.text or "")


def iter_texts(root):
    for t in root.iter(NS + "TEXT"):
        yield t
    # 兜底：若无命名空间
    if root.find(NS + "TEXT") is None:
        for t in root.iter("TEXT"):
            yield t


# ---------- 单文件校验 ----------
def validate_file(over_path, base_path):
    """返回 (checks, fails)：checks 是有序 (名称, ok, 明细列表)；fails 为失败明细总数。"""
    checks = []
    fname = os.path.basename(over_path)

    # 字节层校验先行（不依赖解析，解析失败也能报出精准定位）：实体合法。
    # 纯 ASCII（检查项 6）改为"仅改动的 English 内容"判定，需按 Tag 对齐，移到解析之后。
    raw = open(over_path, "rb").read()

    # 规则 7：数字实体合法
    text_str = raw.decode("ascii", errors="replace")
    bad_ent = []
    for m in RE_NUM_ENTITY.finditer(text_str):
        body = m.group(1)
        try:
            cp = int(body[1:], 16) if body[0] in "xX" else int(body)
        except ValueError:
            bad_ent.append("无法解析实体 %s" % m.group(0))
            continue
        try:
            ch = chr(cp)
        except (ValueError, OverflowError):
            bad_ent.append("码点越界 %s (U+%X)" % (m.group(0), cp))
            continue
        # 控制字符（除 \t \n \r）非法
        if (ord(ch) < 0x20 and ch not in "\t\n\r") or ord(ch) == 0x7F:
            bad_ent.append("解码为控制字符 %s (U+%X)" % (m.group(0), cp))
    if bad_ent:
        checks.append(("实体合法", False, bad_ent[:20]))
    else:
        checks.append(("实体合法", True, []))

    # 规则 1：覆盖包可解析（字节层校验已先跑，实体非法在此也可能触发解析错，两处独立报出）
    try:
        over_root = ET.parse(over_path).getroot()
        checks.append(("可解析", True, []))
    except Exception as e:
        checks.append(("可解析", False, ["覆盖包 XML 解析失败: %s" % e]))
        return checks, ("标记多重集不一致", 0, [])  # 无法解析，结构化比对无从谈起

    # 基准解析（基准坏则是环境问题，单列报出但不判覆盖包错）
    base_root = None
    base_err = None
    if base_path and os.path.exists(base_path):
        try:
            base_root = ET.parse(base_path).getroot()
        except Exception as e:
            base_err = str(e)

    over_texts = list(iter_texts(over_root))

    # 无基准则只能做上述"自洽"校验
    if base_root is None:
        detail = ["缺少基准文件，跳过 key/占位符/标记/其他语言列比对"]
        if base_err:
            detail.append("基准解析失败: %s" % base_err)
        checks.append(("基准比对", False, detail))
        return checks, ("标记多重集不一致", 0, [])

    base_texts = list(iter_texts(base_root))

    # 规则 2：key 集合一致（条数、顺序、值）
    over_tags = [tag_of(t) for t in over_texts]
    base_tags = [tag_of(t) for t in base_texts]
    key_details = []
    if over_tags != base_tags:
        if len(over_tags) != len(base_tags):
            key_details.append("条数不一致：基准 %d 条，覆盖包 %d 条" % (len(base_tags), len(over_tags)))
        base_set, over_set = set(base_tags), set(over_tags)
        removed = [k for k in base_tags if k not in over_set]
        added = [k for k in over_tags if k not in base_set]
        if removed:
            key_details.append("覆盖包缺失 key（%d 个）: %s" % (len(removed), ", ".join(removed[:10])))
        if added:
            key_details.append("覆盖包新增 key（%d 个）: %s" % (len(added), ", ".join(added[:10])))
        # 集合相同但顺序不同
        if not removed and not added and base_tags != over_tags:
            for i, (b, o) in enumerate(zip(base_tags, over_tags)):
                if b != o:
                    key_details.append("顺序不一致：第 %d 条 基准=%s 覆盖包=%s" % (i, b, o))
                    break
        # 重复检测
        dup = [k for k, c in multiset(over_tags).items() if c > 1]
        if dup:
            key_details.append("覆盖包存在重复 key: %s" % ", ".join(dup[:10]))
    checks.append(("key集合一致", len(key_details) == 0, key_details))

    # 若 key 不一致，逐条比对无法可靠对齐；按 Tag 建映射比对交集
    base_by_tag = {}
    for t in base_texts:
        base_by_tag.setdefault(tag_of(t), t)

    # 检查项 6 用：按 Tag 提取覆盖包每条 English 的【原始字节】（未解码）。
    # 中文实体 &#x..; 在原始字节里是纯 ASCII；只有真正写入的原始中文字节才 > 0x7F。
    over_eng_raw_by_tag = {}
    for mm in RE_TAG_ENGLISH_RAW.finditer(raw):
        tg = mm.group(1).decode("ascii", "replace").strip()
        over_eng_raw_by_tag.setdefault(tg, mm.group(2))

    # 规则 3/4/5/6：逐条（按 Tag 对齐）
    ph_details = []      # 检查项 3：数值占位符不守恒（FAIL，大小写敏感）
    unknown_details = [] # 检查项 4-FAIL：未知标记
    link_details = []    # 检查项 4-FAIL：LINK 类标记差异
    close_degrade_details = []  # 检查项 4-FAIL：闭合标记退化（[\X] 被吞成裸 [X]）
    warn_details = []    # 检查项 4-WARN：纯排版标记多重集差异（不影响退出码）
    lang_details = []    # 检查项 5：其他语言列被改动（FAIL）
    ascii_details = []   # 检查项 6：改动的 English 内容含非 ASCII（FAIL）
    for ot in over_texts:
        tag = tag_of(ot)
        bt = base_by_tag.get(tag)
        if bt is None:
            continue  # 新增 key 已在规则 2 报出

        o_eng, b_eng = english_content(ot), english_content(bt)

        # 检查项 3：数值占位符守恒（口径 v2：大小写敏感，%d1≠%D1）
        miss, extra = multiset_diff(
            multiset(placeholder_key(x) for x in RE_PLACEHOLDER.findall(b_eng)),
            multiset(placeholder_key(x) for x in RE_PLACEHOLDER.findall(o_eng)))
        if miss or extra:
            ph_details.append("[%s] 数值占位符不守恒(大小写敏感) 缺失=%s 多余=%s" %
                              (tag, dict(miss) or "{}", dict(extra) or "{}"))

        # 检查项 4：方括号标记 —— 口径 v2 分三档
        b_marks = RE_MARKUP.findall(b_eng)
        o_marks = RE_MARKUP.findall(o_eng)
        b_mark_set = set(b_marks)
        # 4-FAIL(a)：覆盖包出现未知标记（既不在合法词表、又不是该条基准原文本就有的标记）
        unknown = sorted({m for m in o_marks if not is_known_markup(m) and m not in b_mark_set})
        if unknown:
            unknown_details.append("[%s] 未知标记(词表外且基准原文无): %s" % (tag, ", ".join(unknown)))
        # 标记多重集差异，拆成 LINK 类 与 纯排版类
        miss, extra = multiset_diff(multiset(b_marks), multiset(o_marks))
        if miss or extra:
            link_miss = {k: v for k, v in miss.items() if is_link_markup(k)}
            link_extra = {k: v for k, v in extra.items() if is_link_markup(k)}
            plain_miss = {k: v for k, v in miss.items() if not is_link_markup(k)}
            plain_extra = {k: v for k, v in extra.items() if not is_link_markup(k)}
            # 4-FAIL(b)：LINK 类【按方向分档】——译文【多出】基准没有的 LINK = FAIL（悬空链接目标风险）
            if link_extra:
                link_details.append("[%s] 译文多出基准没有的 LINK 标记 多余=%s" % (tag, link_extra))
            # 4-WARN(link)：译文【缺失】基准的 LINK = WARN（LINK 剥离的正常产物，显示无损）
            if link_miss:
                warn_details.append("[%s] 译文缺失基准 LINK 标记(剥离正常) 缺失=%s" % (tag, link_miss))
            # 4-FAIL(c)：闭合标记退化签名 —— 某成对族 X 相对基准【缺失 [\X]/[/X]】同时
            #   【多出裸开标记 [X]】。这是闭标记的转义反斜杠/斜杠被吞的特征(如 [\H1]->[H1]、
            #   [\BOLD]->[BOLD]、[/LINK]->[LINK])，会破坏成对结构，非合理排版重排 -> FAIL。
            #   判定用整条(而非仅 miss/extra 差集)的多重集，兼容基准本有多个同名标记的情况。
            b_close = {}
            for m in b_marks:
                n = close_markup_name(m)
                if n:
                    b_close[n] = b_close.get(n, 0) + 1
            o_close = {}
            o_open_bare = {}
            for m in o_marks:
                n = close_markup_name(m)
                if n:
                    o_close[n] = o_close.get(n, 0) + 1
                n2 = open_bare_name(m)
                if n2:
                    o_open_bare[n2] = o_open_bare.get(n2, 0) + 1
            b_open_bare = {}
            for m in b_marks:
                n2 = open_bare_name(m)
                if n2:
                    b_open_bare[n2] = b_open_bare.get(n2, 0) + 1
            for name in PAIRED_MARKUP_NAMES:
                close_lost = b_close.get(name, 0) - o_close.get(name, 0)   # 闭标记减少数
                bare_gained = o_open_bare.get(name, 0) - b_open_bare.get(name, 0)  # 裸开标记增加数
                if close_lost > 0 and bare_gained > 0:
                    close_degrade_details.append(
                        "[%s] 闭合标记退化: [\\%s]/[/%s] 缺失 %d 且多出裸 [%s] %d (转义被吞特征)"
                        % (tag, name, name, close_lost, name, bare_gained))
            # 4-WARN(plain)：纯排版标记差异（合理重排，不判 FAIL）
            if plain_miss or plain_extra:
                warn_details.append("[%s] 排版标记多重集不一致 缺失=%s 多余=%s" %
                                    (tag, plain_miss or "{}", plain_extra or "{}"))

        # 检查项 6：改动的 English 内容纯 ASCII（在【原始字节】层判定）
        #   仅当覆盖包该条 English 解析值与基准不同（= 被翻译/改动过）时才要求纯 ASCII；
        #   判定用原始字节：中文实体 &#x..; 是纯 ASCII（合法），只有直接写入的原始中文字节 >0x7F 才 FAIL。
        #   未改动条目 English 与基准逐字一致，其历史非 ASCII（如 CP1252 \x92）不判错。
        if o_eng != b_eng:
            raw_block = over_eng_raw_by_tag.get(tag, b"")
            bad_bytes = [(i, b) for i, b in enumerate(raw_block) if b > 0x7F]
            if bad_bytes:
                sample = "".join("‹0x%02X@%d›" % (b, i) for i, b in bad_bytes[:5])
                ascii_details.append("[%s] 改动的 English 含原始非 ASCII 字节 %d 处(中文须用 &#x 实体，锚点 A1)：%s"
                                     % (tag, len(bad_bytes), sample))

        # 检查项 5：其他语言列未触碰
        for lang in OTHER_LANGS:
            bk, bv = lang_value(bt, lang)
            ok_, ov = lang_value(ot, lang)
            if bk != ok_ or bv != ov:
                lang_details.append("[%s] %s 列被改动：基准=%r 覆盖包=%r" % (tag, lang, (bk, bv), (ok_, ov)))

    checks.append(("数值占位符守恒", len(ph_details) == 0, ph_details[:30]))
    checks.append(("标记合法", len(unknown_details) == 0, unknown_details[:30]))
    checks.append(("LINK不多出", len(link_details) == 0, link_details[:30]))
    checks.append(("闭合标记未退化", len(close_degrade_details) == 0, close_degrade_details[:30]))
    checks.append(("改动行纯ASCII", len(ascii_details) == 0, ascii_details[:30]))
    checks.append(("其他语言未触碰", len(lang_details) == 0, lang_details[:30]))

    # WARN 单独返回（不进 checks，不影响退出码）—— 仅纯排版标记差异
    warnings = ("排版标记多重集不一致", len(warn_details), warn_details[:30])
    return checks, warnings


# ---------- 报告 ----------
def main(argv):
    root = repo_root()
    over_dir = argv[1] if len(argv) > 1 else os.path.join(root, "MM汉化MOD", "Assets", "XML", "Text")
    base_dir = argv[2] if len(argv) > 2 else os.path.join(root, "MM源码", "Assets", "XML", "Text")

    over_dir = os.path.abspath(over_dir)
    base_dir = os.path.abspath(base_dir)

    over_files = sorted(glob.glob(os.path.join(over_dir, "*.xml")))

    print("=" * 70)
    print("MM 汉化覆盖包静态校验")
    print("  覆盖包: %s" % over_dir)
    print("  基准  : %s" % base_dir)
    print("=" * 70)

    if not over_files:
        print("\n[空] 覆盖包目录下无 .xml 文件，无可校验对象（M3 未产出则属正常）。")
        return 0

    total_fail_files = 0
    total_warn_files = 0
    total_warn_keys = 0
    fail_report = []
    warn_report = []
    for over_path in over_files:
        fname = os.path.basename(over_path)
        base_path = os.path.join(base_dir, fname)
        checks, warnings = validate_file(over_path, base_path)
        failed = [c for c in checks if not c[1]]
        _, warn_count, warn_items = warnings
        has_warn = warn_count > 0
        status = "FAIL" if failed else ("WARN" if has_warn else "PASS")
        marks = " ".join("%s%s" % (("✓" if ok else "✗"), name) for name, ok, _ in checks)
        if has_warn:
            marks += " ⚠标记重排×%d" % warn_count
        print("\n[%s] %s" % (status, fname))
        print("       %s" % marks)
        if failed:
            total_fail_files += 1
            block = ["", "### FAIL 明细: %s" % fname]
            for name, ok, details in failed:
                block.append("  ✗ %s:" % name)
                for d in details:
                    block.append("      - %s" % d)
            fail_report.append("\n".join(block))
        if has_warn:
            total_warn_files += 1
            total_warn_keys += warn_count
            block = ["", "### WARN 明细: %s（标记多重集不一致 %d 条，已知合法词表内的排版重排，不判 FAIL）" % (fname, warn_count)]
            for d in warn_items:
                block.append("      ~ %s" % d)
            if warn_count > len(warn_items):
                block.append("      ~ …（其余 %d 条略）" % (warn_count - len(warn_items)))
            warn_report.append("\n".join(block))

    print("\n" + "=" * 70)
    print("汇总：共 %d 文件 | PASS %d | FAIL %d | 含 WARN %d 文件(标记重排 %d 条)" %
          (len(over_files), len(over_files) - total_fail_files, total_fail_files,
           total_warn_files, total_warn_keys))
    print("=" * 70)

    if fail_report:
        print("\n########## FAIL 明细 ##########")
        print("\n".join(fail_report))
    if warn_report:
        print("\n########## WARN 明细 ##########")
        print("\n".join(warn_report))

    return min(total_fail_files, 100)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
