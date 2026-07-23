#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
M6.0 翻译流水线 · 批次生成工具

扫描覆盖包(MM汉化MOD) vs 基准(MM源码),找出「English 列与基准逐字节相同且含字母单词」
的条目 = 待翻译,按规模切分成批次 TSV 骨架,供人工/AI 逐批填中文,再由
apply_translations.py 安全注入。

判定口径(与 backfill.py / M4 validate.py 一致):
  - 待翻译候选:覆盖包该 key 的 English 内容(结构化则取内层 <Text>)与基准 English 逐字节相同
    (= M3 回填时未被替换,仍是英文)。
  - 含字母单词:剥掉方括号标记([...])与 %占位符 后仍含 ASCII 字母 -> 进批次;
    否则(纯符号/数字/纯标记)-> 标 AUTO-SKIP,不进批次(无需翻译)。

切分规则:
  - 批内保持文件聚集(同文件的 key 连续),按 ~MAX_KEYS 或 ~MAX_WORDS 触发切批;
  - 大文件按 key 出现顺序区间拆多批。

输出:
  - tools/mm-l10n/batches/batch-NN.tsv  (UTF-8, TAB 分隔, 列: file  key  english  chinese)
    english 列的字面制表符/换行转义为 \\t / \\n(apply 时还原);chinese 列留空待填。
  - tools/mm-l10n/batches/INDEX.md      (每批:文件范围、key 数、英文词数;及 AUTO-SKIP 统计)

