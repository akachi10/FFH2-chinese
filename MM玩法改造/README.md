# MM 玩法改造记录

> **状态（2026-07-23 晚）：全部三项改造已回退**——用户报告游戏崩溃（"改动挂了"），11 个文件已从 `.bak-mod` 恢复并逐字节验证与 MM源码 一致，`YKMod_GameText.xml` 已移除；崩溃版本留存为 `.crashed-*` 后缀备查。汉化未动。本文档保留为设计与实现记录，待逐项排查崩因后可增量重上。
>
> **崩因已实锤（21:39 截图的 XML Load Error 弹窗）**：改造 4 的 `PROMOTION_FLESH_ROT` 里
> `<iCombatHealPercent>50</iCombatHealPercent>`（第 11858 行）**插错了 schema 位置**——
> CIV4UnitSchema.xml 对晋升子元素有严格顺序，该字段放错位导致整个 `CIV4PromotionInfos.xml`
> 校验失败、启动即断。改造 1-3 不涉此文件，非崩因。重上改造 4 时须按 schema 中
> `PromotionInfo` 元素序列把 `iCombatHealPercent` 放到与原版晋升（如带该字段的现成条目）
> 相同的相对位置。

改造目标（用户 2026-07-23 定）：**不希望任何国家灭亡**——让每个文明的首都（王宫城市）几乎不可能被攻陷。改动均为 XML/Python 层，不动 DLL；对已有存档兼容（未新增任何类型，重启游戏即生效）。

## 改造 1：王宫防御 +300%（含免疫轰炸）

文件：`Assets/XML/Buildings/CIV4BuildingInfos.xml` · `BUILDING_PALACE` 条目（首个建筑，字段在 127-128 行附近）

```xml
<iDefense>300</iDefense>          <!-- 原 0：城防 +300% -->
<iBombardDefense>100</iBombardDefense>  <!-- 原 0：轰炸减防免疫 100%，防御无法被攻城武器削掉 -->
```

注：`iBombardDefense=100` 是补充决策——若可被轰炸，+300% 几回合就会被剥光，违背"首都不陷落"意图。如嫌太强可改回 0 或 50。

## 改造 2：王宫城市每回合自动生成守军

文件：`Assets/python/CvEventManager.py` · `onCityDoTurn`（`pPlayer = gc.getPlayer(...)` 之后插入）

```python
## MOD palace-garrison: palace city spawns a 1-turn immobile Longbowman each turn (Tomb Warden duration precedent)
		if pCity.getNumBuilding(gc.getInfoTypeForString('BUILDING_PALACE')) > 0:
			pGarrison = pPlayer.initUnit(gc.getInfoTypeForString('UNIT_LONGBOWMAN'), pCity.getX(), pCity.getY(), UnitAITypes.NO_UNITAI, DirectionTypes.DIRECTION_SOUTH)
			pGarrison.setDuration(1)
			pGarrison.changeImmobileTimer(2)
			pGarrison.AI_setGroupflag(43)	# 43=GROUPFLAG_SUICIDE_SUMMON, keep AI from marching it out
## MOD palace-garrison end
```

机制说明：
- **纯被动**，不走法术系统，无需 AI 施放；`onCityDoTurn` 由引擎每城每回合自动触发；
- `setDuration(1)`：借召唤单位的存活时长机制，下回合自动消失（先例：墓穴守卫 Tomb Warden，`CvSpellInterface.py` ~6305 行）；
- `changeImmobileTimer(2)`：整个存活期定身不能移动（先例：`CvRandomEventInterface.py` 712 行）；
- 对所有拥有王宫的文明生效（玩家 + AI）；蛮族无王宫不受影响；
- **注释必须纯 ASCII**：Civ4 内置 Python 2.4 无编码声明，中文注释会直接 SyntaxError。

## 改造 3：所有地图尺寸 +2 档（2026-07-23）

原则：每档取原表两档之后的**实际网格数值**；原表没有的最高两档按该表自身步长比外推算出新值。各地图脚本在自己的数列内平移，保持每张图固有比例。

| 位置 | 旧 → 新（宽×高） |
|---|---|
| `Assets/XML/Gameinfo/CIV4WorldInfo.xml`（全局默认，12 个 `_mst` 脚本按此比例缩放） | 10×6/13×8/16×10/21×13/26×16/32×20 → 16×10/21×13/26×16/32×20/**39×25**/**48×31** |
| `PrivateMaps/MountainCoast.py` | →10×7/12×8/15×10/21×14/29×20/41×27 |
| `PrivateMaps/PerfectWorld2.py`、`Totestra.py` | →20×13/24×16/30×20/36×24/43×29/52×35 |
| `PrivateMaps/fm_Mirror_Inland_Sea1.py`（仅网格表；出生点方差表误改后已回滚原值） | →10×6/13×8/16×10/21×13/28×17/36×22 |
| `PrivateMaps/Erebus.py`（基数×scaler 形式） | 基数 8/9/10/13/15/18 → 10/13/15/18/22/26 |

注意：网格单位是 4×4 地块，新"巨大"=48×31 网格 ≈ 192×124 地块，是原巨大的 2.3 倍。Civ4 是 32 位程序，但**本机 YK 版 exe 已带 LAA 标记（已验证 Characteristics=0x012F）**，64 位 Windows 下单进程可用 4GB——巨大档一般可正常游玩；后期回合慢是 AI 单线程所致，与硬件无关。若仍遇 MAF 崩溃再降档。

补丁工具存档：scratchpad `shift_grids.py`（一次性,已执行）。

## 改造 3″：老文档法·纯数字改档（2026-07-23 深夜，现役——取代 3′）

用户拍板：把我方所有地图文件改动全部回退（含 7 个翻译垫片），按 2019 年老文档
（`C:\wm4.back\安装顺序.txt`）的做法重上——**只改 getGridSize 数字表 + WorldInfo，
禁止加任何代码**。执行记录：

1. **回退**：10 个文件从原始备份恢复并哈希验证逐字节一致
   （7 个垫片脚本 ← `.bak-l10n`/`.bak-mod`,Erebus/MountainCoast 网格 ← `.bak-mod`,
   `CIV4WorldInfo.xml` ← `.bak-mod`）。副作用：EC/WoE/PW2/PW2_mst/Totestra/SmartMap/
   MountainCoast 的**自定义选项名回英文**（地图介绍仍中文——走引擎 getText,零脚本）。
   `MapScriptTools.py` 的防崩补丁**保留**（属汉化修补,非地图改动,回退即全 _mst 图重挂）。
2. **重上（只改数字,巨大档放大一级,数值沿用 3′ 的外推）**：

| 文件 | 巨大档改动 |
|---|---|
| `CIV4WorldInfo.xml` | 32×20 → **39×25**;`iDefaultPlayers` 11 → **14** |
| `Erebus.py` | 基数 18 → **22** |
| `MountainCoast.py` | (21,14) → **(29,20)** |
| `PerfectWorld2.py`、`Totestra.py` | (36,24) → **(43,29)** |
| `fm_Mirror_Inland_Sea1.py` | (21,13) → **(28,17)** |

其余 11 个自带 getGridSize 的脚本全部按公式跟随 WorldInfo,自动生效。
5 个脚本 diff 验证仅数字行变化,语法全过;fm_Mirror 编辑期误伤的 1 个注释字节已按原样修回。

3. **本体 PublicMaps 补做（2026-07-24,同规矩只改数字,各 `.bak-mod` 备份）**——
   老文档本就针对 PublicMaps;9 个自带数字表的公共图巨大档放大一级:

| 文件 | 巨大档改动 |
|---|---|
| `Terra.py`、`Global_Highlands.py` | 曾 →(45,29),**超安全线已回退原值 (38,24)**(其本身已是加大表,约等于全局巨大档) |
| `Earth2.py` | (40,24) → (50,30)——其 getGridSize 无 return,系本体死代码,实际跟随 WorldInfo 39×25,数字不生效 |
| `Boreal.py`、`Rainforest.py` | (21,13) → **(28,17)** |
| `Highlands.py` | (26,16) → **(32,20)** |
| `Arboria.py` | (16,16) → **(20,20)** |
| `Donut.py` | (20,20) → **(25,25)** |
| `Team_Battleground.py` | 两套表 (16,10)→**(21,13)**、(13,13)→**(16,16)** |

`Big_and_Small.py` 曾按用户要求加过独立表(巨大档 44×29 = 176×116 地块)——**当晚即在
生成时触发 C++ Runtime Error(引擎极限),已从 `.bak-mod` 恢复原样**,回归跟随 WorldInfo
39×25(该尺寸经 Earth3/PW2/中与小实测可正常生成)。教训:39×25(约 1.56 万地块)是本机
MM 环境的已验证安全线,44×29(约 2 万地块)超限。其余无表公共图
(Medium_and_Small/Hemispheres/Tectonics 等)自动跟随 39×25。

## 改造 3′：仅巨大档放大一级 + 默认玩家 +3（2026-07-23 晚，已被 3″ 取代）

用户拍板：不再全档平移，只把"巨大"档改大一个级别、该档默认玩家 +3。手动 4 处（无补丁脚本）：

| 文件 | 改动 |
|---|---|
| `Assets/XML/Gameinfo/CIV4WorldInfo.xml` | 巨大档网格 32×20 → **39×25**（按 大→巨 步长 ×1.23/×1.25 外推）；`iDefaultPlayers` 11 → **14** |
| `PrivateMaps/Erebus.py` | 巨大档基数 18 → **22**（步长 ×1.2，方形网格） |
| `PrivateMaps/MountainCoast.py` | 巨大档 (21,14) → **(29,20)**（步长 ×1.4） |

埃雷布斯大陆 / World of Erebus / Erebus_mst 及全部 `_mst` 图无自有网格表，按 WorldInfo 巨大档自动跟随。其余档位、其余地图脚本一律未动。回退点：各文件同名 `.bak-mod`（原版原样）。

## 改造 4：血肉傀儡新技能"血肉腐败"（2026-07-23，需开新档生效）

设计（用户定）：血肉炼成术造出的躯体不断腐坏——**每回合 -5 生命**（下限 1，不会腐死）；**永远无法自动回血**（含医疗兵/建筑/法术等一切常规治疗）；**生命 <50 时每回合再 -1 攻击力**（下限 1）；仅两条恢复途径：**吃人**（并入血肉傀儡，+20 生命，原有法术）与**战胜敌人**（+50 生命）。

实现（XML 为主，Python 兜底）：

