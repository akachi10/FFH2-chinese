# MM 汉化 · theme 字体方案(M5)

目标(锚点 A4):让 MagisterModmod 在**英文版 BtS** 上用 **SimSun(宋体)** 渲染文本,做法向官方 0.41o 汉化包对齐——把它已验证能显示中文的 SimSun 字体节移植到 MM 的 theme 加载链上。字体只走 theme,**绝不**动 MM 的 `GameFont*.tga`(锚点 A3)。

---

## 1. MM 的 theme 引用链分析

### 1.1 MM 只随包一个入口 thm

`MM源码/Resource/` 下**仅有** `Civ4.thm` 一个文件,内容(全文):

```
resource_path	"Mods/Magister Modmod for FfH2/Resource";
include			"Mods/Magister Modmod for FfH2/Resource/Themes/Civ4/Civ4Theme.thm";
```

两条路径都以 **BtS 安装根**为基准(Civ4 的 GFC 主题引擎按游戏根解析 thm 路径)。

### 1.2 引用链最终引用谁的 Civ4Theme_Common.thm?

**结论:引用链最终指向的 `Civ4Theme.thm` 及其叶子 `Civ4Theme_Common.thm` 都不在 MM 随包文件里 —— 它们由基础游戏(BtS 本体)的主题回退目录提供。**

