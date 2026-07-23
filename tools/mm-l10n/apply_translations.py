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
  - 幂等:再次运行同一 TSV,目标 English 已是等价实体形式则视为已应用(no-op),不重复改动。
  - **单遍替换 + 收敛性自检**:同文件所有 key 一次 TEXT_BLOCK.sub 完成(消除「每 key 重跑
    整文件正则」的累积脆弱性),落盘后立即重读校验每个目标 key 的 English 确等于目标 entity;
    任何「声称处理却未落实」的漏写在此暴露并计入退出码,而非静默丢失(保证:首跑后重跑必幂等)。
  - TSV 异常行(列数<4)不再静默丢弃,单独报出并计入退出码。
  - 可传多个 TSV;chinese 列为空的行跳过(未翻译)。
  - 输出:应用数 / 跳过数 / 拒绝数 / 未找到 / TSV 异常行 / 收敛未落实 + 明细。

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
    # 方括号标记:合法词表内、或该条基准 English 原文本就有此 token(逐条守恒放行,
    # 如快捷键字面文本 [ALT + CTRL + O])—— 二者皆不满足才判非法。
    base_marks = set(B.MARKUP_RE.findall(base_english))
    bad = [m for m in B.MARKUP_RE.findall(chinese)
           if not B.is_known_markup(m) and m not in base_marks]
    if bad:
        return False, "含非法方括号标记(不在合法词表且基准原文亦无): %s" % ", ".join(sorted(set(bad)))
    # 不得多出基准没有的 [LINK=*]
    base_links = B.link_multiset(base_english)
    chi_links = B.link_multiset(chinese)
    extra = chi_links - base_links
    extra_link = {k: v for k, v in extra.items() if k.startswith('[LINK=')}
    if extra_link:
        return False, "多出基准没有的 LINK 标记: %s" % dict(extra_link)
    return True, ""


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
    """读批次 TSV,产出 (file, key, chinese) 列表;跳过表头与 chinese 空行。

    返回 (rows, malformed):malformed 为列数<4 的异常行 [(lineno, 原始行)],
    交由上层报出——旧实现静默 continue 丢弃这些行,是「首跑漏条」的隐患之一。
    """
    rows = []
    malformed = []
    with open(path, "r", encoding="utf-8") as f:
        header = f.readline()  # file\tkey\tenglish\tchinese
        for lineno, ln in enumerate(f, 2):
            ln = ln.rstrip('\n')
            if not ln.strip():
                continue
            parts = ln.split('\t')
            if len(parts) < 4:
                malformed.append((lineno, ln[:80]))
                continue
            fn, key, _eng = parts[0], parts[1], parts[2]
            # chinese 是第 4 列「及其后」——若 chinese 内含未转义制表符会被 split 拆多段,
            # 用 join 复原整段(转义规范要求 chinese 内制表符应写为 \\t;此处再兜一层防截断)。
            chinese = tsv_unescape("\t".join(parts[3:]))
            if chinese.strip() == "":
                continue  # 未翻译
            rows.append((fn, key, chinese))
    return rows, malformed


def _replace_keys_in_file(over_raw, want):
    """单遍替换:对一个文件的一批 (key -> entity),一次 TEXT_BLOCK.sub 完成全部替换。

    单遍扫描避免「每 key 重跑整文件正则」的脆弱累积;每个 TEXT 块最多命中一次。
    返回 (new_raw, per_key_status),per_key_status: key -> 'applied'/'noop'/'not_found'。
    未在文件中出现的 key 标 'not_found'。
    """
    status = {k: 'not_found' for k in want}

    def repl(bm):
        blk = bm.group(1)
        t = B.TAG_RE.search(blk)
        if not t:
            return bm.group(0)
        key = t.group(1).strip()
        if key not in want:
            return bm.group(0)
        entity = want[key]
        em = B.ENGLISH_RE.search(blk)
        if not em:
            status[key] = 'not_found'
            return bm.group(0)
        english_inner = em.group(1)
        nested, _ = B.split_english_content(english_inner)
        if nested:
            new_inner = B.INNER_TEXT_RE.sub(
                lambda m: m.group(1) + entity + m.group(3), english_inner, count=1)
        else:
            new_inner = entity
        if new_inner == english_inner:
            status[key] = 'noop'
            return bm.group(0)
        new_english = '<English>' + new_inner + '</English>'
        new_blk = blk[:em.start()] + new_english + blk[em.end():]
        status[key] = 'applied'
        return '<TEXT>' + new_blk + '</TEXT>'

    new_raw = B.TEXT_BLOCK.sub(repl, over_raw)
    return new_raw, status