| 文件 | 改动 |
|---|---|
| `Assets/XML/Units/CIV4PromotionInfos.xml` | 新晋升 `PROMOTION_FLESH_ROT`（插在 PLAGUED 之后）：`iCombatHealPercent=50`（DLL 原生"战胜回血"字段）、`PyPerTurn=effectFleshRot(pCaster)`（FFH 原生每回合钩子）、TechPrereq=TECH_NEVER、图标复用 Plagued.dds |
| `Assets/XML/Units/CIV4UnitInfos.xml` | UNIT_FLESH_GOLEM 的 FreePromotions 加挂 FLESH_ROT（出生自带） |
| `Assets/python/entrypoints/CvSpellInterface.py` | 新增 `effectFleshRot`：HP 台账存单位 ScriptData（`FCHP:` 前缀）——每回合先把 HP 钳回台账值（**取消一切未经认可的治疗**）再 -5；<50 时攻击 -1。`spellAddToFleshGolem` 的 +20 后补一行台账认可 |
| `Assets/python/CvEventManager.py` | `onCombatResult` 开头：傀儡获胜时把 XML 的 +50 回血记入台账 |
| `Assets/XML/Text/YKMod_GameText.xml`（新文件，仓库同步于 `MM汉化MOD-YK`） | `TXT_KEY_PROMOTION_FLESH_ROT`=血肉腐败 + `_HELP` 全文说明（提及血肉炼成术），6 列双中文格式 |

机制要点：`CvUnit::doHeal()` 无下限钳制、`PyPerTurn` 经 `eval(prom.getPyPerTurn())` 派发（与瘟疫 PROMOTION_PLAGUED 同机制）；台账方案保证医疗兵/城市/法力治疗全部无效，仅白名单两途径生效。已知边界：WorldBuilder 手动改单位 ScriptData 会与台账冲突（`FCHP:` 前缀被覆盖则下回合重新初始化，无害）。

## 配置：自动存档每回合一存、保留 100 个（2026-07-25）

文件：`C:\Users\zsts\Documents\My Games\beyond the sword\CivilizationIV.ini`（MM 在 BtS 下运行、模组无独立 ini，此文件即生效配置；备份 `.bak-mod`）

```ini
MaxAutoSaves = 100      ; 原 5
AutoSaveInterval = 1    ; 原 4
```

沿用 2019 年老文档的 ini 做法（当年设 5/4，本次改 100/1）。纯配置，重启游戏即生效，与存档兼容无关。

## 现场备份

改动前备份存于游戏目录同名 `.bak-mod` 文件：
- `CIV4BuildingInfos.xml.bak-mod`、`CvEventManager.py.bak-mod`
- `CIV4WorldInfo.xml.bak-mod`
- `PrivateMaps/`：`MountainCoast.py`、`PerfectWorld2.py`、`Totestra.py`、`fm_Mirror_Inland_Sea1.py`、`Erebus.py` 各自 `.bak-mod`

## 改造 5：FFH2 侧 —— 21 座王宫强化（2026-07-26）

**注意：本条改的是 FFH2，不是 MM。** 目标文件为现装 FFH2：
`C:\Civilization4\Beyond the Sword\Mods\Fall from Heaven 2\Assets\XML\Buildings\CIV4BuildingInfos.xml`
备份：`CIV4BuildingInfos.xml.bak-mod-20260726-213311`（同目录）

> **⚠ 需开新档才完整生效**：本条所改的 `iDefense` / `iFreeSpecialist` 两项在 DLL 里都走 `processBuilding` 的**增量缓存**路径（建筑增减时才累加，数值随存档存取），旧存档里已建成的王宫**不会**自动获得这些加成。仅 `FreePromotion` / `bApplyFreePromotionOnMove` 因每回合重算而对旧档即时生效。要全部生效请**开新档**。详见下方"存档兼容"。

目的：延续"首都难以陷落"意图，并让首都成为更强的运营核心。对全部 21 个 `BUILDING_PALACE_*` 条目统一改 **4 个字段**（21×4=84 行）：

| 字段 | 原值 → 新值 | 说明 |
|---|---|---|
| `iDefense` | 0 → 200（20 座）；**25 → 225**（Infernal） | 加法 +200，保留 Infernal 原生 25 的优势差 |
| `FreePromotion` | NONE → `PROMOTION_BLESSED` | 中文显示"祝福"，即 `SPELL_BLESS` 所授晋升 |
| `bApplyFreePromotionOnMove` | 0 → 1 | 使晋升作用于城内既有单位（语义见下） |
| `iFreeSpecialist` | 0 → 1 | 每座王宫 +1 免费专家 |

> **已取消项：王宫 +1 城市工作半径（`iPlotRadius`）**。曾一度对 21 座王宫设 `iPlotRadius=3`（3 格工作范围），**用户 2026-07-26 裁决该加成过强，整项取消**，21 座全部改回 `0`（与备份原值一致，相对备份零变化）。金龙（Kuriotates）首都的半径 3 由**原生机制**维持——原生建筑 `BUILDING_CITY_OF_A_THOUSAND_SLUMS`（`iPlotRadius=3`）+ 建城/聚落逻辑 `CvCity.cpp:289-299`——**不受本次取消影响**。现全文件 `iPlotRadius` 非 0 的仅千楼之城 1 处。取消后附带消除了下文"半径回落缺陷"所述的双半径建筑风险。

**DLL 语义核实（仓库 `Fall from Heaven 2/Assets/src/CvGameCoreDLL.041o/`）**：

- `bApplyFreePromotionOnMove` 实际**不是"移动时"触发**，而是在 `CvCity::doTurn()` 里每回合遍历城市所在格单位授予晋升（`CvCity.cpp:988-1003`）。故效果为"**每回合结束时**城内单位获得祝福"，非踏入即得。且**离城不会自动移除**（移除只走 `getRemovePromotion` 字段，本次未用）；`PROMOTION_BLESSED` 自带 `bDispellable=1`、`bRemovedByCombat=1`，会被驱散/战斗消耗。
- 只有 `PromotionInfo` 里 `UnitCombat` 允许的兵种才会获得（`CvCity.cpp:997`）。`PROMOTION_BLESSED` 覆盖 Adept/Archer/Beast/Disciple/Melee/Mounted/Recon，不含 Siege/Naval/Animal 等——属预期内的原生限制。
**`iPlotRadius` 调查留档（该项已取消，结论供日后复用）**：

- `iPlotRadius` 是**绝对半径**而非增量：`CvCity.cpp:4062` 直接 `setPlotRadius(建筑值)`，拆除时回落 `setPlotRadius(2)`（默认值见 `CvCity.cpp:509`）。半径 3 → 37 格（`getNumCityPlots()`，`CvCity.cpp:14653-14659`）。若日后重上此项，值应取 3（非 1）。
- **半径回落有已知缺陷**：`CvCity.cpp:4058-4068` 的回落分支是**无条件** `setPlotRadius(2)`——不扫描城内是否还有其它半径建筑，谁先被移除就按谁的默认值砍。故**同城挂两个 radius=3 建筑是危险组合**：迁都或任一建筑消失时，半径会从 37 格被误砍到 21 格且**不会自愈**。金龙首都（原生已有千楼之城 radius 3）尤其踩这个坑——这是该项取消前 code-review 提出的 major 问题，现随整项取消而消失。

**存档兼容**：未新增任何类型，旧存档可读。但 `iDefense` 在 DLL 里被缓存进 `CvCity::m_iBuildingDefense`（`CvCity.h:1073`），仅在建筑增减时增量累加（`CvCity.cpp:4222`）并随存档读写（`CvCity.cpp:12445/12693`）——**旧存档里已建成的王宫不会自动获得新增城防**，需新开局（或重建该建筑）才生效。`iFreeSpecialist` 同理走 `processBuilding` 增量路径。**故这两项数值加成一律以新开档为准**；`FreePromotion` 系两项因 `CvCity::doTurn()` 每回合重算，旧档即时生效。重启游戏后新局全部生效。

**未动**：王宫其它字段（法力、快乐、iCrime、厌战等）一律未改；其它建筑一律未改；未加 XML 注释（保持原文件风格）。仓库内 `Fall from Heaven 2/Assets/XML/Buildings/CIV4BuildingInfos.xml` 与现装版本内容不同（非同一构建），按边界未同步。

**校验**（取消 `iPlotRadius` 后的最终态）：Python 3.12 解析通过（well-formed）；diff 对备份恰好 **84 行** = `iDefense` 21 + `FreePromotion` 21 + `bApplyFreePromotionOnMove` 21 + `iFreeSpecialist` 21；**`iPlotRadius` 不出现在 diff 中**（21 座全为 0，与备份原值一致）；PALACE 区块外改动 0 行，非 PALACE 建筑逐条比对与备份完全一致（零附带改动）。全文件 `iPlotRadius` 非 0 仅 1 处（千楼之城原生 3）。4 个字段均为**改值不改结构**（未插入/删除/移位任何元素），且文件内元素顺序与 `CIV4BuildingsSchema.xml` 声明序列一致——不重蹈改造 4 因插错 schema 位置导致启动崩溃的覆辙。

## 改造 6：金龙族（Kuriotates）仅最大地图城市上限翻倍（2026-07-26，FFH2 侧）

