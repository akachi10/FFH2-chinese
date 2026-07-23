#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
M6.0 翻译流水线 · 译文注入工具

读取填好 `chinese` 列的批次 TSV(UTF-8),逐条把中文安全注入覆盖包(MM汉化MOD)的
English 列。硬锚点 A1/A5/A9 及校验口径 v2 全程适用。

每条处理:
  1. 用 (file, key) 定位覆盖包文件中的 TEXT 块及其 English 列。
  2. **数值占位符**:译文与基准 English 的数值占位符多重集必须**精确一致(含大小写)**,
     否则拒绝(引擎参数错位会报错)。
  3. **方括号标记**:译文所有 `[...]` 标记必须都在合法词表内;且**不得多出基准没有的
     `[LINK=*]`**(悬空链接风险),否则拒绝。
  4. **非 ASCII -> `&#x` 数字实体**(A1,输出纯 ASCII)。
  5. **文本级精准替换**该 key 的 English 内容(结构化则仅换内层 <Text>),文件其余部分逐字节
     不动(A5)。

特性:
  - 幂等:再次运行同一 TSV,若目标 English 已是等价实体形式则视为已应用(no-op),不重复改动。
  - 可传多个 TSV;chinese 列为空的行跳过(未翻译)。
  - 输出:应用数 / 跳过数 / 拒绝数 + 拒绝原因明细。

复用 backfill.py 的解析/规则/实体函数,避免重复实现。标准库实现。

用法:
  python3 apply_translations.py batches/batch-01.tsv [batch-02.tsv ...]
  python3 apply_translations.py --all         # 应用 batches/ 下所有 batch-*.tsv
