# Rampage 测试计划

## 定位

本计划定义 Rampage 覆盖包的验证层次、风险优先级、准入/退出条件和证据要求。它不记录某次执行结果，也不替代 [PRD](../product/PRD.md) 或 Scrum Master 编写的 Sprint 验收标准。

执行入口：

- macOS 或任意可读工作区的检查见[静态验证](./static-validation.md)。
- Windows 基线、构建和游戏内场景见[运行验收指南](./runtime-acceptance.md)。
- XML、C++、Python、事件和 UI 的固定接口名见[跨层接口契约](../api/README.md)。
- 环境能力与某次检查结果分别以[环境配置](../ops/environments.md)和[环境状态](../ops/status.md)为准。

## 一页策略

本文所称移动半径统一指 `CvUnit::canMoveInto` 针对回合起点使用的 `plotDistance` 边界：`plotDistance = max(dx,dy)+floor(min(dx,dy)/2)`，其中 `dx`、`dy` 是地图横纵方向距离。该等距边界在离散网格上呈近似八边形，不是欧氏距离意义上的圆。

验证必须自底向上推进，前一层通过不能替代后一层：

| 层 | 目标 | 主要证据 | 可判定什么 | 不可替代什么 |
|---|---|---|---|---|
| L0 仓库身份 | 锁定代码线、提交和文件清单 | Git 提交、绝对路径、清单 | 检查的是哪份内容 | 用户机器实际加载目标 |
| L1 文件与语法 | 文件可读、XML well-formed、遗留 Python 特征可识别 | 命令输出、退出码 | 单文件基本完整性 | XML 引用闭包、Python 2.4 宿主可用性 |
| L2 静态跨层契约 | 追踪 XML、C++、Cy*、Python、文本和资源之间的名称契约 | 引用清单、差异清单、人工复核记录 | 合同面是否存在明显漂移 | C++ 能构建、游戏行为正确 |
| L3 Windows 构建 | 用声明的遗留工具链生成 Win32 DLL | 工具版本、完整日志、退出码、DLL/PDB/哈希 | 源码可编译链接、产物可追溯 | DLL 可被 BtS 装载 |
| L4 基线与加载 | 验证 Civ4、BtS、FFH2 Patch o、Rampage 合并目录与实际 DLL | 路径、哈希、启动日志、最小存档 | 宿主和覆盖包能共同加载 | 五项机制的规则正确性 |
| L5 玩法与界面 | 验证 F002–F006，并对账 F007 的原生反馈 | 存档、逐回合观测、日志、截图或录像 | 玩家可观察行为符合产品契约 | 未覆盖组合与长期兼容性 |
| L6 回归与兼容 | 验证干净部署、存取档和受影响邻接机制 | 重放记录、前后哈希、回归结果 | 变更没有破坏规定范围 | 所有外部模组/场景组合 |

分层诊断以最先出现不一致的层为故障归属候选。不得因“主菜单能打开”跳过 XML/DLL 身份核对，也不得因 XML 可解析就声明规则或 UI 正确。

## 范围

### 纳入

- `Rampage` 重点代码线及其与完整 FFH2 Patch o 基线的合并结果。
- XML Schema、XML 数据、C++ 源码与 DLL、Cy* 绑定、Python 入口/UI、文本和资源的跨层契约。
- F001 的外部依赖、Rampage 加载和氏族入口。
- F002 多属性多掷骰近战、F003 远程打击、F004 移动与地块容量、F005 工人占格生产、F006 玩家级食物经济。
- F007 要求的单位信息、战斗结果和食物账目对账。
- Windows x86 遗留构建链、干净 staging 部署、存档/重载与受影响范围回归。

### 不纳入

- Web 浏览器、API、数据库、服务端端口或测试用户；本项目不存在这些运行面。
- 在 macOS 上构建或启动 Civ4/BtS。
- 未经独立需求确认的编译器升级、Python 升级、发行重打包或玩法再设计。
- 把 `Fall from Heaven 2`、`Streak`、`Streak 3` 直接当作 Rampage 的运行目标；它们只用于基线或谱系比较。
- 本计划不创建 Sprint 验收标准、不派生正式验收 TC，也不产出执行报告。

## 风险优先级