**注意：本条属 FFH2 谱系**（`C:\Civilization4\Beyond the Sword\Mods\Fall from Heaven 2\`），不是 MM。MM 目录未动。

需求（用户 2026-07-26 定稿口径）：Kuriotates 特色为城市数硬上限（超出的只能是 settlement 聚落）。**只有最大地图 HUGE 的上限翻倍（5 → 10），其余尺寸保持原版不变。**

调查结论（数值来源链，纯 XML 驱动、无 DLL 硬编码）：

| 环节 | 位置 |
|---|---|
| 基数（金龙专属） | `Assets/XML/Civilizations/CIV4TraitInfos.xml:782` — `TRAIT_SPRAWLING` 的 `<iMaxCities>`，**保持原版 3 未动** |
| 挂载点 | `CIV4CivilizationInfos.xml:1676` — `CIVILIZATION_KURIOTATES` 的 `<CivTrait>TRAIT_SPRAWLING</CivTrait>`（**全 XML 仅此一处引用该 trait，无任何 leader 持有**） |
| 尺寸修正 | `Assets/XML/Gameinfo/CIV4WorldInfo.xml:163` — WORLDSIZE_HUGE 的 `<iMaxCitiesMod>`，**2 → 7** |
| 读取 | `CvPlayer.cpp:2528` — `setMaxCities(TraitInfo.getMaxCities() + WorldInfo.getMaxCitiesMod())` |
| 判定聚落 | `CvCity.cpp:289-293` — `getNumCities() - getNumSettlements() - 1 >= getMaxCities()` 则 `setSettlement(true)` |
| 界面提示 | `CvGameTextMgr.cpp:4723` — 同公式，Civilopedia/trait 悬浮说明自动跟着变，无需改文本 |

**为什么改 `iMaxCitiesMod` 只影响金龙**：该字段虽是全局按尺寸的修正，但公式中它只与 `TraitInfo.iMaxCities` 相加，且 DLL 仅在 `getMaxCities() != -1`（即该 trait 有真实上限）时才走这条分支；全 XML 中非 `-1` 的 `iMaxCities` **只有金龙的 TRAIT_SPRAWLING 一处**，其余 28 个 trait 均为 `-1`（无上限）。故改 HUGE 的 mod 实际只对金龙生效，其它文明零变化。

改动（共 3 处）：

| 文件 | 改动 |
|---|---|
| 安装版 `...\Mods\Fall from Heaven 2\Assets\XML\Gameinfo\CIV4WorldInfo.xml:163` | HUGE `iMaxCitiesMod` 2 → 7 |
| 仓库版 `Fall from Heaven 2/Assets/XML/Gameinfo/CIV4WorldInfo.xml:163` | 同上（git 管理） |
| 安装版 `...\Assets\XML\Civilizations\CIV4TraitInfos.xml:782` | 前一轮曾误改 3 → 6，**已按新口径回退为 3**（与备份逐字节一致） |

各地图尺寸最终上限对照（最终值 = 基数 3 + `iMaxCitiesMod`）：

| 地图尺寸 | iMaxCitiesMod | 原版 | 改后 | 是否变化 |
|---|---|---|---|---|
| DUEL 决斗 | -1 | 2 | 2 | 不变 |
| TINY 极小 | -1 | 2 | 2 | 不变 |
| SMALL 小 | 0 | 3 | 3 | 不变 |
| STANDARD 标准 | 0 | 3 | 3 | 不变 |
| LARGE 大 | 1 | 4 | 4 | 不变 |
| HUGE 巨大 | 2 → **7** | 5 | **10** | **翻倍** |

验证：三份 XML 全部 well-formed（minidom 解析）；diff 恰好 3 处——TraitInfos 对备份**零差异**（回退干净）、安装版 WorldInfo 仅 163 行、仓库版 WorldInfo 仅 163 行（git diff 中的 `iGridWidth/iGridHeight` 变化属并发的地图尺寸改造，非本条）；两份 WorldInfo 的 HUGE `iMaxCitiesMod` 均为 7。未新增类型/字段，**存档兼容**。

生效说明：`setMaxCities` 在 trait 挂载时算一次，老存档中玩家上限值已存入存档；**建议开新档验证**，老档可能仍持旧值。

备份：`CIV4TraitInfos.xml.bak-mod-20260726-213420`、`CIV4WorldInfo.xml.bak-mod-20260726-214052`（本次改动前的新时间戳备份，与地图尺寸改造的 `bak-mod-20260726-181346` 隔离）。仓库版 git 管理，未做 .bak。

## 改造 7：MM 侧王宫强化迁移（2026-07-26）

把改造 5（FFH2 侧 21 座王宫）迁移到 **MM（Magister Modmod）**。目标文件：
`C:\Civilization4\Beyond the Sword\Mods\Magister Modmod for FfH2\Assets\XML\Buildings\CIV4BuildingInfos.xml`
备份：`CIV4BuildingInfos.xml.bak-mod-20260726-220627`（同目录，改前逐字节校验 md5 一致）

**王宫数量：22 座**（MM 比 FFH2 多 1 座 —— `BUILDING_PALACE_MERCURIANS` 天使族王宫）。全部 22 座 `BuildingClass` 均为 `BUILDINGCLASS_PALACE`。`BUILDING_FORBIDDEN_PALACE`（L5373）/ `BUILDING_WINTER_PALACE`（L5600）/ `BUILDING_BONE_PALACE`（L17355）名字带 PALACE 但属其它 BuildingClass，**不在改造范围**，未动。

| 字段 | 原值 → 新值 | 座数 |
|---|---|---|
| `iDefense` | 0 → 200（21 座）；**25 → 225**（Infernal，与 FFH2 侧同样保留原生优势差） | 22 |
| `FreePromotion` | 空 `<FreePromotion/>` → `PROMOTION_BLESSED` | **20**（跳过 2 座，见下） |
| `bApplyFreePromotionOnMove` | 0 → 1 | **20**（同上） |
| `iFreeSpecialist` | 0 → 1 | 22 |

**跳过清单（原生已配 FreePromotion，按用户指令不覆盖）**：

| 王宫 | 原生 FreePromotion | 处理 |
|---|---|---|
| `BUILDING_PALACE_ELOHIM`（L1687） | `PROMOTION_COURAGE`（L1724） | 保留原值；`bApplyFreePromotionOnMove` 一并保持 0（改 1 会让原生勇气晋升的作用面变大，属越权改动），仅 `iDefense`/`iFreeSpecialist` 照常改 |
| `BUILDING_PALACE_GRIGORI`（L2050） | `PROMOTION_TEMPERANCE`（L2087） | 同上 |

**字段支持核实（MM 为 MNAI-U DLL，本地无 DLL 源码，证据强度＝schema 声明 + 既有使用实例）**：

| 字段 | schema 声明 | 既有使用实例 |
|---|---|---|
| `iDefense` | `CIV4BuildingsSchema.xml:166` 声明 + `:560` 序列位 | MM 内多处非王宫建筑已用非 0 值（如 L19762/19994/22378 的 25、L27912 的 10） |
| `FreePromotion` | `:209` + `:481` | MM 内 750 处 FreePromotion，其中 **2 处已用 `PROMOTION_BLESSED`**（L8572、L27833）——与本次写入值完全同型，最强证据 |
| `bApplyFreePromotionOnMove` | `:410` + `:627` | MM 内 **40 处**非王宫建筑已置 1（L7732/7991/8251/8511/8770 等） |
| `iFreeSpecialist` | `:140` + `:534` | BTS 原生字段，250 个建筑条目**全部**含该元素；`CIV4CivicInfos.xml:1560` 已用值 1 |

四项均支持，无需跳过任何字段。

**祝福晋升 Type 核实**：MM 的 `SPELL_BLESS`（`Assets/XML/Units/CIV4SpellInfos.xml:4758-4778`）走 Python 结果 `spellBless(pCaster, eSpell)`；`Assets/python/entrypoints/CvSpellInterface.py:9040` 定义 `def spellBless(pCaster, eSpell=-1, sProm='PROMOTION_BLESSED')` —— 确认授予 **`PROMOTION_BLESSED`**，与 FFH2 侧同名。该 Type 在 `Assets/XML/Units/CIV4PromotionInfos.xml:3832` 声明存在。

**改法（避免改造 4 的崩溃覆辙）**：全部为**改已存在元素的文本值**，未插入/删除/移位任何元素。关键点：20 座"无祝福"王宫的 `FreePromotion` 并非缺失，而是以**自闭合空标签** `<FreePromotion/>` 存在于 schema 正确位置（`FreeBuilding` 之后、`CivicOption` 之前，与 schema 序列 `:481` 一致），故 `<FreePromotion/>` → `<FreePromotion>PROMOTION_BLESSED</FreePromotion>` 属纯值替换，不改结构。文件按 latin-1 原字节往返读写，CRLF 与原编码保持不变。

**未迁移项**（用户裁决）：`iPlotRadius`（整项取消，见改造 5）；金龙城市上限（改造 6，属非首都改动且为 FFH2 谱系）。

**校验**：Python 3.12 `ElementTree` 解析 PASS（well-formed，250 个 BuildingInfo 全部解出，其中 22 座王宫）；diff 对备份恰好 **84 行** = `iDefense` 22 + `FreePromotion` 20 + `bApplyFreePromotionOnMove` 20 + `iFreeSpecialist` 22；改动行号区间 48–5349，**PALACE 区块外改动 0 行**；逐条回读 22 座的四字段值与预期（含 Infernal 225、ELOHIM/GRIGORI 保留原晋升且 onMove 仍为 0）**全部吻合，零 mismatch**；总行数与备份一致（无行增删）。

**存档兼容**：未新增任何类型，旧存档可读。但与改造 5 同理——`iDefense` 与 `iFreeSpecialist` 走 DLL `processBuilding` 增量缓存路径，**旧存档里已建成的王宫不会自动获得这两项加成，需开新档**；`FreePromotion` / `bApplyFreePromotionOnMove` 因每回合重算，旧档即时生效。

**边界遵守**：未碰 FFH2 目录、未碰 MM 的 `WorldInfo`/`TraitInfos`、未碰仓库 `MM源码/`（仅只读参考）、未碰整包备份 `Magister Modmod for FfH2.back`。同目录既有的 `CIV4BuildingInfos.xml.bak-mod`（2026-07-23 的原始备份）与 `.crashed-2140`（崩溃版留存）均未改动。

## 改造 8：史诗探索按地点冷却（scriptData 重实现）（2026-07-26）

**目标**：唯一史诗巢穴（`spellExploreLairEpic`）可重复探索，但每次探索完成后该**地点**进入冷却，冷却期内任何单位、任何玩家都不能再探索该地点；各史诗地点互相独立；普通一次性巢穴不受影响。

**作用范围（写/检分离）**：`ELCD` 标记的**写入点只有史诗路径** `spellExploreLairEpic`（全文件唯一 plot setScriptData 调用）；**检查**放在所有巢穴共用的入口 `reqExploreLair`，但普通巢穴地块永远没有标记，检查扑空即放行——所以冷却实际只作用于史诗地点，普通巢穴（本就探一次即毁）一切照旧。

**根因（旧实现为何无效，已废弃）**：上一版用 `pPlot.setTempImprovementType(iImp, iCooldown)` 把史诗地点自己的改良设回给自己来打冷却标记。MNAI DLL 的 `CvPlot::setTempImprovementType` 开头有守卫 `if (getImprovementType() != eImprovement)` —— 新旧改良相同时整个函数体被跳过，**计时器从未被设置**，于是 `reqExploreLair` 里的 `getTempImprovementTimer() > 0` 永不成立，冷却完全没生效。该 API 的本义是"临时替换成另一种改良、到期换回"，**不能用于原地冷却标记**。

**新实现（纯 Python，不动 DLL）**：冷却状态存进**地块 scriptData**（冷却属于地点，地块是天然载体，且随存档持久化）。

| 位置 | 改动 |
|---|---|
| `spellExploreLairEpic`（写） | 删除 `setTempImprovementType` 一行，改为 `pPlot.setScriptData(setEpicLairCooldownData(pPlot.getScriptData(), CyGame().getGameTurn() + iCooldown))` —— 存"重开回合"绝对值，非倒计时，无需逐回合维护 |
| `reqExploreLair`（读） | 上一版解开的 `getTempImprovementTimer` 判断**恢复为注释**（回到 MM 原生状态）；改为读 scriptData，`当前回合 < 重开回合` → `return False` |
| 新增两个模块级辅助函数 | `getEpicLairCooldownTurn(sData)` / `setEpicLairCooldownData(sData, iTurn)`，置于 `reqExploreLair` 之前 |

**冷却时长公式未改动**：`iCooldown = max(1, (20 * VictoryDelayPercent + 150) / 300)` —— 马拉松 20 回合为基线，按标准 `VictoryDelayPercent` 缩放（马拉松/史诗/标准/快速 = 20/10/7/4 回合）。

**scriptData 追加安全（关键设计约束）**：地块 scriptData 是共享字段，不能整体覆写。采用带前缀的键值段格式 **`ELCD:<重开回合>;`**（Epic Lair CoolDown），前缀先例为单位 scriptData 的 `FCHP:`。

- 写入：读出原值 → 若已有 `ELCD:` 段则**就地摘除该段**再追加新段（永不重复），其余内容原样保留（段前段后的外来数据都保留）
- 读取：`find` + 切片解析，无 `ELCD:` 段 / 无结束分号 / 值非数字 → 一律返回 -1 = **无冷却**（容错，坏数据只会放行不会误锁）
- 坏格式段在下一次写入时被自动修复为合法段
- 冲突核查：全 MM python 目录 grep 确认 `ELCD` 前缀无第二处使用；地块 scriptData 的唯一其它写入点是 `CvEventManager.py:11115` 的 WorldBuilder/调试控制台手动设值，非运行时功能，不会冲掉标记

**性能**：`reqExploreLair` 被 UI 高频调用（法术按钮可用性刷新），解析只用字符串 `find`/切片 + 一次 `int()`，无正则、无 pickle。

**语法/风格**：Python 2.4 兼容（无 `str.format`、无三元表达式、`except:` 裸捕获），注释纯 ASCII，制表符缩进与原文件一致。

**未改动项（用户明令禁改，本次全部遵守）**：死亡率、奖励概率、等级限制、原有探索资格判断（`isBarbarian` / `baseCombatStr` / `isPermanentSummon` / `getDuration` / `SPECIALUNIT` / `UNITCOMBAT_SIEGE` / `isPythonActive` / 地狱火与深渊分支 / AI 距城判断）一律原样；巧匠、教官概率未固定 100%；已放弃的等级与死亡率规则未重新加入；`CustomFunctions.py` 的坏档修复（缺逗号 + -1 检查）未触碰。普通巢穴走 `spellExploreLair`，不写 `ELCD:` 段，零影响。

**双份同步**：运行目录与仓库 `MM源码/` 两份 `entrypoints/CvSpellInterface.py` 做同一逻辑修改（非整文件覆盖 —— 两份存在本地化等既有无关差异，未消除也未扩大）。两个改动区域逐行 diff **完全一致**。

**校验**：改动函数块抽出后 `ast.parse` 语法 PASS（两份文件、两个块均通过）；把**生产文件里实际的**两个辅助函数抽出、接入桩测试跑 25 条断言（写标记→同回合拒绝→到期前拒绝→到期回合放行→重复探索段替换不重复→外来 scriptData 段前段后均完好→空/无标记/无分号/非数字/空值五种坏格式均降级为无冷却且不误锁→坏段自动修复→双地块互不影响）**全 PASS**；改动行非 ASCII 扫描 **0**；`git diff` 确认仅 3 个 hunk，全部落在 `reqExploreLair` 与 `spellExploreLairEpic` 两个函数内。

**存档兼容**：未新增类型、未改 DLL、未改 XML，旧存档可直接读。旧档中的史诗地点 scriptData 无 `ELCD:` 段 = 无冷却，首次探索后开始正常计冷却。

**备份**：运行目录 `CvSpellInterface.py.bak-mod-20260726-225600`；仓库靠 git。

**禁手方案（评估后弃用，2026-07-26）**：`pPlot.changeTempImprovementTimer(iCooldown - pPlot.getTempImprovementTimer())` 裸调计时器。表面有效（计时器确实设上、立即读回也通过、冷却期内确实拦截），实为延时炸弹：`isHasTempImprovement()` 的实现就是 `timer > 0`（`CvPlot.cpp:12829`），doTurn 每回合递减，**归零时执行 `setImprovementType(getRealImprovementType())`**——而绕过 `setTempImprovementType` 正规流程时 `m_eRealImprovement` 从未被设置（= NO_IMPROVEMENT），**冷却到期那回合史诗地点改良会被"还原"成空地、永久消失**。任何"临时改良计时器"相关 API 都不得用于原地标记。

**待实测**：本次为纯逻辑桩验证，游戏内实测（探索一次 → 冷却期内法术按钮**变灰**（`bDisplayWhenDisabled=1`，不是消失）→ 到期回合恢复可点；换单位/换玩家同样被拦）需开档确认。

## 改造 9：MM 极大地图再放大到 50×35（2026-07-27，**已撤销**）

> **撤销记录（同日）**：用户看到 28000 格超出全部实证规模、32 位内存风险最高的提示后，决定回退。现值已手动恢复 39×25（未用备份整文件覆盖）。50×35 版本存证于 `CIV4WorldInfo.xml.bak-mod-20260727-revert9-*`，日后想再上调可直接参考。以下为原始记录：

**目标**：用户玩 Big_and_Small（无自带 getGridSize，走 CIV4WorldInfo.xml 兜底）觉得不够大，把 MM 的 HUGE 档从 39×25 格块（156×100 地块）改为 **50×35 格块 = 200×140 地块**（28000 格）。

- 文件：`Mods\Magister Modmod for FfH2\Assets\XML\Gameinfo\CIV4WorldInfo.xml` 第 151-152 行，仅 iGridWidth/iGridHeight 两值，其余字段未动
- 影响面：MM 里所有**没有自带尺寸表**的地图脚本的 HUGE 档（Big_and_Small、Continents、Fractal 等）；自带 getGridSize 的（Erebus、PerfectWorld2、Totestra 等）不受影响
- 旧存档**不受影响**（地图尺寸在开局时写入存档，读档用存档内数据）；新开局生效
- 风险：28000 格已超过此前任何实证运行规模（此前最大 Big_and_Small 156×100=15600 实测正常），32 位进程后期内存与回合耗时风险最高的一档；崩了可回退备份
- 备份：`CIV4WorldInfo.xml.bak-mod-20260727-020751`；well-formed PASS
- 仓库 `MM源码/` 按只读基准先例未同步（MM 由安装包安装，不存在被仓库覆盖的风险）

## 改造 10：XML 兜底极大档 X+3/Y+2（2026-07-27，MM + FFH2 双侧）

改造 9 撤销后的温和方案：极大档格块 X+3、Y+2。

| MOD | 改前 | 改后 | 实际地块 |
|---|---|---|---|
| MM | 39×25 | **42×27** | 168×108 = 18144 |
| FFH2 | 48×30 | **51×32** | 204×128 = 26112 |

- 文件：两侧 `CIV4WorldInfo.xml` 第 151-152 行，仅 iGridWidth/iGridHeight；FFH2 仓库副本已同步（防 installpatch 覆盖），MM 仓库按只读基准不动
- 影响面：只影响无自带 getGridSize 的地图（Big_and_Small、Continents 等）的极大档；旧档不受影响，新开局生效
- 风险提示：FFH2 侧 26112 格接近改造 9 被否的 28000 规模，后期内存风险同级；MM 侧 18144 格温和
- 备份：两侧各 `.bak-mod-20260727-*`（改前值）；well-formed 三份全过

## 改造 11：伯兰娜加理财+僭夺特性（2026-07-27）

`LEADER_VOLANNA`（伯兰娜/沃兰娜，暗精灵）的 Traits 块追加 `TRAIT_FINANCIAL`（理财）与 `TRAIT_TOLERANT`（僭夺=可建被征服文明的单位），原有 `AGGRESSIVE`/`SCAVENGER` 保留，共 4 特性。

- 文件：MM `CIV4LeaderHeadInfos.xml`（LEADER_VOLANNA 条目内，diff 恰 8 行插入，重复元素追加不涉 schema 顺序风险）；well-formed PASS
- 特性判定是运行时动态查表（`hasTrait` 直读 LeaderHeadInfo），**重启后读旧档大概率即生效**；保险起见以新开局为准
- 备份：`CIV4LeaderHeadInfos.xml.bak-mod-20260727-*`

## 修复 1：CvEventManager 中文名 UnicodeEncodeError 崩溃修复（2026-08-04）

- 症状：单位创建等事件里 `str(unit.getName())` 遇中文名抛 `UnicodeEncodeError`（Python 2 的 `str()` 只认 ascii），游戏弹 Python Exception（用户截图：CvEventManager 行 5620 onUnitCreated）
- 修法：全文件 53 处（46 行）`str(x.getName())` → `x.getName().encode('latin_1','replace')`，与 CvSpellInterface 既有 YK-L10N 修法一致；这些串只用作随机种子/日志（另一处 Sluagh 命名为装饰性），玩法零影响，旧档即时生效
- 文件：MM `Assets\python\CvEventManager.py`（+ 仓库 `MM源码` 同步，两份改前字节一致）
- 工艺：rb/wb 字节级正则替换，CRLF 保持；逐行括号/引号配平校验通过
- 备份：`CvEventManager.py.bak-mod-20260804-115328`（改前字节）

## 改造 12：精灵强制宣战加态度门槛（2026-08-04）

- 背景：`CustomFunctions.py` `warScript`（约 5880 行）——末日计数 > 20 时，记分板排名较低的 AI 精灵（光明/暗任一方）对另一方**无条件**强制全面宣战：不看态度、不要求当前无战争，只受「和平已 ≥20 回合」节流，等于 AC>20 后两族精灵最多和平 20 回合
- 改法：宣战前加一层 `pPlayer.AI_getAttitude(iPlayer2) <= AttitudeTypes.ATTITUDE_ANNOYED`（不悦=1 或 愤怒=0 才触发；谨慎/满意/友好不再强制开战）。注释标记 `YK-MOD gaizao-12`
- 文件：MM `Assets\python\CustomFunctions.py`（+ 仓库 `MM源码` 同步）。注意：两份文件本有少量既有差异（仓库版含 convertToStr 等超前修改），故各自原地打同款补丁，未互相覆盖
- 生效：warScript 每 AI 回合执行，旧档即时生效；人类玩家本就不被脚本代宣战
- 备份：`CustomFunctions.py.bak-mod-20260804-115328`（改前字节）

## 改造 13：植树可在己方城市格施放（限精灵/库里奥塔特）（2026-08-04）

- 需求：原本就能在设施上植树的文明（光明精灵、暗精灵、库里奥塔特），追加「可对自己的城市格植树」；其他文明规则一律不变（精灵坐城保林是单向的，空地坐城后原本无法补种）
- 改法：reqBloom / reqBloomGreater 各加一处己方城市格旁路：施法者文明属三族之一、城市为施法者本人所有、格上无现存地貌、非山峰/水域、地形可长新森林（DLL canHaveFeature 对城市格恒 false，故手动校验）。注释标记 YK-MOD gaizao-13，每份文件 2 处
- 修订史：首版（当日 13:27）误将范围扩为「任何文明可在己方领土设施上植树/育林」（8 处），按用户澄清于 20260804-133137 回退重做为现行 2 处版本；v1 有备份存证
- 施法者提示：植树挂在自然魔法 II（法师线；树人站成熟森林自动获得），范围版需自然亲和；法术 bDisplayWhenDisabled=0，条件不满足时按钮整体隐藏而非置灰
- 已知不确定点：城市格上的幼林能否自然长成森林/远古森林由 DLL 侧成长逻辑决定，待实测；若不成长可再加 python 兜底（城内育林 Bloom2/3 本就可用：城市格设施为 -1 走白名单，精灵领土判定放行）
- 文件：MM entrypoints\CvSpellInterface.py（+ 仓库 MM源码 同步；两份基线略有差异，各自原地打补丁）
- 生效：req 每次点单位即时求值，旧档即时生效
- 备份：CvSpellInterface.py.bak-mod-20260804-132746（原版）；CvSpellInterface.py.bak-mod-20260804-133137（v1 存证）

## 改造 14：金龙族极大地图正城上限 5→7（2026-08-04，MM 侧）

- 需求：用户观察 AI 金龙正城偏少；经查改造 6 只改了 FFH2 侧，MM 侧极大档仍为 基数3+修正2=5
- 改法：MM `Assets\XML\Gameinfo\CIV4WorldInfo.xml` WORLDSIZE_HUGE `<iMaxCitiesMod>` 2→4，上限 5→7（用户定稿 7，非对齐 FFH2 的 10）
- 影响面：与改造 6 同理，全 XML 非 -1 的 `iMaxCities` 仅金龙 TRAIT_SPRAWLING 一处，其余文明零变化；只动极大档
- 生效：`setMaxCities` 开局计算（FFH2 DLL CvPlayer.cpp:2528，MNAI-U 推定同构），**旧档不生效，需新开局**
- 备选方案处置：定居点文化缓增/金币/人口、AI 自动转正——经讨论全部放弃（定居点成长是 DLL 硬锁且经济清零，人口增益无实义；AI 转正原生已有 iAIWeight=300 的技能）。相关草稿补丁未写盘
- 仓库：MM源码 按只读基准不动（沿改造 10 口径）
- 备份：`CIV4WorldInfo.xml.bak-mod-20260804-185121`（改前值，HUGE mod=2）

## ~~改造 16~~：附庸制度新规（已撤销）

> **2026-08-05 撤销**：因 MM 无 DLL 源码，本条只能实现为"附庸成立瞬间自动解除"（事后强制），无法做成真正的"请求时条件"（AI 报价弹窗无法拦截、玩家会经历接受→瞬间撤销）。用户评估该实现形态无价值，裁定撤销。游戏目录与仓库的 `CvEventManager.py` 均已还原至改造前（587,881 字节，即 `.bak-mod-20260805-134545`）；改造版代码留存于 `.bak-mod-20260805-135045`（初版 590,551）与 `.bak-mod-20260805-140014-revert16`（rev2 590,545）备查。经验教训：**动手前先向用户完整说明实现形态与局限，确认价值后再写入**。


- **日期**：2026-08-05
- **动机**：研究封建制度后大量 AI 涌来请求做和平附庸，希望提高附庸门槛：和平附庸必须先有长期互不侵犯关系；同时限制每个宗主只能拥有一个附庸（参考永久同盟"共同防御 40 回合"的设计）。
- **规则口径**（用户确认，rev2 修订）：
  1. **和平附庸**双重前置：(a) 宗主当前没有任何附庸（和平与屈服附庸都占名额）；(b) 双方现存互不侵犯条约（`TRADE_NON_AGGRESSION`）已连续生效 **≥ 40 回合**（按 `getInitialGameTurn()` 计算，多份取最早）。
  2. **屈服附庸（战场打服，`TRADE_SURRENDER`）完全豁免**：成立时不检查任何条件（rev2：用户裁定"被迫投降不看宗主是否已有附庸"），但成立后同样占用名额、会挡住后续的和平附庸。
  3. 曾讨论的"永久同盟的附庸视同己方附庸"用户裁定放弃（实现过重）。
- **实现方式**：MM 无 DLL 源码，无法修改 `CvTeamAI::AI_vassalTrade` 报价/接受判定；改为 **事后强制执行**：`CvEventManager.onVassalState`（`vassalState` 事件，附庸关系成立瞬间触发）中审查上述规则，不合规立即 `gc.getTeam(iMaster).freeVassal(iVassal)` 解除（DLL 端会销毁含 `TRADE_VASSAL`/`TRADE_SURRENDER` 的条约），并向涉事人类玩家弹中文提示（\u 转义存储，文件保持 ASCII）。判定细节：屈服/和平之分与互不侵犯条约龄期均通过遍历 `CyGame().getDeal()` 的条约项（`TradeData.ItemType`）确定；API（`freeVassal`/`isHasNonAggression`/`getInitialGameTurn`/`TradeTypes.TRADE_NON_AGGRESSION` 枚举导出）已对照 MNAI 系 DLL 源码逐一核实存在。
- **已知局限**：
  - AI 的附庸**报价弹窗无法拦截**（DLL 层），玩家接受后若不合规会立即解除并提示；AI 之间的不合规附庸也会在成立瞬间被静默解除（无人类涉事时不弹消息），AI 可能反复尝试。
  - 互不侵犯条约若中途断签重签，龄期按**现存条约**重新起算（不做跨条约累计）。
  - 该逻辑即时生效（Python 实时读取），旧档同样适用；存档中已存在的附庸关系不受追溯，仅约束新成立的关系。
- **改动文件**：
  - 游戏目录 `Assets\python\CvEventManager.py`（onVassalState 重写，+69 行；改前 587,881 → 改后 590,551 字节；备份 `.bak-mod-20260805-134545`（初版前）、`.bak-mod-20260805-135045`（rev2 前，590,551 字节初版存证）；rev2 后 590,545 字节）
  - 仓库 `MM源码/Assets/python/CvEventManager.py` 同步同一补丁（git 管理，无 .bak）
- **回退**：还原备份文件即可。

## 改造 17：史诗探索冷却统一常量化（当前 1 回合）

- **日期**：2026-08-05
- **动机**：用户希望把改造 8 的史诗巢穴冷却收敛为单一可调变量，并暂时设为 1 回合以便集中刷探索（授环者巧匠/大吉奖池）。
- **改动**（rev2 按速度分档）：`CvSpellInterface.py` 顶部（ELCD 辅助函数上方）新增按速度分档表 `EPIC_LAIR_COOLDOWN_BY_SPEED = {GAMESPEED_MARATHON/EPIC/NORMAL/QUICK: 各一值，现均为 1}` 与兜底 `EPIC_LAIR_COOLDOWN_DEFAULT = 1`；`spellExploreLairEpic` 中原速度缩放公式 `max(1, (20*VictoryDelayPercent+150)/300)`（等效马拉松 20/史诗 10/普通 7/快速 4，已在注释中保留）替换为按当前速度查表。初版单一常量 `EPIC_LAIR_COOLDOWN_TURNS`（备份 `.bak-mod-20260805-171043` 存证）已被本表取代。
- **生效方式**：Python 实时读取，旧档立即生效。注意存档中已写入的 `ELCD:` 印记存的是"解锁回合"绝对值，改动前探索过的点仍按原冷却走完剩余回合；此后新的探索一律 1 回合冷却。
- **调整方法**：按速度改表中对应值即可（恢复原版行为：马拉松 20/史诗 10/普通 7/快速 4）。
- **改动文件**：游戏 `Assets\python\entrypoints\CvSpellInterface.py`（1,732,785 → 1,732,853 字节；备份 `.bak-mod-20260805-170829`）；仓库 `MM源码` 同名文件同步（1,731,547 → 1,731,615）。
- **已知边界**：织锦屋/游荡城堡等专属结算函数依旧不走冷却（既有口径，见改造 8 相关记录）。

## 改造 18：世界编辑器可操作「隐藏建筑」（敌对版神殿等）

- **日期**：2026-08-06
- **动机**：用户城里出现「教会堂（敌对）」等敌对版宗教建筑，想删掉却在世界编辑器（Platy Builder）里根本选不到。
- **根因**（已核 XML + WB 源码）：敌对版建筑 `bGraphicalOnly=1`，且与友好版**共用同一 BuildingClass**（例：`BUILDING_TEMPLE_OF_THE_ORDER` 与 `..._HOSTILE` 同属 `BUILDINGCLASS_TEMPLE_OF_THE_ORDER`，DefaultBuilding 为友好版）。Platy WB 的建筑列表有两道过滤：①`bHideInactive`（默认开）只放行 `getCivilizationBuildings(class) == i` 的那一个，即友好版；②分类归属上 `bGraphicalOnly` 的条目只进「显示隐藏选项」和「全部」。两道叠加后敌对版在任何视图下都不可见、无法点击。全 MOD 共 250 座建筑，其中 51 座 `bGraphicalOnly`，17 座同时带 `ReligionType`（16 座敌对版神殿 + 警戒大教堂）。
- **改动**：
  - `WBBuildingScreen.py`（城市建筑编辑页）：`bHideInactive` 过滤加例外——`bGraphicalOnly` 的建筑、以及**本城已实际拥有**的建筑一律放行；另在分类归集处，让 `bGraphicalOnly` 且 `ReligionType != -1` 的建筑同时进入「宗教建筑」列表（原先只进「显示隐藏选项」）。
  - `CvPlatyBuilderScreen.py`（左侧「建筑」刷子模式）：同样对 `bGraphicalOnly` 放行 `bHideInactive` 过滤，使「显示隐藏选项」分类真正可用。
- **效果**：世界编辑器里进城市建筑页，选「宗教建筑」或「显示隐藏选项」分类即可看到「XX（敌对）」条目，点击切换增删；**无需**再去关掉"隐藏未启用"开关。删除走 WB 原有 `setNumRealBuilding`，与控制台 `pCity.setNumRealBuilding(iBuilding, 0)` 等价。
- **生效方式**：纯 UI 层 Python，实时生效，旧档可用；不影响任何游戏规则与 AI。
- **改动文件**：
  - 游戏 `Assets\python\Screens\PlatyBuilder\WBBuildingScreen.py`（23,090 → 23,761 字节；备份 `.bak-orig-20260806-172142`）
  - 游戏 `Assets\python\Screens\PlatyBuilder\CvPlatyBuilderScreen.py`（107,958 → 108,184 字节；备份 `.bak-orig-20260806-172142`）
  - 仓库 `MM源码/Assets/python/Screens/PlatyBuilder/` 下同名两文件同步（git 管理，无 .bak）
- **回退**：还原两个 `.bak-orig-20260806-172142` 备份即可。
- **相关机制备忘**：敌对/友好版切换由 `CvEventManager.onBuildingBuilt`（建成时判定）与 `onPlayerChangeStateReligion` / 阵营变更（塔莉事件）时的逐城重判负责，判定条件各建筑不同（例：工造坊＝国教授环者 或 善良阵营 或 至善政策；教会堂＝国教秩序 或 善良阵营）。敌对版数值实为负资产（教会堂敌对版：陆军产能 −20%、军事产能 −10%、商业 −20%、革命指数 +1、无维护费减免/牧师位/国教快乐），但在神赐之力（Arda）计分中仍按其 `ReligionType` 参与城市项。审判官净化宗教也能摧毁敌对版（走 `PrereqReligion` 匹配，圣城与世界奇迹除外）。

## 改造 19：三桅战舰 / 主力舰恢复运兵能力（载量 3）

- **日期**：2026-08-07
- **动机**：用户发现三桅战舰装不了陆军、只能挂一只猎鹰，怀疑是 bug。
- **核查结论**（FFH2 原版 vs MM 逐条对比 `CIV4UnitInfos.xml`）：是 MM 的**有意改动**，不是运行时故障。
  - FFH2 原版：三桅战舰 `iCargo=2 / DomainCargo=DOMAIN_LAND / SpecialCargo=(无)`；主力舰同。
  - MM 改为：`iCargo=1 / DomainCargo=DOMAIN_AIR / SpecialCargo=SPECIALUNIT_BIRD`——DLL `CvUnit::cargoSpaceAvailable` 里这两个字段非空即为硬门槛，必须完全匹配，故只有 `UNIT_HAWK`（DOMAIN_AIR + SPECIALUNIT_BIRD）能上船。
  - 战略/百科文本未同步修改（仍写"用来运载单位"、"可运载 36 个军人"），是误导来源。
  - 全表比对：**MM 只把这两艘从 2 降到 1**，其余船只全为上调（大帆船 3→5、皇后级巨舰 6→10、魔法驳船 1→3、水手挽歌 3→4、桨帆船 0→3、飞艇 6→10），并新增铁甲舰 15 / 特洛伊木马 8 / 商船 2 / 走私船 1 / 扭曲气泡 21 / 水元素 5（载海军）。判断为"运兵职能从战斗主力舰剥离、交给专职船"的设计取向。
- **改动**：`UNIT_FRIGATE`、`UNIT_MAN_O_WAR` 各 3 个字段（仅改已有元素的值，无插入/删除，符合 schema 顺序约束）：
  - `<SpecialCargo>SPECIALUNIT_BIRD</SpecialCargo>` → `NONE`
  - `<DomainCargo>DOMAIN_AIR</DomainCargo>` → `NONE`
  - `<iCargo>1</iCargo>` → `3`
  - 取 `NONE`（而非 `DOMAIN_LAND`）是因为单字段无法表达"陆地或空中"；置空后陆军与猎鹰都能装载，为用户指定的兼容方案。文件中本就存在 `<DomainCargo>NONE</DomainCargo>`（3 处）与 `<SpecialCargo>NONE</SpecialCargo>`（4 处），写法经过验证。
- **生效方式**：单位定义类字段，Python/DLL 实时读取，**旧档立即生效**，无需新开局。
- **已知副作用**：`DomainCargo` 置空后，理论上海军单位也可手动装载进这两艘船（DLL 只在"载具与货物的 specialCargo 和 domainCargo 完全相同"时拒绝，见 `CvUnit::canLoadUnit` 中 Denev 2009/12/08 的防飞艇套娃补丁）。同型船互装仍被拒绝；AI 不会主动这么做。若不希望如此，把两处 `DomainCargo` 改回 `DOMAIN_LAND` 即可（代价是不能再挂鹰）。
- **改动文件**：游戏 `Assets\XML\Units\CIV4UnitInfos.xml`（2,024,381 → 2,024,345 字节；备份 `.bak-mod-20260807-064513`；此前已有无时间戳的 `.bak-mod` 充当原版存证）；仓库 `MM源码/Assets/XML/Units/CIV4UnitInfos.xml` 同步。
- **回退**：还原 `.bak-mod-20260807-064513` 即可。
- **未做**：战略/百科文本未修订（`TXT_KEY_UNIT_FRIGATE_STRATEGY` 等仍是原版口径，现在反而与改后行为一致了）。

## 改造 20：移除「附庸边境压制」（DLL 二进制补丁）

- **日期**：2026-08-07 15:35（Asia/Shanghai）
- **动机**：用户观察到附庸国的边境被宗主"吃掉"，希望恢复成正常的纯文化判定。
- **机制根因**（EMM/MNAI 源码 `CvGameCoreDLL/CvPlot.cpp` 4450–4545，BtS 原版即有）：
  - `CvPlot::calculateCulturalOwner()` 先按文化算出 `eBestPlayer`（还需 `isWithinCultureRange`）。
  - 随后对**非城市格**（整段包在 `if (!isCity())` 内，故城市本身不会被吞）扫描半径 3 的 37 格大十字，候选城市 = `eBestPlayer` 本队 **或 `eBestPlayer` 所臣服的宗主队**（`GET_TEAM(...).isVassal(pLoopCity->getTeam())`）。
  - 取 `GC.getCityPlotPriority()` 最小者，且**自家城市 +5 惩罚**（源码注释：`priority ranges from 0 to 4 -> give priority to Masters of a Vassal`）。FfH 把半径从 2 扩到 3，优先级表变成 环0=0 / 环1=1,2 / 环2=3,4 / 环3=5,6,7（`CvGlobals.cpp:370`），所以宗主城市在 2 格内必赢，第 3 圈时部分位次才打平。
  - 单向：候选集不含"本方的附庸"，宗主永远不会被附庸反吃。
  - `CvTeam::setVassal()`（`CvTeam.cpp:5790`）在改完标志位后对双方全部地块 `updateCulture(true,false)`，故签约/解约当场重画边界。
  - 实际代价：`CvPlot::updateWorkingCity()` 要求工作城市与地块主人同属一人（`CvPlot.cpp:7527`），被吞的格子附庸城市不能耕。
- **为何只能改 DLL**：MM 只发布编译好的 `CvGameCoreDLL.dll`，不含源码；`CvGlobals.h` 的 `USE_*_CALLBACK` 系列没有地块归属回调，Python 层无钩子；纯 Python 补偿（每回合改写归属或清零宗主文化）会被同回合的 `doPlotCulture` 反复覆盖，且有归属抖动风险，已否决。
- **定位方法**（无符号表，纯静态分析，可复现）：
  1. 导出表 `?getInstance@CvGlobals@@SAAAV1@XZ` → 全局 `gGlobals` 位于 `0x10556830`。
  2. 导出表 `?getCityPlotPriority@CvGlobals@@QAEPAHXZ`（RVA `0x20FC50`）函数体为 `mov eax,[ecx+0xB0]` → 成员偏移 `+0xB0`。
  3. 优先级数组绝对地址 = `0x105568E0`；全 `.text` 段仅 2 处引用（`0x1020803B` = 本函数，`0x1020CE5E` = `updateWorkingCity`）。
  4. `0x1020803B` 附近可见 `cmp eax,0x25`（37 格循环）、`add eax,5`（+5 惩罚）、`m_abVassal[]` 内联查表，确认即目标。
- **补丁内容**（文件偏移 = RVA，因 `.text` 的 `VirtualAddress` 与 `PointerToRawData` 同为 `0x1000`）：

  | 偏移 | 改前 | 改后 | 含义 |
  |------|------|------|------|
  | `0x00207FFE` | `8B 0D 28 68 55 10` (`mov ecx,[10556828]`) | `EB 67 90 90 90 90` (`jmp 10208067` + 4×nop) | 队伍不同 → 直接 continue，不再查 isVassal |

  等价于原版中根本没有这条附庸规则。后续 `add eax,5` 只会对同队候选统一生效，相对顺序不变，自动失效，无需第二处改动。
- **安全核验**：落点 `0x10208067` 是原有合法指令边界（原"非宗主"分支的目标）；全函数区扫描确认**无任何分支落入** `0x10207FFE–0x10208021` 的死代码；全文件比对**仅 6 字节不同**；大小仍 6,111,232 字节；PE 头 `CheckSum` 原本即为 0，未改。
- **校验值**：原版 `04eeb7bba7ca81ecbce2e4c0a92dbb44804db2271401b7fe2cffcf9e5686e21e`；补丁 `866597a31cf23c18944ca4df07010b960579fa51dc395ef918bad71c9a306876`。
- **文件**：`<MM>\Assets\CvGameCoreDLL.dll`；原版存证 `CvGameCoreDLL.dll.bak-orig-20260807-153551`（同目录，已核验 sha256 与原版一致）。补丁脚本 `patch_vassal_border.py` 带字节校验与 `--revert` 还原。
- **影响面与限制**：
  - 对全图所有宗主-附庸关系生效，AI 之间同样；不区分对象（规则本身不带对象参数，无法只对自由殖民地生效）。
  - 存档格式未变，老档可继续读；读档后不会立刻回弹，需等地块下次文化刷新（每回合 `doPlotCulture`），约 1–2 回合内边界长回去。
  - 多人联机时对方若为未打补丁的 DLL 会 OOS。
  - 宗主的 `getTotalLand()` 会随之减少，间接影响附庸实力评估（`setMasterPower`/`setVassalPower`）。
- **回滚**：复制 `.bak-orig-20260807-153551` 覆盖回 `CvGameCoreDLL.dll`，或 `python patch_vassal_border.py --revert <补丁DLL> <输出>`。

## 改造 21：阿尔达调整（灰色议会惩罚减弱 + 等级/阶级加成）

- **日期**：2026-08-09 07:11（Asia/Shanghai）
- **动机**：① 灰色议会一旦铺开，周边城市对**所有其他宗教**的祭司施加 −7 阿尔达，压制过强；② 原算法完全不看单位本身，一个 1 级见习祭司和一个 10 级大祭司阿尔达完全相同，缺乏成长感。
- **机制定位**（MM 自有 Python，未涉及 DLL）：
  - `CvSpellInterface.effectArda(pCaster)`（约 1745 行起）是本体，`helpEffectArda(lpUnits, eSpell)`（约 3070 行起）是**逐行复制的第二份**，只多了 `szBuffer` 提示文本。两处算法必须同步。
  - 阿尔达基数 `iArda = 40`；`dReligionAdjustments` 是「其他宗教对我的阿尔达修正」表，先给默认值，再按 `iReligionCaster` 分支整体覆盖。
  - 该表在三处被消费：本方国教（仅正值生效，+3/+3 加成）、地块主人的国教（交战再 −5/−5）、以及半径内每座城市所含宗教（按距圣城/距城市的距离百分比缩放后累加）。
  - 末尾 `iArda // 10` 夹到 0–9，映射 `PROMOTION_ARDA0..ARDA9`；>100 走 ARDA10，<0 走 ARDA0 并可能触发脱冕/叛教分支。
  - 阿尔达等级效果见 `arda_reference.html`：ARDA0 = 战力 −100%/施法失误 +200%，ARDA5 = 中性，ARDA10 = 战力 +100%/失误 −100%。**每 10 点阿尔达 = 1 个档位**。