"""

import os
import re
import sys
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import backfill as B

BATCH_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "batches")


def tsv_unescape(s):
    """还原 make_batches 的转义:字面 \\t \\r \\n \\\\ -> 真实字符。"""
    out = []
    i = 0
    while i < len(s):
        c = s[i]
        if c == '\\' and i + 1 < len(s):
            nx = s[i + 1]
            out.append({'t': '\t', 'r': '\r', 'n': '\n', '\\': '\\'}.get(nx, nx))
            i += 2
        else:
            out.append(c)
            i += 1
    return ''.join(out)


def num_ph_exact(s):
    """数值占位符多重集,**精确大小写**(不做 lower)。"""
    return Counter(B.NUM_PH_RE.findall(s))


def validate_translation(chinese, base_english):
    """校验译文能否安全注入。返回 (ok, reason)。base_english 为基准 English 真实文本。"""
    # 数值占位符精确一致(含大小写)
    if num_ph_exact(chinese) != num_ph_exact(base_english):
        return False, "数值占位符与基准不一致(需精确含大小写): 译文=%s 基准=%s" % (
            dict(num_ph_exact(chinese)), dict(num_ph_exact(base_english)))
    # 方括号标记必须都在合法词表内
    bad = [m for m in B.MARKUP_RE.findall(chinese) if not B.is_known_markup(m)]
    if bad:
        return False, "含非法方括号标记(不在合法词表): %s" % ", ".join(sorted(set(bad)))
    # 不得多出基准没有的 [LINK=*]
    base_links = B.link_multiset(base_english)
    chi_links = B.link_multiset(chinese)
    extra = chi_links - base_links
    extra_link = {k: v for k, v in extra.items() if k.startswith('[LINK=')}
    if extra_link:
        return False, "多出基准没有的 LINK 标记: %s" % dict(extra_link)
    return True, ""


def find_and_replace(over_raw, key, entity):
    """在覆盖包文本中定位 key 的 TEXT 块,替换其 English 内容为 entity。

    返回 (new_raw, status):
      status='applied'   已替换
      status='noop'      目标 English 已等于 entity(幂等,无需改)
      status='not_found' 未找到该 key 或无 English 列
    """
    result = {'status': 'not_found', 'raw': over_raw}

    def repl(bm):
        blk = bm.group(1)
        t = B.TAG_RE.search(blk)
        if not t or t.group(1).strip() != key:
            return bm.group(0)
        em = B.ENGLISH_RE.search(blk)
        if not em:
            return bm.group(0)
        english_inner = em.group(1)
        nested, _ = B.split_english_content(english_inner)
        if nested:
            new_inner = B.INNER_TEXT_RE.sub(
                lambda m: m.group(1) + entity + m.group(3), english_inner, count=1)
        else:
            new_inner = entity
        if new_inner == english_inner:
            result['status'] = 'noop'
            return bm.group(0)
        new_english = '<English>' + new_inner + '</English>'
        new_blk = blk[:em.start()] + new_english + blk[em.end():]
        result['status'] = 'applied'
        return '<TEXT>' + new_blk + '</TEXT>'

    new_raw = B.TEXT_BLOCK.sub(repl, over_raw)
    result['raw'] = new_raw
    return result['raw'], result['status']


def base_english_of(base_raw_cache, fn, key, base_dir=None):
    """取基准 English 真实文本(结构化取内层 Text);缓存按文件。"""
    if fn not in base_raw_cache:
        path = os.path.join(base_dir or B.MM_SRC_DIR, fn)
        if not os.path.exists(path):
            base_raw_cache[fn] = None
        else:
            raw = open(path, "rb").read().decode(B.ENC)
            d = {}
            for bm in B.TEXT_BLOCK.finditer(raw):
                blk = bm.group(1)
                t = B.TAG_RE.search(blk)
                em = B.ENGLISH_RE.search(blk)
                if not t or not em:
                    continue
                _, eng = B.split_english_content(em.group(1))
                d[t.group(1).strip()] = eng
            base_raw_cache[fn] = d
    d = base_raw_cache[fn]
    return None if d is None else d.get(key)


def read_tsv(path):
    """读批次 TSV,产出 (file, key, chinese) 列表;跳过表头与 chinese 空行。"""
    rows = []
    with open(path, "r", encoding="utf-8") as f:
        header = f.readline()  # file\tkey\tenglish\tchinese
        for ln in f:
            ln = ln.rstrip('\n')
            if not ln.strip():
                continue
            parts = ln.split('\t')
            if len(parts) < 4:
                continue
            fn, key, _eng, chinese = parts[0], parts[1], parts[2], parts[3]
            chinese = tsv_unescape(chinese)
            if chinese.strip() == "":
                continue  # 未翻译
            rows.append((fn, key, chinese))
    return rows


def apply_files(tsv_paths, over_dir=None, base_dir=None):
    over_dir = over_dir or B.OUT_DIR
    base_cache = {}
    over_cache = {}     # fn -> 当前文本(累积多行修改)
    applied = 0
    noop = 0
    skipped_untranslated = 0  # 由 read_tsv 已滤掉,统计另计
    rejected = []
    not_found = []

    for path in tsv_paths:
        rows = read_tsv(path)
        for fn, key, chinese in rows:
            base_eng = base_english_of(base_cache, fn, key, base_dir)
            if base_eng is None:
                not_found.append((fn, key, "基准无此 key 或文件缺失"))
                continue
            ok, reason = validate_translation(chinese, base_eng)
            if not ok:
                rejected.append((fn, key, reason))
                continue
            # 通过 -> 数值占位符大小写已保证一致;转实体
            entity = B.to_entities(chinese)
            if fn not in over_cache:
                over_path = os.path.join(over_dir, fn)
                over_cache[fn] = open(over_path, "rb").read().decode(B.ENC)
            new_raw, status = find_and_replace(over_cache[fn], key, entity)
            over_cache[fn] = new_raw
            if status == 'applied':
                applied += 1
            elif status == 'noop':
                noop += 1
            else:
                not_found.append((fn, key, "覆盖包中未定位到该 key 的 English 列"))

    # 落盘(纯 ASCII)
    for fn, raw in over_cache.items():
        with open(os.path.join(over_dir, fn), "wb") as w:
            w.write(raw.encode(B.ENC))

    return applied, noop, rejected, not_found


def main(argv):
    # 解析可选目录覆盖(自验用:对副本操作,不碰真覆盖包);默认走 B.OUT_DIR/B.MM_SRC_DIR。
    over_dir = None
    base_dir = None
    args = []
    it = iter(argv[1:])
    for a in it:
        if a == "--over-dir":
            over_dir = os.path.abspath(next(it)); continue
        if a == "--base-dir":
            base_dir = os.path.abspath(next(it)); continue
        args.append(a)

    if not args:
        print("用法: python3 apply_translations.py <batch.tsv> [...]  |  --all"
              "  [--over-dir DIR --base-dir DIR]")
        return 2
    if args == ["--all"]:
        tsv_paths = sorted(
            os.path.join(BATCH_DIR, f) for f in os.listdir(BATCH_DIR)
            if re.match(r'batch-\d+\.tsv$', f))
        if not tsv_paths:
            print("batches/ 下无 batch-*.tsv")
            return 0
    else:
        tsv_paths = args

    applied, noop, rejected, not_found = apply_files(tsv_paths, over_dir, base_dir)

    print("=" * 60)
    print("译文注入结果")
    print("  已应用: %d" % applied)
    print("  幂等跳过(已是目标译文): %d" % noop)
    print("  拒绝: %d" % len(rejected))
    print("  未找到 key: %d" % len(not_found))
    print("=" * 60)
    if rejected:
        print("\n### 拒绝明细")
        for fn, key, reason in rejected:
            print("  ✗ [%s] %s : %s" % (fn, key, reason))
    if not_found:
        print("\n### 未找到明细")
        for fn, key, reason in not_found:
            print("  ? [%s] %s : %s" % (fn, key, reason))

    # 有拒绝时退出码非 0,便于流水线感知
    return 1 if rejected else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