| 级别 | 风险 | 失效方式 | 主要控制层 |
|---|---|---|---|
| Critical | 实际加载了错误模组、错误 DLL 或混合基线 | 所有结果针对错误对象，结论无效 | L0、L4 |
| Critical | DLL ABI、源码、Boost.Python、Python 2.4 不匹配 | 启动崩溃、入口缺失或静默错误 | L2–L4 |
| Critical | XML 字段/枚举顺序与 C++ 读取漂移 | 规则值错位或加载失败 | L1–L5 |
| High | C++ 规则、Cy* 暴露、Python/UI 不一致 | 计算正确但显示或操作错误，或反之 | L2、L5 |
| High | XML Type、文本键和资源路径在合并目录不闭合 | 特定单位、动作、文本或资源到达时失败 | L2、L4、L5 |
| High | F002–F006 的边界、行动成本或跨回合状态错误 | 核心玩法或经济结算错误 | L5、L6 |
| Medium | 覆盖复制留下陈旧文件 | 干净环境与升级环境行为不同 | L4、L6 |
| Medium | 存档、缓存或历史场景路由改变结果 | 重载后漂移，或绕过 Rampage | L4、L6 |
| Low | 非关键布局、本地化或资源回退问题 | 信息可读性下降但规则仍可运行 | L2、L5 |

优先级按阻断加载、静默破坏核心规则、影响范围和暴露时机确定。任何涉及金额、权限的通用风险规则不适用于本地单机模组；核心写入状态仍按 High 处理。

### 定向静态候选风险

下表只记录当前源码结构与产品契约之间需要上层验证的候选风险，不表示当前加载 DLL 已复现故障，也不构成 Scrum Master 验收标准或正式 TC。Windows 场景入口见[运行验收指南](./runtime-acceptance.md)。

| 候选风险 | 静态证据 | 现有需求映射 | 必须由 Windows 运行确认 |
|---|---|---|---|
| 玩家食物状态的存档持久化与每回合修正来源 | `m_iFood`、`m_iFoodPerTurn` 在 `CvPlayer::reset` 归零，但 `CvPlayer::read/write` 未见二者；`m_iFoodPerTurn` 仅见初始化、净食物读取、getter 与 Cy 只读暴露，未见非零写入入口（`CvPlayer.h:1184-1185`；`CvPlayer.cpp:416-417,7185,8711-8739,16813-17800`；`CyPlayer.cpp:805-807`；`CyPlayerInterface1.cpp:189`） | AC-F006-03 至 AC-F006-05、AC-F007-03 | 非零 Food Stores/Income/Cost 在保存、完全退出进程、重载后的保留与下一回合结算 |
| 禁用研究状态与 Food Income/净食物的静态耦合 | `CvPlayer::getCommerceRate` 在 `getDisableResearch() > 0` 时不区分 `CommerceTypes` 而直接返回 `0`；`calculateBaseNetFood` 使用 `getCommerceRate(COMMERCE_FOOD)` 计算净食物（`CvPlayer.cpp:7181-7189,11577-11603`） | AC-F006-03 至 AC-F006-05、AC-F007-03 | 在非零 `COMMERCE_FOOD` 下成对切换禁用研究状态，对账财务顾问 Food Income、HUD 净食物、回合结算后的 Food Stores/金币；产品意图由产品侧确认 |
| Work Tile worked 标记与账本/单位位置的存档一致性 | `m_bIsWorked` 只见初始化、setter/getter，未见进入 `CvPlot::read/write` 或被其他规则消费；Work Tile 另行更新玩家金币/食物 commerce（`CvPlot.h:512-513,659`；`CvPlot.cpp:74,4880-4888,9181-9667`；`CvUnit.cpp:1477-1566`） | AC-F005-01、AC-F005-03、AC-F007-03 | 在一个工人工作状态下保存、完全退出进程并重载；移动或推进回合前同时对账地块 `isWorked()`、玩家 `COMMERCE_GOLD`/`COMMERCE_FOOD`、Food Stores 与工人坐标，再令最后工人离开确认贡献只撤销一次 |
| 运输货物容量成本的消费 | `CvUnit::hasMaxUnitPerTile` 把运输者及可防守货物成本累加到 `iActualUnitWithCargo`，后续容量返回判断未再读取该变量（`CvUnit.cpp:3466-3499,3523-3572`） | AC-F004-03 | 同一运输者空载与装载正成本货物进入临界容量地块时的允许/拒绝结果 |
| 城市训练的候选单位成本 | `CvCity::canTrain` 只用候选成本判断是否为零，容量比较使用现有陆地/飞行占用，未把候选成本加入比较（`CvCity.cpp:1852-1867`） | AC-F004-03 | 现有占用加候选成本低于、等于和高于城市容量时的训练资格与完成后占用 |
| 近战同轮致死后的停止顺序 | `CvUnit::resolveCombat` 先执行防守方掷骰分支，再执行攻击方掷骰分支，双方死亡检查位于两段之后（`CvUnit.cpp:1796-1996`） | AC-F002-02、AC-F007-02 | 防守方先造成致死伤害后，攻击方同一轮是否仍产生掷骰、日志或伤害 |

## 需求覆盖地图

此表只定义验证切面，不复述或改写产品验收标准。预期行为以 PRD 中对应 AC 为准。