### 改动 1：灰色议会惩罚 −7 → −1

- 全文件 `RELIGION_GREY_COUNCIL') : -7,` 共 **42 处**（`effectArda` 21 处 + `helpEffectArda` 21 处，即每个宗教的分支表里各一条），统一改为 `-1,`。
- **未动**：灰色议会自己分支里的 `RELIGION_GREY_COUNCIL : 10`（2 处，行 2271/3596 附近），本教自我加成保持不变。
- 其余宗教的 `-17`（众母神）、`-21`（太一之子）等数值一律未动。

### 改动 2：加入等级与阶级加成

在两处 `iArda = 40` 之后各插入：

```python
		#改造 21：单位等级与阶级加成（等级 x1，阶级 x3）
		iLevelArda = pCaster.getLevel()
		iTierArda = 3 * gc.getUnitInfo(pCaster.getUnitType()).getTier()
		iArda += iLevelArda + iTierArda
```

`helpEffectArda` 侧额外追加一行提示（复用既有文本键，不新增 XML）：

```python
		if iLevelArda + iTierArda != 0:
			szBuffer += localText.getText("TXT_KEY_TXT_ARDA_FROM", (iLevelArda + iTierArda, pCaster.getName(), ))
```

- `getTier()` 已由 DLL 导出到 Python（`CyInfoInterface1.cpp:475`），且 MM 自身在 `CustomFunctions.py:722/5000`、`CvEventManager.py:3865`、`CvSpellInterface.py:4528/4987` 已多处调用，兼容性无疑问。
- 数量级参考：祭司 `iTier=3`、大祭司 `iTier=4`（天使 3、炽天使 4、煽动者 3）。所以 1 级祭司 +10（3×3+1），5 级大祭司 +17，10 级大祭司 +22 —— 约合 **+1 到 +2 个阿尔达档位**。