复用 backfill.py 的解析/规则函数,避免重复实现。标准库实现。
"""

import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import backfill as B  # 复用正则与规则函数

BATCH_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "batches")

# 切批阈值
MAX_KEYS = 700          # 每批 key 上限(~600-800)
MAX_WORDS = 12000       # 每批英文词上限(~1.2 万)

# 剥标记/占位符后判字母用
STRIP_MARKUP_PH = re.compile(r'\[[^\[\]]*\]|%[A-Za-z0-9_.]+')
HAS_LETTER = re.compile(r'[A-Za-z]')


def tsv_escape(s):
    """english 列写入 TSV 前转义:制表符/回车/换行 -> 字面 \\t \\r \\n。"""
    return s.replace('\\', '\\\\').replace('\t', '\\t').replace('\r', '\\r').replace('\n', '\\n')


def english_word_count(english):
    """英文词数:剥掉标记与占位符后按空白分词。"""
    clean = STRIP_MARKUP_PH.sub(' ', B.decode_entities(english))
    return len([w for w in clean.split() if w])


def has_translatable_letters(english):
    """剥掉方括号标记与 %占位符后是否仍含 ASCII 字母。"""
    clean = STRIP_MARKUP_PH.sub(' ', B.decode_entities(english))
    return bool(HAS_LETTER.search(clean))


def collect_pending():
    """遍历覆盖包 vs 基准,返回 (pending_list, auto_skip_count, missing_count)。

    pending_list: [(file, key, english_raw)] —— english_raw 为覆盖包内 English 原始文本
                  (结构化取内层 <Text>),保持字节原样供 TSV。
    auto_skip:    English 与基准相同但无字母单词(纯符号/数字/标记)的条目数。
    """
    pending = []
    auto_skip = 0

    for fn in sorted(os.listdir(B.OUT_DIR)):
        if not fn.lower().endswith(".xml"):
            continue
        over_path = os.path.join(B.OUT_DIR, fn)
        base_path = os.path.join(B.MM_SRC_DIR, fn)
        if not os.path.exists(base_path):
            continue
        over_raw = open(over_path, "rb").read().decode(B.ENC)
        base_raw = open(base_path, "rb").read().decode(B.ENC)

        # 基准按 key -> English 内容
        base_eng = {}
        for bm in B.TEXT_BLOCK.finditer(base_raw):
            blk = bm.group(1)
            t = B.TAG_RE.search(blk)
            em = B.ENGLISH_RE.search(blk)
            if not t or not em:
                continue
            _, eng = B.split_english_content(em.group(1))
            base_eng[t.group(1).strip()] = eng

        for om in B.TEXT_BLOCK.finditer(over_raw):
            blk = om.group(1)
            t = B.TAG_RE.search(blk)
            em = B.ENGLISH_RE.search(blk)
            if not t or not em:
                continue
            key = t.group(1).strip()
            _, over_eng = B.split_english_content(em.group(1))
            base = base_eng.get(key)
            if base is None:
                continue  # 覆盖包新增 key(理论上不该有);跳过
            # English 与基准逐字节相同 = 未翻译
            if over_eng != base:
                continue
            if has_translatable_letters(over_eng):
                pending.append((fn, key, over_eng))
            else:
                auto_skip += 1

    return pending, auto_skip


def split_batches(pending):
    """按 key/词阈值切批,批内文件聚集。返回 [ [ (file,key,eng), ... ], ... ]。

    pending 已按文件、文件内 key 出现顺序排列(collect 保序),故批内天然文件聚集
    (同文件 key 连续)。小文件可合入同一批;大文件超阈值时按 key 出现顺序拆多批。
    仅在 key 数或累计词数达阈值时换批,不因换文件强制换批(避免批数过碎)。
    """
    batches = []
    cur = []
    cur_keys = 0
    cur_words = 0

    for fn, key, eng in pending:
        w = english_word_count(eng)
        need_break = cur and (
            cur_keys >= MAX_KEYS or
            cur_words + w > MAX_WORDS
        )
        if need_break:
            batches.append(cur)
            cur = []
            cur_keys = 0
            cur_words = 0
        cur.append((fn, key, eng))
        cur_keys += 1
        cur_words += w

    if cur:
        batches.append(cur)
    return batches


def write_batches(batches, auto_skip):
    os.makedirs(BATCH_DIR, exist_ok=True)
    # 清理旧批次(仅 batch-*.tsv),避免残留
    for old in os.listdir(BATCH_DIR):
        if re.match(r'batch-\d+\.tsv$', old):
            os.remove(os.path.join(BATCH_DIR, old))

    index_rows = []
    total_keys = 0
    total_words = 0
    for i, batch in enumerate(batches, 1):
        name = "batch-%02d.tsv" % i
        path = os.path.join(BATCH_DIR, name)
        with open(path, "w", encoding="utf-8") as w:
            w.write("file\tkey\tenglish\tchinese\n")
            for fn, key, eng in batch:
                w.write("%s\t%s\t%s\t\n" % (fn, key, tsv_escape(eng)))
        files = sorted({b[0] for b in batch})
        keys = len(batch)
        words = sum(english_word_count(b[2]) for b in batch)
        total_keys += keys
        total_words += words
        file_range = files[0] if len(files) == 1 else "%s … %s (%d 文件)" % (files[0], files[-1], len(files))
        index_rows.append((name, file_range, keys, words))

    # INDEX.md
    lines = []
    A = lines.append
    A("# 翻译批次索引")
    A("")
    A("由 `tools/mm-l10n/make_batches.py` 生成。每批为待翻译条目骨架 TSV(UTF-8,TAB 分隔,"
      "列 `file / key / english / chinese`),填好 `chinese` 列后由 `apply_translations.py` 注入。")
    A("")
    A("- **批次总数**:%d" % len(batches))
    A("- **待翻译条目合计**:%d key" % total_keys)
    A("- **英文词量合计**(剔除标记/占位符):约 %d 词" % total_words)
    A("- **AUTO-SKIP**(English 与基准相同但无字母单词,纯符号/数字/标记,无需翻译):%d 条" % auto_skip)
    A("")
    A("切批阈值:每批 ≤ %d key 或 ≤ %d 英文词。批内文件聚集(同文件 key 连续排列,小文件可合批,"
      "大文件按 key 区间拆多批)。" % (MAX_KEYS, MAX_WORDS))
    A("")
    A("| 批次 | 文件范围 | key 数 | 英文词数 |")
    A("|------|---------|-------|---------|")
    for name, file_range, keys, words in index_rows:
        A("| %s | %s | %d | %d |" % (name, file_range, keys, words))
    A("")
    with open(os.path.join(BATCH_DIR, "INDEX.md"), "w", encoding="utf-8") as w:
        w.write("\n".join(lines))

    return total_keys, total_words


def main():
    print("扫描覆盖包 vs 基准 ...")
    pending, auto_skip = collect_pending()
    print("待翻译候选:%d 条  |  AUTO-SKIP(纯符号/数字/标记):%d 条" % (len(pending), auto_skip))
    batches = split_batches(pending)
    total_keys, total_words = write_batches(batches, auto_skip)
    print("已生成 %d 个批次,合计 %d key / 约 %d 英文词" % (len(batches), total_keys, total_words))
    print("输出目录:", BATCH_DIR)


if __name__ == "__main__":
    main()