| 需求 | 静态/构建切面 | Windows 运行切面 |
|---|---|---|
| F001 | 覆盖清单、DLL 格式、入口 XML/Python、外部依赖清单 | AC-F001-01、AC-F001-02、AC-F001-03、AC-F001-04；基线、模组身份和氏族入口 |
| F002 | Unit Schema/Infos、CvInfos、CvUnit、事件与日志文本 | AC-F002-01 至 AC-F002-05；属性、多掷骰、护甲、伤势、行动/日志 |
| F003 | 射程/次数 XML、合法性和结算、任务入口、动画/日志 | AC-F003-01 至 AC-F003-04；距离、视线、多次射击、行动成本 |
| F004 | Unit/Terrain/Feature/Improvement/Defines、CvUnit/CvPlot/CvCity | AC-F004-01 至 AC-F004-05；`plotDistance` 半径边界、回合起点重置、容量、例外、来源 |
| F005 | Build/Unit/Improvement/Commerce/Text、CvUnit/CvPlot/CvPlayer | AC-F005-01 至 AC-F005-04；0/1/多工人、离开、产出变化 |
| F006 | Commerce/Text、CvPlayer、CyPlayer、HUD/财务顾问 | AC-F006-01 至 AC-F006-05；成本、豁免、正净值、缺口与金币 |
| F007 | GameTextMgr、Python screens、事件负载、字体与文本键 | AC-F007-01 至 AC-F007-03；单位、战斗、食物三组对账 |

## 准入与退出条件

### 静态验证

准入：仓库路径、目标代码线和提交可记录；所需检查命令可用。退出：L1 命令无未解释错误；L2 的引用差异均被分类为“覆盖包内满足”“由合并基线提供”或“需上层验证”。未分类差异阻止进入构建/运行结论，但不自动等同运行失败。

### Windows 构建

准入：工具链版本、include/lib 路径、源码提交、构建配置和一次性 staging 目标已锁定；不得把正式目标作为 Makefile 自动复制目录。退出：clean Debug/Release 命令退出码成功，日志无未解释错误，产物为 Win32/x86，DLL/PDB/哈希和依赖版本可追溯。

### Windows 运行

准入：Civ4、BtS、完整 FFH2 Patch o 分别完成基线冒烟；Rampage 从完整基线建立；实际目录、DLL 哈希、覆盖清单和缓存策略已记录。退出：F001–F007 所引用的权威验收标准均有对应执行证据；受影响规则完成存档/重载和干净部署回归；所有异常能定位到明确层或被标为阻塞。

正式 Sprint 放行仍由 Scrum Master 的验收标准、批次和验收报告决定，本计划本身不授予 PASS。

## 证据要求

每次执行至少记录：

- 源提交、仓库绝对路径、代码线、执行时间和操作者。
- Windows 版本、Civ4/BtS/FFH2 版本来源、目标模组绝对路径。
- DLL SHA-256、构建配置、工具链版本；使用预编译 DLL 时明确标注来源未知项。
- 合并部署清单、关键 XML/Python/资源哈希以及是否为干净 staging。
- 命令原文、退出码和未删节错误上下文；游戏内则保存日志、测试存档和逐回合观察。
- 每条结论对应的 PRD/SM 验收标准 ID，及其证据文件位置。

截图或录像能证明可见结果，但不能单独证明内部计算、实际 DLL 身份或跨回合状态；必须与日志、数值对账和环境清单组合使用。执行事实写入状态文档或报告，不回写本无状态计划。

## 变更影响与回归选择

| 变更面 | 最小回归范围 |
|---|---|
| XML 字段、Type 或枚举 | XML well-formed、Schema/C++ 读取、Type 引用、DLL/Python enum、受影响玩法 |
| C++ 规则或 Cy* 接口 | clean 构建、DLL 身份、Python 调用方、受影响玩法与存取档 |
| Python 入口/UI | Python 2.4 语法/导入、宿主入口、界面对账、相关玩法 |
| 文本键或资源 | 所有生产方引用、合并目录存在性、触发该路径的游戏内显示 |
| 安装/构建脚本 | 干净 staging、升级 staging、目标绝对路径、哈希、回退演练 |
| 食物、工人、移动等持久状态 | 回合边界、保存、重载、单位进入/离开和极端值 |

## 固有未知与升级条件

- 外部 Civ4/BtS、FFH2 Patch o 基线、嵌入式 Python 模块及字体/模型资源不在仓库中；只能在合并后的 Windows 目标确认。
- 预编译 DLL 与全部当前源码是否精确同源，不能仅凭共同提交证明。
- XML 缓存、存档兼容、场景 `ModPath` 和 DLL 导出兼容仍需宿主证据。
- 遇到异常时按 L0→L6 收集证据；第一处不一致交给对应开发/DevOps 角色，不用更高层现象猜测根因。