- **影响面**：`effectArda` 对所有走阿尔达的单位生效（各教祭司/大祭司、天使系等），不限于某一宗教；被排除在阿尔达体系外的（无宗教、众母神、太一之子、巨龙崇拜、洛基/树人/丑角/布鲁哈/不静之影、带巨龙晋升者）不受影响。
- **文件**：`<MM>\Assets\python\entrypoints\CvSpellInterface.py`（1,733,146 → 1,733,703 字节）；仓库同步 `<repo>\MM源码\Assets\python\entrypoints\CvSpellInterface.py`（1,731,908 → 1,732,465 字节）。
- **备份**：`CvSpellInterface.py.bak-mod-20260809-071146`（游戏目录，1,733,146 字节，已核验落盘）。仓库侧受 git 管理，未留 .bak。
- **校验**：改动共 94 行（42×2 数值 + 4 行计算块 + 6 行提示块）；两个产物均通过 `lib2to3` 的 **Python 2 语法解析**；CRLF 行尾与制表符缩进保持原样。
- **回滚**：把 `.bak-mod-20260809-071146` 覆盖回 `CvSpellInterface.py` 即可；仓库侧 `git checkout` 该文件。

## 改造 22：阿尔达「阶」改用祭祀等级 + 经验半点制（修订改造 21）

