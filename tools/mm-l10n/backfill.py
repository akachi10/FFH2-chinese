#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MM 汉化回填工具 (Sprint mm-localization / M3)

把官方 FFH2 简体汉化包的现成译文,逐 key 比对英文原文后,回填进 MM 汉化覆盖包的文本 XML。

严格遵循技术路线硬锚点:
  A1 中文写入 <English> 列,数字实体形式 (&#x....;),输出字节纯 ASCII,保持 MM 原文件 XML 声明不变
  A2 简体中文(官方包已确认为简体)
  A5 结构守恒:仅替换被回填条目的 English 文本内容,其余(key/其他语言列/Gender/Plural/
     注释/占位符)逐字节保持原样。用文本级精准替换,不做 XML 库整体重序列化
  A8 逐 key 比对:官方包某 key 的英文原文(规范化空白后)与 MM 同 key 的英文完全一致才回填;
     不一致进"待翻译"清单
  A9 保守优先:数值占位符 %sN/%dN 大小写不敏感的多重集必须守恒,否则跳过入待翻译
     ([ICON]/[LINK]/[COLOR]/[NEWLINE] 等标记:中文可多可等,不做硬校验——不报错即可)

用法:
  python3 backfill.py            # 执行回填,生成 111 个覆盖文件 + 回填报告
  python3 backfill.py --verify   # 仅跑自验(需已生成覆盖文件)

标准库实现,无第三方依赖。
"""

import os
import re
import sys
import html
import random
from collections import Counter, OrderedDict

# ---- 路径 ----
REPO = "/Users/taoyawei/IdeaProjects/ffh2-mods-ba"
OFFICIAL_DIR = ("/private/tmp/claude-501/-Users-taoyawei-IdeaProjects-ffh2-mods-ba/"
                "c58d8cd1-76f7-4738-9d91-9164834a6cc1/scratchpad/ch041o/Text")
MM_SRC_DIR = os.path.join(REPO, "MM源码/Assets/XML/Text")
OUT_DIR = os.path.join(REPO, "MM汉化MOD/Assets/XML/Text")
REPORT_PATH = os.path.join(REPO, "docs/mm-localization/回填报告.md")

# 官方包源文件以 latin-1 逐字节读入即可:中文本就是 ASCII 数字实体,声明的 GB2312 与实体无关
ENC = "latin-1"

# ---- 正则 ----
TEXT_BLOCK = re.compile(r'<TEXT>(.*?)</TEXT>', re.S)
TAG_RE = re.compile(r'<Tag>(.*?)</Tag>', re.S)
ENGLISH_RE = re.compile(r'<English>(.*?)</English>', re.S)
CHINESE_RE = re.compile(r'<Chinese>(.*?)</Chinese>', re.S)
INNER_TEXT_RE = re.compile(r'(<Text>)(.*?)(</Text>)', re.S)
# 数值占位符 · 大小写对齐用:仅带序号的 %d1 %s2 及裸 %s %d %f 等格式符(用于把译文改回基准大小写)
NUM_PH_RE = re.compile(r'%[0-9.]*[sdfSDF]\d*')

# 占位符守恒校验用(与 M4 validate.py 同口径):%后跟字母数字下划线段。
# 覆盖 %HP 之类的歧义百分号,大小写不敏感多重集守恒,不等即跳过入待翻译。
PH_CHECK_RE = re.compile(r'%[A-Za-z0-9_]+')

# 方括号标记(与 M4 同口径)
MARKUP_RE = re.compile(r'\[[^\[\]]*\]')
# 合法标记词表(与 M4 validate.py KNOWN_MARKUP_PATTERNS 对齐):命中任一即合法。
# 译文中出现「不命中词表 且 基准英文原文也没有」的方括号标记 = 未知标记 -> 跳过入待翻译。
KNOWN_MARKUP_PATTERNS = [re.compile(p) for p in (
    r"^\[NEWLINE\]$", r"^\[TAB\]$", r"^\[SPACE\]$",
    r"^\[PARAGRAPH(:\d+)?\]$",
    r"^\[COLOR_[A-Z0-9_]+\]$",
    r"^\[ICON_[A-Z0-9_]+\]$",
    r"^\[LINK=[^\[\]]*\]$", r"^\[\\LINK\]$", r"^\[/LINK\]$",
    r"^\[BOLD\]$", r"^\[\\BOLD\]$",
    r"^\[H[12]\]$", r"^\[\\H[12]\]$",
    r"^\[(CT_[A-Z_]+|OUR_[A-Z_]+)(:\d+|\.\d+)?\]$",
    r"^\[NUM\d+:[^\[\]]*\]$",
    r"^\[[sdf]\d*(_[a-z_]+)?\]$",
    r"^\[[sdf]\d*:\d+_[a-z_]+\]$",
)]


def is_known_markup(tok):
    return any(p.match(tok) for p in KNOWN_MARKUP_PATTERNS)


def unknown_markups(chi_text, base_english):
    """译文中出现、既不在合法词表又不在基准英文原文里的方括号标记集合。"""
    base_marks = set(MARKUP_RE.findall(base_english))
    return sorted({m for m in MARKUP_RE.findall(chi_text)
                   if not is_known_markup(m) and m not in base_marks})


# LINK 类标记(与 M4 validate.py RE_LINK_MARKUP 同口径)
LINK_MARKUP_RE = re.compile(r'\[(?:LINK=[^\[\]]*|\\LINK|/LINK)\]')


def link_multiset(s):
    """LINK 类标记多重集(整字符串比较,与 M4 LINK 守恒口径一致)。"""
    return Counter(LINK_MARKUP_RE.findall(s))


def decode_entities(s):
    """把 XML 数字实体解码回真实字符 (&#x6253; / &#25171; -> 字符)。"""
    s = re.sub(r'&#x([0-9A-Fa-f]+);', lambda m: chr(int(m.group(1), 16)), s)
    s = re.sub(r'&#(\d+);', lambda m: chr(int(m.group(1))), s)
    return s


def norm_en(s):
    """英文比对用规范化:解码实体+反转义 XML 命名实体+折叠空白。"""
    return re.sub(r'\s+', ' ', html.unescape(decode_entities(s))).strip()


def num_ph_multiset(s):
    """占位符多重集,大小写归一(与 M4 同口径:%后字母数字下划线段)。

    用于守恒校验:检出 %HP 等歧义百分号、以及真丢失/新增的数值占位符。
    """
    return Counter(p.lower() for p in PH_CHECK_RE.findall(s))


# [LINK=...] 起始标记 与 [\LINK] / [/LINK] 结束标记(两种写法都见于官方译文)
LINK_OPEN_RE = re.compile(r'\[LINK=[^\]]*\]')
LINK_CLOSE_RE = re.compile(r'\[[\\/]LINK\]')
# 一个完整 LINK 段:[LINK=X] 内容 [\LINK]/[/LINK](内容非贪婪,不跨越下一个开标记)
LINK_SEGMENT_RE = re.compile(r'(\[LINK=[^\]]*\])(.*?)(\[[\\/]LINK\])', re.S)


def strip_links(s, base_english):
    """条件剥离译文中的 LINK 标记对,保留内部文字(M3.1,已按 M4 新校验修正)。

    规则(区分两种 LINK,兼顾 A5 与 A9):
    - **基准英文本身就含**的同名 `[LINK=X]`:官方译文照搬,链接目标在 MM 中存在、非悬空
      -> **整段保留**(A5 标记原样,满足 M4「LINK 标记守恒」校验)。
    - **基准英文没有、官方译者额外加**的 `[LINK=Y]`:目标可能在 MM 中不存在,悬空链接
      有不确定性 -> **删开闭标记,保留内部文字**(A9 零风险)。

    实现:按 LINK 段处理,段内 open 标记在基准英文里出现则整段保留,否则去标记留文字。
    残留的孤立(未配对)LINK 标记:open 在基准中存在则留,否则删。
    """
    base_opens = set(LINK_OPEN_RE.findall(base_english))

    def seg_repl(m):
        open_tag, inner, close_tag = m.group(1), m.group(2), m.group(3)
        if open_tag in base_opens:
            return open_tag + inner + close_tag   # 基准也有 -> 整段保留
        return inner                              # 额外加的 -> 去标记留文字

    s = LINK_SEGMENT_RE.sub(seg_repl, s)
    # 清理残留的孤立开标记(基准无者删,基准有者保留)
    s = LINK_OPEN_RE.sub(lambda m: m.group(0) if m.group(0) in base_opens else '', s)
    # 残留孤立闭标记:仅当基准英文也有闭标记时保留,否则删
    base_has_close = bool(LINK_CLOSE_RE.search(base_english))
    if not base_has_close:
        s = LINK_CLOSE_RE.sub('', s)
    return s


def align_placeholder_case(text, ref_english):
    """把 text 中的数值占位符逐个改写为基准 English 的精确大小写形式(M3.1)。

    做法:按出现顺序,以「小写归一后的占位符」为键,查基准 English 中同键占位符的
    原始大小写,替换 text 中对应出现。基准同键有多种大小写时按出现顺序配对。
    要求调用前已确认二者大小写归一多重集相等,故按序一一对应必然可配。
    """
    ref_by_key = {}
    for m in NUM_PH_RE.finditer(ref_english):
        ref_by_key.setdefault(m.group(0).lower(), []).append(m.group(0))
    cursor = {}

    def repl(m):
        key = m.group(0).lower()
        lst = ref_by_key.get(key)
        if not lst:
            return m.group(0)
        i = cursor.get(key, 0)
        val = lst[i] if i < len(lst) else lst[-1]
        cursor[key] = i + 1
        return val

    return NUM_PH_RE.sub(repl, text)


def to_entities(text):
    """把真实中文文本编码为 XML 数字实体形式,保证输出纯 ASCII。

    - 非 ASCII 字符 -> &#xXXXX;
    - '&' 若非既有实体的一部分,转 &amp; (中文译文中一般已无裸 & 需要保护占位符/标记原样)
    ASCII 可打印字符(含 [ICON_*] %s1 等标记/占位符)原样保留。
    """
    out = []
    for ch in text:
        o = ord(ch)
        if o < 128:
            out.append(ch)
        else:
            out.append('&#x%x;' % o)
    return ''.join(out)


def load_official():
    """加载官方汉化包 -> OrderedDict[key] = (norm_english, chinese_text_decoded)。

    chinese_text_decoded 为解码后的真实中文串(未做实体化);为空/占位则值为 None。
    """
    off = OrderedDict()
    for fn in sorted(os.listdir(OFFICIAL_DIR)):
        if not fn.lower().endswith(".xml"):
            continue
        raw = open(os.path.join(OFFICIAL_DIR, fn), "rb").read().decode(ENC)
        for bm in TEXT_BLOCK.finditer(raw):
            blk = bm.group(1)
            t = TAG_RE.search(blk)
            e = ENGLISH_RE.search(blk)
            c = CHINESE_RE.search(blk)
            if not t or not e:
                continue
            key = t.group(1).strip()
            eng_norm = norm_en(e.group(1))
            chi = None
            if c is not None:
                decoded = decode_entities(c.group(1))
                if decoded.strip() != "":
                    chi = decoded
            off[key] = (eng_norm, chi)
    return off


def split_english_content(english_inner):
    """把 <English> 元素内部内容拆成 (是否嵌套Text, 用于比对的英文串)。

    MM 中部分 English 为 <English><Text>..</Text><Gender>..</Gender></English> 形态。
    回填时仅替换内层 <Text> 内容,Gender/Plural 保留。
    """
    tm = INNER_TEXT_RE.search(english_inner)
    if tm:
        return True, tm.group(2)
    return False, english_inner


def backfill():
    off = load_official()

    stats = OrderedDict()      # 每文件统计
    total = Counter()
    verify_samples = []        # (key, chinese_decoded, entity_written) 供自验抽样
    pending = []               # 待翻译清单条目 (file, key, reason)

    for fn in sorted(os.listdir(MM_SRC_DIR)):
        if not fn.lower().endswith(".xml"):
            continue
        src_path = os.path.join(MM_SRC_DIR, fn)
        raw = open(src_path, "rb").read().decode(ENC)

        fstat = Counter()

        def repl_block(bm):
            blk = bm.group(1)
            t = TAG_RE.search(blk)
            em = ENGLISH_RE.search(blk)
            if not t or not em:
                fstat['no_key'] += 1
                return bm.group(0)
            key = t.group(1).strip()
            fstat['keys'] += 1
            english_inner = em.group(1)
            nested, eng_for_cmp = split_english_content(english_inner)

            if key not in off:
                fstat['mm_only'] += 1
                pending.append((fn, key, "MM-only"))
                return bm.group(0)

            oeng, ochi = off[key]
            if ochi is None:
                fstat['no_translation'] += 1
                pending.append((fn, key, "official-no-chinese"))
                return bm.group(0)
            if norm_en(eng_for_cmp) != oeng:
                fstat['eng_changed'] += 1
                pending.append((fn, key, "eng-changed-by-MM"))
                return bm.group(0)
            # 官方译文未译:<Chinese> 列内容规范化后等于英文原文(译者仅把英文复制进中文列)。
            # 回填等于保留英文,应计入待翻译而非虚增回填数(不影响运行,只为统计准确)。
            if norm_en(ochi) == oeng:
                fstat['official_untranslated'] += 1
                pending.append((fn, key, "official-untranslated"))
                return bm.group(0)

            # M3.1-步骤2: 条件剥离 LINK。基准英文也有的 LINK 整段保留(A5,非悬空);
            #             仅剥基准没有、官方译者额外加的 LINK(A9,可能悬空)。
            chi_text = strip_links(ochi, eng_for_cmp)

            # M3.1-步骤1: 数值占位符大小写不敏感多重集守恒;若归一后仍不等(如多出 %HP)
            #             -> 跳过入待翻译
            if num_ph_multiset(eng_for_cmp) != num_ph_multiset(chi_text):
                fstat['ph_mismatch'] += 1
                pending.append((fn, key, "numeric-placeholder-mismatch"))
                return bm.group(0)
            # M3.1: 未知标记守恒。剥离 LINK 后,若译文仍含既不在合法词表、基准英文也没有的
            #        方括号标记(如官方旧写法 [HAPPY_ICON],MM 已改用 [ICON_HAPPY])
            #        -> 引擎不识别会字面显示,文不对题,跳过入待翻译。
            unk = unknown_markups(chi_text, eng_for_cmp)
            if unk:
                fstat['markup_unknown'] += 1
                pending.append((fn, key, "unknown-markup:" + ",".join(unk)))
                return bm.group(0)
            # M3.1: LINK 类标记守恒(A5,与 M4 同口径)。条件剥离后,译文的 LINK 标记多重集
            #        必须与基准英文一致——不一致者(如官方译文把基准的 [LINK=X] 丢弃/换成别的
            #        目标)强行回填会破坏基准 LINK 结构,跳过入待翻译。
            if link_multiset(chi_text) != link_multiset(eng_for_cmp):
                fstat['link_mismatch'] += 1
                pending.append((fn, key, "link-markup-mismatch"))
                return bm.group(0)

            # 通过 -> 把译文数值占位符逐个改写为 MM 基准 English 的精确大小写
            chi_text = align_placeholder_case(chi_text, eng_for_cmp)

            # 通过全部判据 -> 回填
            ochi = chi_text
            entity = to_entities(ochi)
            if nested:
                # 仅替换内层 <Text> 内容,其余(Gender/Plural)原样
                new_inner = INNER_TEXT_RE.sub(
                    lambda m: m.group(1) + entity + m.group(3), english_inner, count=1)
            else:
                new_inner = entity
            new_english = '<English>' + new_inner + '</English>'
            new_blk = blk[:em.start()] + new_english + blk[em.end():]
            fstat['backfilled'] += 1
            verify_samples.append((key, ochi, entity, fn))
            return '<TEXT>' + new_blk + '</TEXT>'

        new_raw = TEXT_BLOCK.sub(repl_block, raw)

        # 写出(纯 ASCII,latin-1 编码等价于原字节;实体保证无 >127 字符)
        out_path = os.path.join(OUT_DIR, fn)
        with open(out_path, "wb") as w:
            w.write(new_raw.encode(ENC))

        stats[fn] = fstat
        for k, v in fstat.items():
            total[k] += v

    return stats, total, verify_samples, pending


# ---------------- 自验 ----------------

def self_verify(verify_samples, pending, stats, total):
    import xml.etree.ElementTree as ET
    print("\n===== 自验 =====")
    ok = True

    # 1. 随机抽 20 个回填条目:实体解码后与官方译文一致 + 数值占位符集合与英文一致
    off = load_official()
    sample = random.sample(verify_samples, min(20, len(verify_samples)))
    bad = 0
    for key, ochi, entity, fn in sample:
        decoded_back = decode_entities(entity)
        if decoded_back != ochi:
            bad += 1
            print("  [FAIL] 实体回解码不一致:", key)
        oeng = off[key][0]
        if num_ph_multiset(oeng) != num_ph_multiset(ochi):
            bad += 1
            print("  [FAIL] 数值占位符不一致:", key)
    print("[1] 抽样20条实体解码+占位符一致: %s (%d/%d 通过)" %
          ("OK" if bad == 0 else "FAIL", len(sample) - bad, len(sample)))
    ok = ok and bad == 0

    # 2. 全部输出文件可被 xml.etree 解析
    parse_fail = []
    n_files = 0
    for fn in sorted(os.listdir(OUT_DIR)):
        if not fn.lower().endswith(".xml"):
            continue
        n_files += 1
        try:
            ET.parse(os.path.join(OUT_DIR, fn))
        except Exception as e:
            parse_fail.append((fn, str(e)))
    print("[2] %d 个输出文件 xml.etree 解析: %s" %
          (n_files, "全部OK" if not parse_fail else "FAIL"))
    for fn, e in parse_fail[:10]:
        print("      [FAIL]", fn, e)
    ok = ok and not parse_fail

    # 3. diff:改动行只出现在被回填条目的 English 行
    #    比对每个输出文件与 MM 原文件,逐块检查:凡内容变化的块,其变化必须落在 <English>...</English>
    diff_bad = []
    for fn in sorted(os.listdir(OUT_DIR)):
        if not fn.lower().endswith(".xml"):
            continue
        src = open(os.path.join(MM_SRC_DIR, fn), "rb").read().decode(ENC)
        out = open(os.path.join(OUT_DIR, fn), "rb").read().decode(ENC)
        src_blocks = TEXT_BLOCK.findall(src)
        out_blocks = TEXT_BLOCK.findall(out)
        # 块外内容必须完全一致
        if TEXT_BLOCK.sub('<TEXT/>', src) != TEXT_BLOCK.sub('<TEXT/>', out):
            diff_bad.append((fn, "块外字节发生变化"))
            continue
        if len(src_blocks) != len(out_blocks):
            diff_bad.append((fn, "TEXT 块数变化"))
            continue
        for sb, ob in zip(src_blocks, out_blocks):
            if sb == ob:
                continue
            # 变化的块:把两侧 English 元素抠掉后必须完全相同
            sb2 = ENGLISH_RE.sub('<English/>', sb)
            ob2 = ENGLISH_RE.sub('<English/>', ob)
            if sb2 != ob2:
                diff_bad.append((fn, "非 English 内容变化"))
                break
    print("[3] diff 改动仅落在 English 内容: %s" %
          ("OK" if not diff_bad else "FAIL"))
    for fn, e in diff_bad[:10]:
        print("      [FAIL]", fn, e)
    ok = ok and not diff_bad

    # 4. 统计数自洽
    keys = total['keys']
    accounted = (total['backfilled'] + total['mm_only'] + total['eng_changed']
                 + total['no_translation'] + total['ph_mismatch']
                 + total['markup_unknown'] + total['link_mismatch']
                 + total['official_untranslated'])
    print("[4] 统计自洽: keys=%d = backfilled+mm_only+eng_changed+no_tr+ph_mismatch"
          "+markup_unknown+link_mismatch+official_untranslated=%d : %s"
          % (keys, accounted, "OK" if keys == accounted else "FAIL"))
    ok = ok and keys == accounted

    print("\n自验总结: %s" % ("全部通过 ✅" if ok else "存在失败 ❌"))
    return ok


# ---------------- 报告 ----------------

def write_report(stats, total, pending):
    lines = []
    A = lines.append
    A("# MM 汉化回填报告")
    A("")
    A("工具:`tools/mm-l10n/backfill.py`  ·  基准:`MM源码/Assets/XML/Text/`(只读)  ·  "
      "官方译文:0.41o 简体汉化包(gb2312 变体,已确认简体)")
    A("")
    A("回填策略(遵循硬锚点 A1/A2/A5/A8/A9):中文写入 `<English>` 列、数字实体形式、"
      "文件字节纯 ASCII、保持 MM 原声明;逐 key 比对英文原文一致才回填。")
    A("")
    A("### A8 英文比对规范化规则")
    A("")
    A("**仅空白归一,其余(含方括号标记、大小写、占位符)精确比较。** 具体:解码 XML 数字/命名"
      "实体 → 折叠连续空白为单空格 → 去首尾空白;不做大小写折叠、不剥标记。此为收紧后的口径"
      "(与 M4 一致),确保 MM 改写过英文的 key 不会因大小写/标记差异被误判为一致而盲目复用。")
    A("")
    A("### M3.1 修正(占位符大小写对齐 + LINK 剥离 + 未知标记守恒)")
    A("")
    A("1. **数值占位符大小写对齐**:比对按大小写不敏感;通过后把译文数值占位符逐个改写为 "
      "MM 基准 English 的精确大小写(`%D1`→`%d1` 等)。归一后多重集仍不等(如多出 `%HP`)→"
      "跳过入待翻译。")
    A("2. **条件剥离 `[LINK=...]`/`[\\LINK]` 标记对**(区分两种 LINK,兼顾 A5 与 A9):"
      "**基准英文本身就含**的同名 `[LINK=X]`(官方译文照搬,目标在 MM 中存在、非悬空)→ "
      "整段保留(满足 M4「LINK 标记守恒」校验);**基准英文没有、官方译者额外加**的 `[LINK=Y]`"
      "(目标可能悬空)→ 删标记留内部文字(A9 零风险)。")
    A("3. **未知标记守恒**:剥 LINK 后,译文若仍含既不在合法词表、基准英文原文也没有的方括号"
      "标记(如官方旧写法 `[HAPPY_ICON]`,MM 已改用 `[ICON_HAPPY]`)→ 引擎不识别会字面显示,"
      "文不对题,跳过入待翻译。")
    A("3b. **LINK 标记守恒**(A5,与 M4「LINK标记守恒」同口径):条件剥离后,译文的 LINK 类"
      "标记多重集必须与基准英文一致。若官方译文把基准英文本有的 `[LINK=X]` 丢弃(改用颜色"
      "高亮)或换成别的目标,导致译文 LINK 集合 ≠ 基准 → 强行回填会破坏基准 LINK 结构,"
      "跳过入待翻译。")
    A("4. **纯排版标记差异**(`[NEWLINE]`/`[TAB]`/`[PARAGRAPH:N]`/`[COLOR_*]`/`[BOLD]`/"
      "`[ICON_*]`)保留原样,不做处理。")
    A("5. **官方译文未译**:官方包部分条目 `<Chinese>` 列内容规范化后等于英文原文(译者仅把"
      "英文复制进中文列)。回填等于保留英文,归入待翻译而非虚增回填数(不影响运行,只为统计准确)。")
    A("")
    A("## 总量")
    A("")
    A("| 分类 | 数量 |")
    A("|------|------|")
    A("| MM 总 key 数 | %d |" % total['keys'])
    A("| **回填数**(复用官方译文) | **%d** |" % total['backfilled'])
    A("| 跳过 · 英文被 MM 改过 | %d |" % total['eng_changed'])
    A("| 跳过 · 数值占位符不守恒 | %d |" % total['ph_mismatch'])
    A("| 跳过 · 未知标记(基准无且词表外) | %d |" % total['markup_unknown'])
    A("| 跳过 · LINK 标记不守恒(译文丢/换基准的 LINK) | %d |" % total['link_mismatch'])
    A("| 跳过 · 官方译文未译(中文列=英文原文) | %d |" % total['official_untranslated'])
    A("| 跳过 · 官方包无中文 | %d |" % total['no_translation'])
    A("| MM 独有(官方包无此 key) | %d |" % total['mm_only'])
    A("")
    待翻译 = (total['eng_changed'] + total['ph_mismatch'] + total['markup_unknown']
              + total['link_mismatch'] + total['official_untranslated']
              + total['no_translation'] + total['mm_only'])
    A("**待翻译合计 = %d**(= 英文改过 %d + 占位符不守恒 %d + 未知标记 %d + LINK不守恒 %d + "
      "官方未译 %d + 无中文 %d + MM 独有 %d)"
      % (待翻译, total['eng_changed'], total['ph_mismatch'], total['markup_unknown'],
         total['link_mismatch'], total['official_untranslated'],
         total['no_translation'], total['mm_only']))
    A("")

    # 待翻译词量估计:英文按空白分词
    def count_words_of_pending():
        # 重新扫描 MM,取 pending 的英文词数
        pend_keys = {}
        for fn, key, reason in pending:
            pend_keys.setdefault(fn, set()).add(key)
        words = 0
        for fn in sorted(pend_keys):
            raw = open(os.path.join(MM_SRC_DIR, fn), "rb").read().decode(ENC)
            for bm in TEXT_BLOCK.finditer(raw):
                blk = bm.group(1)
                t = TAG_RE.search(blk)
                em = ENGLISH_RE.search(blk)
                if not t or not em:
                    continue
                if t.group(1).strip() in pend_keys[fn]:
                    _, eng = split_english_content(em.group(1))
                    # 去标记后计词
                    clean = re.sub(r'\[[^\]]*\]|%[0-9.]*[sdfSDF]\d*', ' ',
                                   html.unescape(decode_entities(eng)))
                    words += len([w for w in clean.split() if w])
        return words

    est_words = count_words_of_pending()
    A("## 待翻译词量估计")
    A("")
    A("待翻译条目英文原文按空白分词(已剔除 `[标记]`/`%%占位符`)约 **%d 词**。" % est_words)
    A("")

    A("## 按文件分列")
    A("")
    A("| 文件 | key 数 | 回填 | 英文改过 | 占位符不守恒 | 未知标记 | LINK不守恒 | 官方未译 | MM独有 |")
    A("|------|-------|------|---------|------------|--------|----------|--------|--------|")
    for fn in sorted(stats):
        s = stats[fn]
        A("| %s | %d | %d | %d | %d | %d | %d | %d | %d |" %
          (fn, s['keys'], s['backfilled'], s['eng_changed'],
           s['ph_mismatch'], s['markup_unknown'], s['link_mismatch'],
           s['official_untranslated'], s['mm_only']))
    A("")

    # Top10 回填 / Top10 待翻译
    top_bf = sorted(stats.items(), key=lambda kv: kv[1]['backfilled'], reverse=True)[:10]
    A("## Top10 回填最多的文件")
    A("")
    A("| 文件 | 回填数 |")
    A("|------|-------|")
    for fn, s in top_bf:
        A("| %s | %d |" % (fn, s['backfilled']))
    A("")
    def pend_of(s):
        return (s['mm_only'] + s['eng_changed'] + s['ph_mismatch']
                + s['markup_unknown'] + s['link_mismatch']
                + s['official_untranslated'] + s['no_translation'])
    top_pending = sorted(stats.items(), key=lambda kv: pend_of(kv[1]), reverse=True)[:10]
    A("## Top10 待翻译最多的文件")
    A("")
    A("| 文件 | 待翻译数 |")
    A("|------|--------|")
    for fn, s in top_pending:
        A("| %s | %d |" % (fn, pend_of(s)))
    A("")

    # 待翻译 key 清单(单独区块,供 M6 使用)
    A("## 待翻译 key 清单(节选,前 100 条)")
    A("")
    A("完整清单见工具重跑输出;此处列前 100 条,格式 `文件 · key · 原因`。")
    A("")
    for fn, key, reason in pending[:100]:
        A("- `%s` · `%s` · %s" % (fn, key, reason))
    A("")

    os.makedirs(os.path.dirname(REPORT_PATH), exist_ok=True)
    with open(REPORT_PATH, "w", encoding="utf-8") as w:
        w.write("\n".join(lines))
    print("报告已写入:", REPORT_PATH)


def main():
    if "--verify" in sys.argv:
        # 仅自验:需要重新计算 samples/stats -> 直接跑一遍回填(幂等)
        pass
    print("加载官方译文 ...")
    stats, total, verify_samples, pending = backfill()
    print("回填完成:%d 文件,%d key,回填 %d,英文改过 %d,占位符不守恒 %d,未知标记 %d,LINK不守恒 %d,官方未译 %d,无中文 %d,MM独有 %d"
          % (len(stats), total['keys'], total['backfilled'], total['eng_changed'],
             total['ph_mismatch'], total['markup_unknown'], total['link_mismatch'],
             total['official_untranslated'], total['no_translation'], total['mm_only']))
    ok = self_verify(verify_samples, pending, stats, total)
    write_report(stats, total, pending)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
