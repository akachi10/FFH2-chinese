# 项目 CLAUDE.md（FFH2-chinese）

## 改动纪律（强制）

1. **首次改某个游戏文件，先备份原版**：改动前若该文件没有任何备份，先做 `<文件名>.bak-orig`（原版存证，永不覆盖、永不删除）。历史上已用最早的 `.bak-mod`（如 PublicMaps 下 2007-09 年的）充当原版存证的，视同 `.bak-orig`，同样不许覆盖。
2. **每次更改都做备份**：在已有备份的文件上再次改动，改前复制 `<文件名>.bak-mod-<yyyyMMdd-HHmmss>`（时间戳=实际执行时刻），使每个版本可独立还原。
3. **改动必须登记**：每次改动完成后，在本文件下方「改动版本列表」加一行（或更新对应行），版本号与 `MM玩法改造/README.md` 的"改造 N"编号对应；详细动机、字段、DLL 依据写在台账（README），本表只做索引。
4. 仓库内文件（git 管理）不做 `.bak` 备份，靠 git；游戏目录（`C:\Civilization4\...`）必须做文件备份。
   **两个仓库均由 session 管理提交**（用户 2026-08-08 授权）：游戏目录仓库与本台账仓库（`FFH2-chinese`），改动落盘并登记后由 session 直接 commit，无需询问。仅推送远端（push / 建远程仓库）仍需用户确认。
5. **实现形态偏离预期时先沟通，符合预期则直接做**：若改动只能以与用户要求不同的形态落地（妥协实现、体验差异、副作用、局限），必须先说明实际效果与局限，经用户确认有价值后再写入文件；能完全按预期实现的改动无需额外确认，按上述流程直接执行。（源自改造 16 的教训："事后自动解除"≠用户要的"请求时条件"，此类偏差应在动手前摆明。）

## 改动版本列表