- **日期**：2026-08-09 07:25（Asia/Shanghai）
- **动机**：改造 21 用 `iTier` 当「阶」是**误判**。`iTier` 是全 MOD 通用的强度档（0–8，589 个单位都有），不是神职阶级，实测有硬伤：
  - 不公管理者（Stewards of Inequity）**整条线 `iTier=0`**（赌徒 / 食利者 / 亲信），主教也吃 +0，而别家主教吃 +12。
  - 狐人祭司 `iTier=2`（和别家**信徒**同级），但狐人主教是 4，中间断一档。
  - 少数英雄 `iTier=5`（勒忒 / 斯塔提乌斯 / 特里斯坦 / 伊夫利特）、`iTier=7`（恩巴尔），会白吃 +15 / +21。
- **术语澄清**：汉化里的「主教」就是 **High Priest / 大祭司** 这一级（森林主教 = `UNIT_HIGH_PRIEST_OF_LEAVES`、天穹主教 = `..._OF_THE_EMPYREAN`、寒冰主教 = `..._OF_WINTER`）。基础 FfH2 时代的 `UNIT_PRIOR`（圣堂主教）/ `UNIT_PROFANE`（亵渎主教）/ `UNIT_RUNEKEEPER`（符文主教）/ `UNIT_SPEAKER`（言灵主教）在 MM 的 `CIV4UnitInfos.xml` 中**已不存在**（计数为 0），仅文本键作为遗留残留，统一改叫 `UNIT_HIGH_PRIEST_*`。

