# 翻译批次索引

由 `tools/mm-l10n/make_batches.py` 生成。每批为待翻译条目骨架 TSV(UTF-8,TAB 分隔,列 `file / key / english / chinese`),填好 `chinese` 列后由 `apply_translations.py` 注入。

- **批次总数**:24
- **待翻译条目合计**:7734 key
- **英文词量合计**(剔除标记/占位符):约 269800 词
- **AUTO-SKIP**(English 与基准相同但无字母单词,纯符号/数字/标记,无需翻译):51 条

切批阈值:每批 ≤ 700 key 或 ≤ 12000 英文词。批内文件聚集(同文件 key 连续排列,小文件可合批,大文件按 key 区间拆多批)。

| 批次 | 文件范围 | key 数 | 英文词数 |
|------|---------|-------|---------|
| batch-01.tsv | AIAutoPlay_CIV4GameText.xml … BUGOptions_RevDCMGameText.xml (17 文件) | 700 | 5060 |
| batch-02.tsv | BUGOptions_RevDCMGameText.xml … CIV4DiplomacyText.xml (10 文件) | 690 | 11981 |
| batch-03.tsv | CIV4DiplomacyText.xml | 700 | 7145 |
| batch-04.tsv | CIV4DiplomacyText.xml … CIV4GameText_Events_BTS.xml (5 文件) | 643 | 11977 |
| batch-05.tsv | CIV4GameText_Events_BTS.xml … CIV4GameText_FFH2.xml (3 文件) | 388 | 10628 |
| batch-06.tsv | CIV4GameText_FFH2.xml | 101 | 11549 |
| batch-07.tsv | CIV4GameText_FFH2.xml … Civ4lerts Options.xml (17 文件) | 617 | 11988 |
| batch-08.tsv | Civ4lerts Options.xml … Magister_CIV4GameText_FFH2.xml (18 文件) | 201 | 11662 |
| batch-09.tsv | Magister_CIV4GameText_FFH2.xml | 180 | 11989 |
| batch-10.tsv | Magister_CIV4GameText_FFH2.xml | 118 | 11322 |
| batch-11.tsv | Magister_CIV4GameText_FFH2.xml | 399 | 11936 |
| batch-12.tsv | Magister_CIV4GameText_FFH2.xml | 75 | 9217 |
| batch-13.tsv | Magister_CIV4GameText_FFH2.xml | 1 | 17281 |
| batch-14.tsv | Magister_CIV4GameText_FFH2.xml | 15 | 10869 |
| batch-15.tsv | Magister_CIV4GameText_FFH2.xml | 1 | 22593 |
| batch-16.tsv | Magister_CIV4GameText_FFH2.xml | 375 | 7087 |
| batch-17.tsv | Magister_CIV4GameText_FFH2.xml | 30 | 11259 |
| batch-18.tsv | Magister_CIV4GameText_FFH2.xml | 636 | 11997 |
| batch-19.tsv | Magister_CIV4GameText_FFH2.xml | 172 | 11984 |
| batch-20.tsv | Magister_CIV4GameText_FFH2.xml | 266 | 11898 |
| batch-21.tsv | Magister_CIV4GameText_FFH2.xml | 183 | 11587 |
| batch-22.tsv | Magister_CIV4GameText_FFH2.xml … RevolutionText_CIV4GameText.xml (23 文件) | 700 | 11796 |
| batch-23.tsv | RevolutionText_CIV4GameText.xml … Units.xml (17 文件) | 289 | 11903 |
| batch-24.tsv | Units.xml … WorldBuilder_CIV4GameText.xml (6 文件) | 254 | 3092 |