推导:
1. MM 的 `Civ4.thm` → `include` 了 `Mods/Magister Modmod for FfH2/Resource/Themes/Civ4/Civ4Theme.thm`。
2. 但 `MM源码/` 全树里**没有** `Themes/` 子目录 —— 即 MM **不随包** `Civ4Theme.thm`,也不随包 `Civ4Theme_Common.thm`。全系统检索(仓库 + tmp)均只有 MM 的 `Civ4.thm` 这一个 thm 入口,再无同名文件。
3. 因此该 `include` 路径下的文件由 Civ4 资源加载器的**回退机制**解析:mod 未提供的资源回落到基础游戏资源目录 `<BtS>\Resources\Themes\Civ4\`。`Civ4Theme.thm` 再 `include` `Civ4Theme_Common.thm`(字体节所在)。
4. **MM 是完全独立的 mod**(自带完整 Assets:111 个 Text XML、自己的 CvGameCoreDLL.dll、自己的 `GameFont*.tga`、自己的 `Resource/Civ4.thm`),它的 theme 链完全以 `Mods/Magister Modmod for FfH2/` 为根自洽,**不依赖 "Fall from Heaven 2" 作为并列 mod 存在**。

### 1.3 官方汉化包的做法(成品参照)

官方 0.41o 汉化包在 `Fall from Heaven 2/Resource/Themes/Civ4/` 下投放了 **7 个叶子 thm**(`Civ4Theme_Button/Common/Edit/Label/Scroll/SplitPanel/Window`),**没有** `Civ4.thm`、也**没有**中间层 `Civ4Theme.thm`。

- 也就是说,官方包**只覆盖叶子主题文件**,不碰入口/中间层——靠资源加载器"mod 目录优先于基础游戏回退"的规则,让自己那份带 SimSun 的叶子文件盖过 BtS 本体的叶子文件。
- 逐文件核查:7 个叶子里**只有 `Civ4Theme_Common.thm` 含字体节(SimSun)**,其余 6 个是皮肤/布局定义,不含任何 `GFont(...)`。因此字体覆盖的**唯一有效文件是 `Civ4Theme_Common.thm`**;官方包投放全部 7 个,只是选择整目录携带,其余 6 个对字体无贡献(且与基础游戏本体字节一致)。

---

## 2. 覆盖文件应落的最终游戏路径

### 2.1 结论:落在 MM 自己的子树,不落 "Fall from Heaven 2" 目录

官方包投放到 "Fall from Heaven 2" 目录,是因为**它汉化的对象是 FFH2 那个 mod**,其 theme 链根在 `Mods/Fall from Heaven 2/`。而**我们汉化的对象是 MM**,MM 的 `resource_path` 与 `include` 全部硬编码 `Mods/Magister Modmod for FfH2/Resource` —— 它的资源加载优先搜索 **MM 自己的 mod 资源路径**,再回退基础游戏。

所以要让带 SimSun 的 `Civ4Theme_Common.thm` 盖过 BtS 本体回退,必须把它放进 **MM 自己的 theme 子树**:

```
Mods/Magister Modmod for FfH2/Resource/Themes/Civ4/Civ4Theme_Common.thm
```

这样 MM 的 `Civ4.thm` → `Civ4Theme.thm`(仍来自 BtS 回退)→ `Civ4Theme_Common.thm`(**命中 MM 子树里我们投放的这份**,优先于 BtS 本体的同名叶子)。**无需**依赖 "Fall from Heaven 2" 目录里有什么。

### 2.2 覆盖包内相对路径(与 MM 安装目录同构)

```
MM汉化MOD/Resource/Themes/Civ4/Civ4Theme_Common.thm
```

发布时按原路径复制进 MM 安装目录即生效。

### 2.3 ⚠️ 安装目录名歧义(交 SM / M9 决策)

- MM 的 `Civ4.thm` 与 ini 里 mod 名为 **`Magister Modmod for FfH2`**(带空格)。MM 的 theme 链**内部**硬编码这个带空格名,与物理安装文件夹名无关(内部路径由 thm 自引用锁定)。
- 但现有 `docs/mm-localization/安装顺序.md`(第 23-25 行)写的安装文件夹是 **`Mods\MagisterModmod`**(无空格,来自 2023-10-20 installer 生成的目录名)。
- **物理覆盖动作**是"把 `MM汉化MOD/` 整目录复制进 installer 实际生成的那个 MM 文件夹"。因此覆盖文件的物理落点 = installer 生成的文件夹名(以 `安装顺序.md` 记录的 `MagisterModmod` 为准),即:
  `...\Beyond the Sword\Mods\MagisterModmod\Resource\Themes\Civ4\Civ4Theme_Common.thm`
- 这不影响 theme 链正确性(MM 的 `Civ4.thm` 用带空格的内部路径引用自身 Resource;资源加载器按当前激活 mod 的实际目录解析,folder 名以 installer 为准)。M9 写安装文档时按 `安装顺序.md` 既有的 `MagisterModmod` 落点即可,本文件无需玩家手动新建 `Themes/Civ4/` 以外的东西——`MM汉化MOD/` 整目录复制会自动带出该子路径。

---

## 3. 改了哪些行(diff 摘要)

**本方案对 thm 内容零手工改动。** 采用 A9 最保守做法:**直接字节复制官方 0.41o 汉化包已验证的 `Civ4Theme_Common.thm`**,不手改一行——因为该文件本身就是已验证能显示中文的成品,手改反而引入风险。

- 源:官方包 `Fall from Heaven 2/Resource/Themes/Civ4/Civ4Theme_Common.thm`
- 目标:`MM汉化MOD/Resource/Themes/Civ4/Civ4Theme_Common.thm`
- 校验:`cmp` 逐字节相同,MD5 均为 `085ac41d9546eb75c9c734c4acb6a802`(IDENTICAL)

相对 **BtS 本体原版** `Civ4Theme_Common.thm`,官方包在字体节(约 373-411 行,`// >>> CYBERFRONT ... // <<< CYBERFRONT` 块)做的变更是:把原版 **Sylfaen** 字体族改为 **SimSun**,并注释掉整段 Sylfaen 定义。生效的 SimSun 字体节:

```
GFont .Size1_Normal = GFont("SimSun", "Regular", 13, ...ALPHA);
GFont .Size2_Normal = GFont("SimSun", "Regular", 14, ...ALPHA);
GFont .Size2_Bold   = GFont("SimSun", "Bold",    14, ...BOLD, ALPHA);
GFont .Size2_Italic = GFont("SimSun", "Italic",  14, ...ITALIC, ALPHA);
GFont .Size3_Normal = GFont("SimSun", "Regular", 15, ...ALPHA);
GFont .Size3_Bold   = GFont("SimSun", "Bold",    15, ...BOLD, ALPHA);
GFont .Size4_Normal = GFont("SimSun", "Regular", 22, ...ALPHA);
GFont .Size4_Bold   = GFont("SimSun", "Bold",    20, ...BOLD, ALPHA);
```

即 SimSun 13/14/15/22px(Size4_Bold 为 20px)。字体节以外的皮肤/布局/光标/图标定义与原版逐字节一致。

**只投放 `Civ4Theme_Common.thm` 一个文件**(A9 改动最小化):其余 6 个官方叶子 thm 不含字体、对本目标无贡献,不携带。

---

## 4. CrossOver bottle 需装 SimSun 字体(必读)

theme 里 `GFont("SimSun", ...)` 是按**字体族名**向操作系统要字体,thm 自身**不携带任何字库文件**。因此运行环境的 bottle 里**必须**装有宋体,否则引擎找不到 SimSun,中文会退回方块/缺字。

**做法:把 `simsun.ttc` 放进 bottle 的 Windows 字体目录。**

- 目标路径:`<CrossOver bottle>/drive_c/windows/Fonts/simsun.ttc`
  (即游戏视角的 `c:\windows\Fonts\simsun.ttc`)
- 来源:任一简体中文版 Windows 的 `C:\Windows\Fonts\simsun.ttc`(SimSun/NSimSun 合集,含"宋体")。
- 放入后重启 bottle 内的游戏进程即可被 theme 识别。
- CrossOver 默认 bottle **不带宋体**,此步不可省。
- 字库版权归微软,随汉化包**不分发** `simsun.ttc`,由用户自行从自有 Windows 拷入(与官方汉化包做法一致——官方包同样不含 ttf/ttc)。

> M9 安装文档收口时,把本节整合进 `安装顺序.md` 第 7 步"中文字体"占位(该步原文标注"待补充")。

---

## 5. 风险点

| # | 风险 | 评估 / 缓解 |
|---|------|------------|
| R1 | MM 的 `Civ4Theme.thm`(中间层,来自 BtS 回退)引用叶子的路径若与 MM 子树不在同一 `resource_path` 覆盖域,叶子覆盖可能不命中 | 低。官方包已用同款"只覆盖叶子、不碰中间层"证明该机制可行;MM 与 FFH2 同源同 GFC 引擎,行为一致。**但本机无 Civ4 运行环境,最终以用户 CrossOver 内实测为准**——若中文不显示,回退方案见 R2。 |
| R2 | 万一叶子覆盖不命中(极端情况) | 备选:把中间层 `Civ4Theme.thm` 也一并投放到 MM 子树(从 BtS 本体拷出、改其 include 指向 MM 子树的 Common),但这偏离 A9 最小改动,非必要不做。**先按当前单文件方案让用户实测。** |
| R3 | bottle 未装 SimSun | 中文变方块。缓解:第 4 节步骤 + M9 安装文档强调"此步不可省"。 |
| R4 | 安装文件夹名歧义(`MagisterModmod` vs `Magister Modmod for FfH2`) | 见 §2.3,已交 M9/SM。不影响 theme 链正确性,只影响物理复制落点。 |
| R5 | 与 A3 冲突风险 | 无。本方案只投放 `Civ4Theme_Common.thm`,完全不触碰 `GameFont.tga` / `GameFont_75.tga`,严格守 A3。 |

---

## 6. 交付物清单

1. `MM汉化MOD/Resource/Themes/Civ4/Civ4Theme_Common.thm`(字节等同官方 0.41o 汉化包成品,MD5 `085ac41d9546eb75c9c734c4acb6a802`)
2. 本文件 `docs/mm-localization/theme方案.md`