### 改动 1：「阶」改为祭祀等级 0 / 3 / 6

改用**晋升**判定，而不是 `iTier` 数据表：

```python
		if pCaster.isHasPromotion(gc.getInfoTypeForString('PROMOTION_DIVINE2')):
			iRankArda = 6
		elif pCaster.isHasPromotion(gc.getInfoTypeForString('PROMOTION_DIVINE')):
			iRankArda = 3
		else:
			iRankArda = 0
```

- 依据：MM 的 `CIV4UnitInfos.xml` 里，**信徒**无 DIVINE、**祭司**带 `PROMOTION_DIVINE`、**主教/大祭司**带 `DIVINE + DIVINE2`，全 20+ 个宗教一致，无例外。
- 用 `isHasPromotion`（运行时状态）而非 UnitInfo 查表，因此众母神叛教分支剥掉 `PROMOTION_DIVINE` 后阶级会同步掉回 0，语义自洽。
- 只带 `DIVINE2` 不带 `DIVINE` 的少数单位（守护藤蔓、盲眼兄弟、欢乐舞者、羽蛇、炽天使、奥瑞克飞升、忿怒、戈西亚、海博伦、灰阳、凯泽夫、索凯德、恩巴尔）按主教级 6 计。

### 改动 2：经验改为每等级 0.5，不预先取整

```python
		iLevelArda = pCaster.getLevel() / 2.0
		iArda += iRankArda + iLevelArda
```

- 用 `2.0` 而非 `2`：Python 2 的整数除法会把 5 级压成 2，损失半点；浮点保留半点一路累加到最后。
- **配套必改**：收尾把阿尔达折成档位索引时必须转回整数，否则 `list.pop(float)` 在 Python 2 直接抛 TypeError：

```python
			iArda = int(iArda)//len(listArdas)      # 原为 iArda//len(listArdas)
```

  两个函数各一处，共 2 处。`if iArda > 100` / `elif iArda < 0` 这两个比较对浮点天然安全，未动。
- 提示文本里显示的加成用 `int(...)` 包一层，避免浮点进 `%d` 槽位。

### 数量级对照（基数 40，每 10 点 = 1 个阿尔达档位）

| 单位 | 阶 | 经验 | 合计 | 约合 |
|---|---|---|---|---|
| 信徒 1 级 | 0 | +0.5 | +0.5 | 0 档 |
| 祭司 1 级 | 3 | +0.5 | +3.5 | 0 档 |
| 祭司 6 级 | 3 | +3 | +6 | 0~1 档 |
| 主教 1 级 | 6 | +0.5 | +6.5 | 0~1 档 |
| 主教 10 级 | 6 | +5 | +11 | +1 档 |
| 主教 20 级 | 6 | +10 | +16 | +1~2 档 |

比改造 21（主教 1 级即 +13）温和很多，成长几乎全部来自经验。

- **文件**：`<MM>\Assets\python\entrypoints\CvSpellInterface.py`（1,733,703 → 1,734,114 字节）；仓库同步（1,732,465 → 1,732,876 字节）。
- **备份**：`CvSpellInterface.py.bak-mod-20260809-072541`（= 改造 21 状态，1,733,703 字节）。
- **校验**：diff 共 4 段、22 行；两个产物均通过 `lib2to3` 的 Python 2 语法解析；CRLF 与制表符缩进保持原样。
- **未动**：改造 21 的第一项（灰色议会 −7 → −1，42 处）保持生效。

## 改造 23：灰色议会惩罚回调 −3 + 阿尔达退回整数运算（修订改造 21/22）

- **日期**：2026-08-08 18:03–18:06（Asia/Shanghai）
- **动机**：① 改造 21 把灰色议会惩罚从 −7 直接砍到 −1，用户实测认为削过头（灰色议会本就近乎免疫他教影响——它自己的 `dReligionAdjustments` 只列 4 条：自身 +10、巨龙崇拜 −2、众母神 −17、太一之子 −21，其余二十余教全走默认不影响它；而它对**所有**其他宗教都有一条负值，这个不对称是刻意设计），回调到 −3。② 悬浮提示里出现 `1110048768` 这种天书数字。

### 改动 1：灰色议会 −1 → −3

- 全文件 `RELIGION_GREY_COUNCIL')\t\t\t:\t-1,` 共 **42 处**（`effectArda` 21 + `helpEffectArda` 21）统一改为 `-3,`。
- **未动**：灰色议会自身分支里的 `: 10`（2 处）；其余宗教的 −17（众母神）/ −21（太一之子）等一律未动。
- 字节数不变（−1 与 −3 等长）。

### 改动 2：阿尔达退回整数运算（修显示 BUG，非打补丁）

- **根因**：改造 22 把等级加成写成 `pCaster.getLevel() / 2.0`，`iArda` 由此变成**浮点**。Civ4 的 `localText.getText` 走 C++ 层，`%d` 槽位拿到 Python float 时不做转换，**直接把 4 字节位模式当整数读出**——浮点 42.5 的 IEEE754 位模式恰好就是 `1110048768`（已用 `struct.pack/unpack` 验证）。
- **修法口径（用户 2026-08-08 拍板）**：*"修法是参考原来无 BUG 的写法，而不是打补丁。"* 原版无 BUG 的写法就是 **`iArda` 全程整数**，`%d` 自然永远正确、收尾也不需要任何 `int()` 保护。故不在 `getText` 处包 `int()`（那只是堵漏，`iArda` 流到新位置还会再漏），而是**从源头消除浮点**。
- 用户明确要求**向下取整、且整数相除默认就是**，故用 `/ 2`（Python 2 整数除法天然向下取整），不引入 `math.floor` 等额外写法。