| 版本 | 日期 | 内容 | 主要文件（游戏目录） | 备份标识 |
|------|------|------|---------------------|----------|
| 改造 1 | 2026-07-23 | 王宫防御 +300%（MM，已被改造 7 口径部分取代） | MM `CIV4BuildingInfos.xml` | `.bak-mod`（07-23） |
| 改造 2 | 2026-07-23 | 王宫城市每回合自动生成守军（MM） | MM python/Config | 见台账 |
| 改造 3″ | 2026-07-23 | MM 地图尺寸改档（现役，取代 3/3′） | MM `CIV4WorldInfo.xml` | 见台账 |
| 改造 4 | 2026-07-23 | 血肉傀儡"血肉腐败"技能（MM） | MM python + `init.xml` | 见台账 |
| 配置 | 2026-07-25 | 自动存档每回合一存、保留 100 | `CivilizationIV.ini` | `.bak-*` 系列 |
| 地图×1.5 | 2026-07-26 | 全部地图等比 ×1.5（Erebus 6 档 + PublicMaps 9 脚本 + FFH2 WorldInfo 兜底；基线=香草原值） | FFH2 `PrivateMaps\Erebus.py`；BtS `PublicMaps\*.py`；FFH2 `CIV4WorldInfo.xml` | `Erebus.py.bak-mod-20260726-171435`；其余 `.bak-mod-20260726-181346` |
| 改造 5 | 2026-07-26 | FFH2 侧 21 座王宫强化：城防 +200（Infernal 225）/ 城内单位每回合祝福 / +1 免费专家；3 格范围项已取消 | FFH2 `CIV4BuildingInfos.xml` | `.bak-mod-20260726-213311` |
| 改造 6 | 2026-07-26 | 金龙族仅极大地图城市上限翻倍（5→10，其余尺寸不变；FFH2 侧） | FFH2 `CIV4TraitInfos.xml`、`CIV4WorldInfo.xml` | `.bak-mod-20260726-213420`、`.bak-mod-20260726-214052` |
| 改造 7 | 2026-07-26 | MM 侧王宫强化迁移（22 座；Elohim/Grigori 保留原生晋升不发祝福） | MM `CIV4BuildingInfos.xml` | `.bak-mod-20260726-220627` |
| 改造 8 | 2026-07-26 | 史诗探索按地点冷却（地块 scriptData `ELCD:` 段重实现；旧的 `setTempImprovementType` 方案因 DLL 同值守卫无效，已废弃） | MM `python\entrypoints\CvSpellInterface.py`（+ 仓库 `MM源码` 同步） | `.bak-mod-20260726-225600` |
| ~~改造 9~~ | 2026-07-27 | ~~MM 极大地图 39×25→50×35~~ **已撤销**（用户评估 28000 格内存风险后决定回退，现值恢复 39×25） | MM `CIV4WorldInfo.xml` | `.bak-mod-20260727-020751`（39×25）/ `.bak-mod-20260727-revert9-*`（50×35 存证） |
| 改造 10 | 2026-07-27 | XML 兜底极大档 X+3/Y+2：MM 39×25→42×27（168×108），FFH2 48×30→51×32（204×128）；影响 Big_and_Small 等无自带尺寸表的地图，旧档不受影响 | MM + FFH2 `CIV4WorldInfo.xml`（FFH2 仓库副本同步） | 各自 `.bak-mod-20260727-*`（改前值） |
| 改造 11 | 2026-07-27 | 伯兰娜（LEADER_VOLANNA，暗精灵）加 理财（FINANCIAL）+ 僭夺（TOLERANT）两特性，原有好战/拾荒保留，共 4 特性 | MM `CIV4LeaderHeadInfos.xml` | `.bak-mod-20260727-*`（改前值） |
| 修复 1 | 2026-08-04 | CvEventManager 53 处 `str(x.getName())` 中文名 UnicodeEncodeError 崩溃修复（YK-L10N 同款 `encode('latin_1','replace')`，旧档即时生效） | MM `python\CvEventManager.py`（+ 仓库同步） | `.bak-mod-20260804-115328` |
| 改造 12 | 2026-08-04 | 精灵强制宣战（warScript，AC>20）加「不悦或以下」态度门槛，谨慎及以上不再强制开战 | MM `python\CustomFunctions.py`（+ 仓库同步） | `.bak-mod-20260804-115328` |
| 改造 13 | 2026-08-04 | 植树可在己方城市格施放——仅限原本可在设施上植树的文明（光明/暗精灵+库里奥塔特）；其他文明规则不变（canHaveFeature 对城市恒否，手动校验旁路；首版误扩「任何文明己方设施放行」已于当日修订撤回） | MM `python\entrypoints\CvSpellInterface.py`（+ 仓库同步） | `.bak-mod-20260804-132746`（原版）/ `.bak-mod-20260804-133137`（v1 存证） |
| 改造 14 | 2026-08-04 | 金龙族极大地图正城上限 5→7（MM 侧 `iMaxCitiesMod` 2→4，仅金龙受影响——全 XML 唯一非 -1 的 `iMaxCities` 是 TRAIT_SPRAWLING）；**旧档不生效，需新开局**。定居点增强/AI 转正方案经讨论放弃（成长为 DLL 硬锁、人口无收益） | MM `CIV4WorldInfo.xml`（仓库 MM源码 按只读基准不动，沿改造 10 口径） | `.bak-mod-20260804-185121` |
| ~~改造 15~~ | 2026-08-09 | ~~降低通胀（HandicapInfo / GameSpeedInfo）~~ **未实施**——仅停留在调研阶段，用户 2026-08-09 裁定不做，编号作废留空。游戏文件从未改动 | 无 | 无 |
| ~~改造 16~~ | 2026-08-05 | ~~附庸新规（和平附庸需互不侵犯 40 回合+一人一附庸，事后解除式实现）~~ **已撤销**（DLL 无源码只能做成立后自动解除，无法做成请求时条件，用户评估无价值；游戏文件已还原） | MM `python\CvEventManager.py`（已还原） | `.bak-mod-20260805-134545`（还原来源）/ `.bak-mod-20260805-135045`、`.bak-mod-20260805-140014-revert16`（改造版存证） |
| 改造 17 | 2026-08-05 | 史诗探索冷却常量化（rev2 按速度分档）：`EPIC_LAIR_COOLDOWN_BY_SPEED` 表（马拉松/史诗/普通/快速各一值，现全为 1）+ `EPIC_LAIR_COOLDOWN_DEFAULT` 兜底；原版等效值 20/10/7/4 已注释存档。实时生效；已在冷却中的点走完原剩余冷却 | MM `python\entrypoints\CvSpellInterface.py`（+ 仓库同步） | `.bak-mod-20260805-170829`、`.bak-mod-20260805-171043` |
| 改造 18 | 2026-08-06 | 世界编辑器可增删「隐藏建筑」（bGraphicalOnly，含 16 座各教「敌对版」神殿）：解除 Platy WB 的"隐藏未启用"过滤对隐藏建筑的屏蔽，并让隐藏宗教建筑进入「宗教建筑」分类 | MM `python\Screens\PlatyBuilder\WBBuildingScreen.py`、`CvPlatyBuilderScreen.py`（+ 仓库同步） | 各自 `.bak-orig-20260806-172142` |
| 改造 19 | 2026-08-07 | 三桅战舰 / 主力舰恢复运兵：MM 把这两艘从「载 2 陆军」改成「只挂 1 只猎鹰」，现改为载量 3、无域/无特殊限制（陆军与猎鹰皆可）| MM `CIV4UnitInfos.xml`（+ 仓库同步） | `.bak-mod-20260807-064513` |