def _verify_persisted(over_raw, want):
    """收敛性自检:重新扫描 over_raw,确认 want 中每个 key 的 English(结构化取内层 Text)
    确实 == 目标 entity。返回未落实的 key 列表 [(key, 现值截断)]。"""
    cur = {}
    for bm in B.TEXT_BLOCK.finditer(over_raw):
        blk = bm.group(1)
        t = B.TAG_RE.search(blk)
        if not t:
            continue
        key = t.group(1).strip()
        if key not in want:
            continue
        em = B.ENGLISH_RE.search(blk)
        if not em:
            cur[key] = None
            continue
        nested, _ = B.split_english_content(em.group(1))
        if nested:
            m = B.INNER_TEXT_RE.search(em.group(1))
            cur[key] = m.group(2) if m else None
        else:
            cur[key] = em.group(1)
    bad = []
    for key, ent in want.items():
        got = cur.get(key)
        if got != ent:
            bad.append((key, (got[:40] if got else got)))
    return bad


def apply_files(tsv_paths, over_dir=None, base_dir=None):
    over_dir = over_dir or B.OUT_DIR
    base_cache = {}
    applied = 0
    noop = 0
    rejected = []
    not_found = []
    malformed_all = []
    unconverged = []   # 收敛性自检失败:声称写入却未落实(根因防线)

    # 先聚合所有批次的行,按文件分组(同文件所有 key 一次替换 → 单遍,消除累积脆弱性)
    per_file = {}   # fn -> {key: entity}
    for path in tsv_paths:
        rows, malformed = read_tsv(path)
        for lineno, ln in malformed:
            malformed_all.append((os.path.basename(path), lineno, ln))
        for fn, key, chinese in rows:
            base_eng = base_english_of(base_cache, fn, key, base_dir)
            if base_eng is None:
                not_found.append((fn, key, "基准无此 key 或文件缺失"))
                continue
            ok, reason = validate_translation(chinese, base_eng)
            if not ok:
                rejected.append((fn, key, reason))
                continue
            per_file.setdefault(fn, {})[key] = B.to_entities(chinese)

    # 逐文件单遍替换 + 落盘 + 收敛性自检
    for fn, want in per_file.items():
        over_path = os.path.join(over_dir, fn)
        over_raw = open(over_path, "rb").read().decode(B.ENC)
        new_raw, status = _replace_keys_in_file(over_raw, want)

        for key, st in status.items():
            if st == 'applied':
                applied += 1
            elif st == 'noop':
                noop += 1
            else:
                not_found.append((fn, key, "覆盖包中未定位到该 key 的 English 列"))

        # 落盘(纯 ASCII)
        with open(over_path, "wb") as w:
            w.write(new_raw.encode(B.ENC))

        # 收敛性自检:重读落盘结果,确认每个目标 key 的 English 确等于目标 entity。
        # 任何「声称处理却未落实」在此暴露,而非静默漏写(直接对齐验收:首跑后重跑必幂等)。
        reread = open(over_path, "rb").read().decode(B.ENC)
        bad = _verify_persisted(reread, want)
        for key, got in bad:
            # not_found 的 key 不算未收敛(本就无处可写);其余是真异常
            if status.get(key) != 'not_found':
                unconverged.append((fn, key, got))

    return applied, noop, rejected, not_found, malformed_all, unconverged


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

    (applied, noop, rejected, not_found,
     malformed, unconverged) = apply_files(tsv_paths, over_dir, base_dir)

    print("=" * 60)
    print("译文注入结果")
    print("  已应用: %d" % applied)
    print("  幂等跳过(已是目标译文): %d" % noop)
    print("  拒绝: %d" % len(rejected))
    print("  未找到 key: %d" % len(not_found))
    print("  TSV 异常行(列数<4,已跳过): %d" % len(malformed))
    print("  收敛性自检未落实: %d" % len(unconverged))
    print("=" * 60)
    if rejected:
        print("\n### 拒绝明细")
        for fn, key, reason in rejected:
            print("  ✗ [%s] %s : %s" % (fn, key, reason))
    if not_found:
        print("\n### 未找到明细")
        for fn, key, reason in not_found:
            print("  ? [%s] %s : %s" % (fn, key, reason))
    if malformed:
        print("\n### TSV 异常行明细(列数<4,已跳过——请检查 TSV 完整性)")
        for src, lineno, ln in malformed:
            print("  ! [%s:%d] %s" % (src, lineno, ln))
    if unconverged:
        print("\n### 收敛性自检失败(声称处理却未落实,严重——请报告)")
        for fn, key, got in unconverged:
            print("  ✗✗ [%s] %s 现值=%r" % (fn, key, got))

    # 退出码:有拒绝 / 收敛失败 / TSV 异常行 → 非 0,便于流水线感知
    return 1 if (rejected or unconverged or malformed) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