| 位置 | 改前（改造 22） | 改后（回归原版形态） | 处数 |
|---|---|---|---|
| `effectArda` / `helpEffectArda` | `iLevelArda = pCaster.getLevel() / 2.0` | `... / 2` | 2 |
| 两处收尾 | `iArda = int(iArda)//len(listArdas)` | `iArda = iArda//len(listArdas)` | 2 |
| `helpEffectArda` 提示行 | `(int(iRankArda + iLevelArda), pCaster.getName(), )` | `(iRankArda + iLevelArda, ...)` | 1 |

  后两组是改造 22 为兜底浮点而加的**补丁**（当时为躲 `list.pop(float)` 的 TypeError），源头去掉浮点后一并拆除，代码回到原版形态。

- **数值影响**：等级加成由半点制变为每 2 级 +1 且向下取整。1 级 +0、2–3 级 +1、10 级 +5、20 级 +10。主教 10 级合计 6+5=11，与改造 22 的 11 相同；奇数级比改造 22 少 0.5（如 5 级由 +2.5 变 +2）。阿尔达每 10 点 1 档，此差异不足以跨档。
- **文件**：游戏 `<MM>\Assets\python\entrypoints\CvSpellInterface.py`（1,734,114 → 1,734,095 字节）；仓库 `MM源码` 同步（1,732,876 → 1,732,857）。各缩 19 字节（2×2 + 2×5 + 5，与拆除字符数吻合）。
- **备份**：`.bak-mod-20260808-180325`（= 改造 22 状态，1,734,114 字节）、`.bak-mod-20260808-180535`（= 灰议 −3 已改、浮点未改，1,734,114 字节）。仓库侧受 git 管理，未留 .bak。
- **校验**：两份均通过 `lib2to3` 的 **Python 2 语法解析**；CRLF 39,623 行、裸 LF **0**、制表符缩进保持；残留 `getLevel() / 2.0` = 0、`int(iArda)` = 0、`int(iRankArda` = 0；灰议 `-3` = 42 处、自身 `+10` = 2 处。
- **生效**：Python 实时读取，**旧档即时生效**，无需新开局。
- **回滚**：覆盖 `.bak-mod-20260808-180325` 可退回改造 22 状态；仓库侧 `git checkout` 该文件。
- **未做**：截图中 `-940-0%` 那一行的畸形显示未追查（疑为另一处 `%d` 槽位问题，但未定位、未验证，不作结论）。

## 改造 24：阿尔达「阶+经验」加成改为纯抗性（封顶 41）

- **日期**：2026-08-08 18:52（Asia/Shanghai）
- **动机**：改造 21–23 的等级/阶级加成是**无条件增强**——主教在毫无减益的环境里也白拿一两个档位，用户实测认为"太变态"。裁定改为**只用来对抗减益，不用来增强**。

### 档位映射先厘清（此前记录有误，此处更正）

`listArdas` 里 **ARDA10 是注释掉的**，实际长度 **10**（ARDA0–ARDA9），索引即 `iArda // 10`：

| iArda | 30–39 | **40–49** | 50–59 | 90–100 |
|---|---|---|---|---|
| 档位 | ARDA3 | **ARDA4（基数所在档）** | ARDA5（中性） | ARDA9（战力 +100%） |

注意基数 40 落在 **ARDA4**，本身就低于中性档 ARDA5 一级——MM 的原始设计里，祭司在完全中立环境下略微不利，要靠国教占比、友好领土、圣城邻近等正修正才能爬到中性以上。

### 改法：从「开头累加」改为「收尾按缺口封顶补」

```python
# 开头：只算，不加
iLevelArda = pCaster.getLevel() / 2
# （原有的 iArda += iRankArda + iLevelArda 已删除）

# 收尾（所有修正累加完、listArdas 定义之前）：
iArdaResist = min(iRankArda + iLevelArda, max(0, 41 - iArda))
iArda += iArdaResist
```

- **封顶 41**（用户定，非 40）：`41 // 10 = 4`，与基数 40 同为 **ARDA4 档**，所以档位上零增益，只是留 1 点余量。
- 插入点在两个函数各自所有修正累加完之后、`listArdas` 定义之前——避开中途的脱冕/叛教/众母神转化等提前 return 分支。
- `helpEffectArda` 的提示行**从原位（封顶前）移到封顶后**，改为显示 `iArdaResist` 即真实生效值；否则会报出未封顶的完整加成，与实际不符。

### 行为验证（桩测试）

| 场景 | 最终 iArda | 实际加成 | 档位 |
|---|---|---|---|
| 信徒 1 级、无减益 | 40 | +0 | ARDA4 |
| 主教 20 级、无减益 | 41 | +1 | **ARDA4（与信徒同档）** |
| 主教 20 级、−10 减益 | 41 | +11 | ARDA4（抗住了） |
| 信徒 1 级、−10 减益 | 30 | +0 | ARDA3（抗不住） |
| 主教 20 级、−30 减益 | 26 | +16（用尽） | ARDA2（超出抗性上限） |
| 主教 20 级、**+20 增益** | 60 | **+0** | ARDA6（加成完全不发放） |

最后一行是本次改造的核心：已有净增益时加成一分不给，彻底杜绝"增强"。

- **文件**：游戏 `<MM>\Assets\python\entrypoints\CvSpellInterface.py`（1,734,095 → 1,734,339 字节）；仓库 `MM源码` 同步（1,732,857 → 1,733,101）。
- **备份**：`.bak-mod-20260808-185229`（= 改造 23 状态，1,734,095 字节）。
- **校验**：两份均通过 `lib2to3` 的 Python 2 语法解析；CRLF 39,627 行、裸 LF **0**；`iArda += iRankArda + iLevelArda` 残留 0 处、`iArdaResist` 封顶式各 2 处、提示行 1 处。
- **生效**：Python 实时读取，**旧档即时生效**。
- **回滚**：覆盖 `.bak-mod-20260808-185229` 退回改造 23（无条件加成）。
- **未动**：改造 23 的灰色议会 −3（42 处）保持生效；等级仍为 `getLevel() / 2` 整数除法向下取整。

## 改造 25：阿尔达加成改为按基础值分段衰减（取代改造 24 的硬封顶）

- **日期**：2026-08-08 19:40（Asia/Shanghai）
- **动机**：改造 24 的硬封顶 41 把加成压得太死——处境好的祭司一点拿不到，成长感全没了。用户要求改为**平滑衰减**：被压制时全额给，基础值越高给得越少。真实目的是**让敌对教派的祭司也能为我所用**（俘获/策反后在我方地盘会吃满减益，正落在全额区间）。

### 分段表

| 不含加成的 iArda | 系数 |
|---|---|
| < 40 | **×1.0 全额** |
| 40–49 | ×0.8 |
| 50–59 | ×0.6 |
| 60–69 | ×0.4 |
| 70–79 | ×0.2 |
| ≥ 80 | ×0 |

```python
iArdaResist = iRankArda + iLevelArda
if iArda >= 80:
    iArdaResist = 0
elif iArda >= 70:
    iArdaResist = iArdaResist * 2 / 10
elif iArda >= 60:
    iArdaResist = iArdaResist * 4 / 10
elif iArda >= 50:
    iArdaResist = iArdaResist * 6 / 10
elif iArda >= 40:
    iArdaResist = iArdaResist * 8 / 10
iArda += iArdaResist
```

- 用**整数乘除**（先乘后整除 `*8/10`）而非 `*0.8`，避免重蹈改造 22 的浮点进 `%d` 槽位问题（见改造 23）。
- 位置与改造 24 相同：两个函数各自所有修正累加完之后、`listArdas` 定义之前。提示行仍显示 `iArdaResist` 即真实生效值。

### 行为验证（桩测试）

| 场景 | 基础值 | 满额 | 实际给 | 最终 | 档位 |
|---|---|---|---|---|---|
| 信徒 1 级、无减益 | 40 | 0 | 0 | 40 | ARDA4 |
| 主教 20 级、−30 减益 | 10 | 16 | **16 全额** | 26 | ARDA2 |
| 主教 20 级、−10 减益 | 30 | 16 | **16 全额** | 46 | ARDA4 |
| 主教 20 级、无减益 | 40 | 16 | 12 | 52 | ARDA5 |
| 主教 20 级、+20 增益 | 60 | 16 | 6 | 66 | ARDA6 |
| 主教 20 级、+40 增益 | 80 | 16 | **0** | 80 | ARDA8 |
| 祭司 10 级、−10 减益 | 30 | 8 | 8 全额 | 38 | ARDA3 |

- **已知局限（需注意）**：加成上限 = 阶 6 + 等级/2，20 级主教也只有 **+16 = 1.6 个档位**。而敌对教派祭司在我方领土常被压 30–50 点（国教不符 + 地块主人国教 + 邻近城市异教三重叠加），仍会停在 ARDA1–2 的重残区间（ARDA0 战力 −100%/失误 +200%）。**若目标是让敌对教派真正可用，本项不足够**，需另行削弱那几项惩罚或加归顺豁免——尚未实施。
- **文件**：游戏（1,734,339 → 1,734,959 字节）；仓库 `MM源码` 同步（1,733,101 → 1,733,721）。
- **备份**：`.bak-mod-20260808-194006`（= 改造 24 状态）。
- **校验**：两份均通过 `lib2to3` Python 2 语法解析；CRLF 39,649 行、裸 LF 0；`41 - iArda` 残留 0 处，衰减式各 2 处。
- **生效**：旧档即时生效。**回滚**：覆盖 `.bak-mod-20260808-194006` 退回改造 24 的硬封顶。

## 历史参考（2019 年 FFH 时代的改造，见 `C:\wm4.back\安装顺序.txt`）

- 地图尺寸：`CIV4WorldInfo.xml` + 地图脚本 `getGridSize`（Terra 大网格 / Pangaea 小一档）
- 自动存档：ini `MaxAutoSaves=5`、`AutoSaveInterval=4`
- 血肉傀儡削弱（用户 2026-07-23 口述确认）：原版 FFH 0.41 吞噬逻辑是"牺牲者更强则属性**直接看齐牺牲者**"；用户改为"**每次只 +1**"（线性成长，反超模）。该削弱版存在于仓库 FFH2 谱系与 `C:\Civilization4` 现装 FFH 的 `spellAddToFleshGolem`（两处一致，均为用户版而非原版）。另在 Streak 谱系把其击杀经验 8/4→4/2。**MM 用的仍是原版式"看齐"逻辑**（还叠加了回血 20 与晋升继承），如需在 MM 复刻削弱，改 MM 的 `spellAddToFleshGolem` 中两处 `setBaseCombatStr(max(...))` 为 `+1` 即可。成品备份 `C:\wm4.back\CIV4UnitInfos.rar` 未拆验