| 改造 20 | 2026-08-07 | 移除「附庸边境压制」：DLL 二进制补丁，`CvPlot::calculateCulturalOwner()` 不再把宗主城市放进候选名单，附庸地块不再被宗主吞并 | MM `Assets\CvGameCoreDLL.dll`（偏移 `0x207FFE`，6 字节） | `.bak-orig-20260807-153551` |

| 改造 21 | 2026-08-09 | 阿尔达两项调整：① 灰色议会对**其他**宗教的阿尔达惩罚 −7 → −1（42 处，其自身 +10 不动）；② 阿尔达基数加入施法者**等级 ×1** 与**单位阶级 `iTier` ×3** | MM `CvSpellInterface.py`（+ 仓库同步） | `.bak-mod-20260809-071146` |

| 改造 22 | 2026-08-09 | 修订改造 21 的第二项：「阶」改用**祭祀等级**（信徒 0 / 祭司 3 / 主教 6，按 `PROMOTION_DIVINE/DIVINE2` 判定，不再用 `iTier`）；经验改为**每等级 0.5** 且不预先取整（收尾索引改 `int(iArda)//10`）| MM `CvSpellInterface.py`（+ 仓库同步） | `.bak-mod-20260809-072541` |

| 改造 23 | 2026-08-08 | 阿尔达两项修订：① 灰色议会对其他宗教的惩罚 −1 → **−3**（42 处，改造 21 削过头的回调；其自身 +10 仍不动）；② **等级加成退回整数除法** `getLevel() / 2`（原 `/ 2.0`），`iArda` 恢复全程整数，连带拆除改造 22 为兜底浮点而加的 3 处 `int()` 补丁——修掉悬浮提示里 `1110048768`（= 浮点 42.5 的位模式）这类天书数字 | MM `CvSpellInterface.py`（+ 仓库同步） | `.bak-mod-20260808-180325`（改造22态）/ `.bak-mod-20260808-180535`（灰议−3 后） |

| 改造 24 | 2026-08-08 | 阿尔达「阶+经验」加成改为**纯抗性**：不再于开头直接累加，改为所有修正算完后按缺口封顶补 `min(阶+经验, max(0, 41 - iArda))`。无减益时封顶 41（与基数 40 同为 ARDA4 档，档位零增益）；仅当被压到 41 以下才补，最多补回 41。提示文本同步改为显示封顶后的真实生效值 | MM `CvSpellInterface.py`（+ 仓库同步） | `.bak-mod-20260808-185229` |

| 改造 25 | 2026-08-08 | 阿尔达「阶+经验」加成改为**按基础值分段衰减**（取代改造 24 的硬封顶 41）：不含加成的 iArda `<40` 全额、`40s ×0.8`、`50s ×0.6`、`60s ×0.4`、`70s ×0.2`、`≥80` 归零；整数乘除（`*8/10`）不引回浮点。意图是让被压制的祭司（尤其敌对教派）拿满加成，处境好的不再白拿 | MM `CvSpellInterface.py`（+ 仓库同步） | `.bak-mod-20260808-194006` |

| 改造 26 | 2026-08-08 | 敌对版神殿可造祭司：**12 个**（确有敌对版的教派）祭司的 `PrereqBuilding`（认具体 Type，写死友好版）改为 `PrereqBuildingClass`（认 BuildingClass，友好/敌对同类通吃）——与**信徒既有写法对齐**（信徒本就用 Class，故敌对神殿一直能出信徒）。**仅改确有 `_HOSTILE` 版的 12 个**；无敌对版的 5 个（丰饶/永恒结社/树叶/灰议/狐人，其 Class 下只有一个 Type、两种写法等价）与莱兰（信徒要图书馆、祭司要档案馆，本就是不同建筑的递进链）一律保持 `PrereqBuilding` 原样，不留无谓变更。主教不动，`StateReligion` 仍要求国教对口，敌对教派升不了主教 | MM `CIV4UnitInfos.xml`（+ 仓库同步） | `.bak-mod-20260808-202434` |

