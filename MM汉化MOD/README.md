# MM汉化MOD — MagisterModmod 中文覆盖包

基于 MagisterModmod 2023-10-20 版(见 `../MM源码/`)。

**使用方式(直接替换)**:把本目录下 `Assets/` 整个复制进游戏的
`Beyond the Sword/Mods/MagisterModmod/`,覆盖同名文件即可;删掉被覆盖的文件重装 MM 即还原英文。

## 结构

- `Assets/XML/Text/` — 翻译后的文本 XML(与 MM 同名同路径)
- `术语表.md` — Erebus 专名中英对照(以 FFH2 0.41o 官方汉化包译名为准,MM 新增专名在此扩充)

## 翻译规则

1. 只改各 `TXT_KEY` 下的文本内容,**不增删 key、不动占位符**(`%s1`、`%d1`、`[COLOR_*]`、`[ICON_*]`、`[NEWLINE]`、`[PARAGRAPH:*]` 等原样保留)
2. 专名(文明、领袖、宗教、法术领域、单位)一律先查术语表;术语表没有的,新增条目再用
3. lore/图鉴文本按文学翻译标准处理,保持黑暗奇幻文体;界面/游戏性文本以简洁准确优先
4. 与 FFH2 原版重复的 key,优先复用 0.41o 官方汉化的现成译文,只翻 MM 的增量