| 改造 27 | 2026-08-09 | 商船（`UNITCLASS_MERCHANTMAN`）改为国家单位，每方同时最多 **2** 艘（`iMaxPlayerInstances` −1 → 2）。动机：贸易任务收益在马拉松+跨海下可达 1.1 万金/次而买船仅 1800，「每回合买船跑贸易」成印钞机；限量而非砍收益，保留正常玩法手感 | MM `CIV4UnitClassInfos.xml`（+ 仓库同步） | `.bak-orig-20260809-232547`、`.bak-mod-20260809-232547` |

> 路径缩写：FFH2 = `C:\Civilization4\Beyond the Sword\Mods\Fall from Heaven 2\Assets\XML\...`；MM = `C:\Civilization4\Beyond the Sword\Mods\Magister Modmod for FfH2\Assets\XML\...`；BtS = `C:\Civilization4\Beyond the Sword\`。

## 游戏目录 git 仓库（改造版本管理）

**游戏目录本身是一个独立的 git 仓库**，专门管改造历史，与本仓库（`FFH2-chinese`）互不隶属。

- 仓库根：`C:\Civilization4\Beyond the Sword\Mods\Magister Modmod for FfH2\`
- 跟踪范围：**只跟踪 `*.xml` / `*.py` / `*.ini`**。规则写在该目录的 `.gitignore`（默认 `*` 全忽略 + `!*/` 允许递归 + 白名单放行），已用模拟目录树实测验证。
- 明确排除：所有 `*.bak-*` / `*.crashed-*` / `*.pyc`（含 `Text.bak-orig-*` 这类**备份目录**，必须写 `*.bak-*/` 且排在 `!*/` 之后，否则会被递归收进来）；`Art/`、`res/`、`sounds/`、`Resource/`、`Trophy/`；`*.dll` / `*.FPK` / `*.exe` / `*.xlsm` / `*.CivBeyondSwordWBSave`。
- `.gitattributes` 设 `* -text`：**关闭一切换行符自动转换**。Civ4 的 XML/Python 全是 CRLF，autocrlf 会让游戏解析异常，也会让 diff 整篇爆红。仓库本地也设了 `core.autocrlf false`。
- **提交由 session 负责**（用户 2026-08-08 授权）：每次改造落盘后，session 直接敲 `git add -A` → `git commit -m "改造 N：xxx"` 提交，不必询问、不必等用户动手。目录名含空格，路径要引号。
- **首次提交已完成**：2026-08-09，commit `e16de2b`「baseline: 改造 1-22 后的游戏目录配置」，541 个文件（xml 276 / py 259 / ini 2 / dll 1 / 其余为 git 配置与脚本），`.git` 约 9 MB。
- **git 身份**：本机原先没有配任何 `user.name` / `user.email`，`git commit` 会直接 fatal 退出。已在**该仓库本地**配 `zsts` / `akache.tao@gmail.com`（`--local`，不影响其它仓库）。换机器或重建仓库时需重配。
- **主 DLL 纳入跟踪**：`Assets\CvGameCoreDLL.dll`（改造 20 打过二进制补丁）用 `!/Assets/CvGameCoreDLL.dll` 单独放行；**不**跟踪 `CvGameCoreDLL_Assert.dll`（6.5MB 调试版，从未改动），`.bak-orig-*` / `.bak-mod-*` 备份也仍被排除。`.gitattributes` 加了 `*.dll binary`，避免 git 尝试 diff/合并。注意：6MB 二进制每提交一版就在仓库里留一份完整副本，改 DLL 要有节制；`MM玩法改造\tools\` 下的补丁脚本（带字节校验与 `--revert`）仍是首选的复现与回滚手段。

### 两个仓库的分工（用户 2026-08-08 定）

**工作目录（`FFH2-chinese`）与游戏目录是两件事**，不要混为一谈：

| 仓库 | 职责 | 提交口径 |
|---|---|---|
| 工作目录 `FFH2-chinese` | **工程管理**：台账、文档、汉化成品、工具脚本、`MM源码` 对照基准 | 按工作内容提交，信息写清改了什么 |
| 游戏目录 `Magister Modmod for FfH2` | **改造版本留痕**：实际生效的游戏文件 | **每次改造落盘后提一次，提交信息对应台账的「改造 N」编号** |

游戏目录的提交与台账编号一一对应，日后靠编号即可在两边互查（例：`03406db` ↔ 改造 23）。

### 台账仓库（`FFH2-chinese`）自身的 git

- 同样由 session 管理提交；本地身份已配 `zsts` / `akache.tao@gmail.com`（此前也是空的，会 fatal）。
- **`.gitattributes` 已补（2026-08-08，`* -text`）**：此前该仓库没有这个文件，Git for Windows 默认 `autocrlf=true` 把入库文件的 CRLF **剥成 LF**——1423 个已跟踪文件中 **1159 个** blob 与磁盘不一致（例：`MM源码` 的 `CvSpellInterface.py` 磁盘 1,732,857、blob 仅 1,693,234，差 39,623 = CRLF 行数）。这会让「仓库版 vs 游戏版」的字节比对失去意义。
- **已于 `6ce7647` 全库重新入库修正**：1801 个文件、480 万行增删（插入与删除行数完全相等，纯行尾变化零内容改动）。**现状：blob 与磁盘逐字节一致，不一致 0 个**（台账仓库 1415 / 游戏目录仓库 541，两边均已核验）。按用户裁定「旧的不管」，更早的历史提交未改写，仍是 LF，但那段历史不再作为基准使用。

### 与 `MM源码` 的分工

`<repo>\MM源码` 是**上游英文原版**的快照，不是游戏目录的镜像，**不需要再同步**。它的作用是当对照基准——例如靠「仓库版 vs 游戏版」的字节差判断某项改动是否真的落地。已知两边天然不同的地方：游戏侧的 `Text\*` 是汉化后的（`Magister_CIV4GameText_FFH2.xml` 1.31MB → 5.17MB），`Text\YKBase_*` 系列与 `Assets\Config\` 整批只存在于游戏侧。

### 改动纪律的调整

游戏目录进 git 之后，`.bak-mod-<时间戳>` 备份**仍然保留**——因为改动落盘与 `git commit` 之间有时间差，`.bak` 是那段窗口里唯一的退路。两者并存：`.bak` 管即时回滚，git 管长期历史与跨改造对比。

## 已知机制要点（改动前必读）

- 地图尺寸：脚本 `getGridSize()` 覆盖 XML；改尺寸先看目标地图有无自带尺寸表。详见记忆与 `docs/`。
- 城防（iDefense）/ 免费专家（iFreeSpecialist）走 `processBuilding` 增量缓存进存档——**旧档不生效，需开新档**；FreePromotion+onMove 每回合重算，旧档即时生效。
- `bApplyFreePromotionOnMove` 实义是"每回合结束授予城内单位"，非"踏入即得"（FFH2 DLL `CvCity.cpp:988-1003`；MM 为 MNAI-U，推定同构、待实测）。
- 同城两个 `iPlotRadius>0` 建筑会触发 DLL 回落缺陷（失去其一误砍到半径 2），勿给王宫类再挂半径。
- Civ4 XML 无继承：改"所有王宫"= 逐条目批量替换 + 计数校验（N 座 × M 字段）。
- 插入/移位 XML 元素会因 schema 顺序崩溃启动，只改已有元素的值；批量改动后必查 well-formed。
- `CvPlot::setTempImprovementType` 开头有 `if (getImprovementType() != eImprovement)` 守卫：**新旧改良相同时整个调用被静默跳过**，计时器不会被设置。因此它只能用于"临时换成别的改良"，**不能拿来给地块打原地冷却/标记**（改造 8 的根因）。地块级持久标记改用 `plot.getScriptData()/setScriptData()` + 带前缀键值段（如 `ELCD:<回合>;`），读写必须保留段外既有内容。
- 附庸边境压制（BtS 原版逻辑）：`CvPlot::calculateCulturalOwner()` 对非城市地块，会把「文化最高玩家所臣服的宗主」的城市也当作候选，且给自家城市 +5 优先级惩罚（越小越优先），导致附庸紧邻宗主城市的地块被宗主收走；`CvTeam::setVassal()` 在签约/解约当场对双方全部地块重算一次。已由改造 20 的 DLL 补丁移除。
- 阿尔达（Arda）判定：`CvSpellInterface.effectArda()` 基数 40，累加宗教占比/阵营/领袖态度/地形/邻近城市宗教等修正，最后 `iArda//10` 夹到 0–9 映射 `PROMOTION_ARDA0..9`（>100 → ARDA10，<0 → ARDA0 并可能触发脱冕）。**`helpEffectArda()` 是同一套算法的第二份拷贝（同文件靠后）**，改算法必须两处同步，否则提示与实际不符。
