# Rampage 跨层接口契约

## 这里定义什么

Rampage 没有 Web 服务接口。本目录定义 Civilization IV 宿主、GameCore DLL、XML、Python 与原生 UI 之间依赖固定名称和参数形状的接口。它们共同属于[跨层一致性边界](../architecture/decisions/0002-cross-layer-consistency.md)；产品行为见 [PRD](../product/PRD.md)，交互职责见 [UE 规格](../product/UE-spec.md)。

最短阅读路径：

1. 修改 XML 字段、`Type` 或全局开关：读 [XML → C++](modules/xml-cpp-contract.md)。
2. 修改 `Cy*` 查询、枚举或 Python 模块名：读 [C++ → Python](modules/cpp-python-contract.md)。
3. 修改事件标签、回调或 XML Python 表达式：读 [事件与脚本](modules/events-and-scripting.md)。
4. 修改顾问、百科、HUD 或目标模式：读 [UI 入口](modules/ui-entrypoints.md)。

## 运行时方向

```text
XML Schema ──约束──> XML 数据 ──读取──> CvInfo / Global Defines
                                           │
                                           ├──消费──> C++ 规则与结算
                                           └──发布──> CvPythonExtensions / Cy*
                                                            │
宿主 / DLL ──固定模块名、函数名、事件标签──────────────────────┤
                                                            v
                                              Python 规则、事件与原生 UI
```

Python 也会写回 `CyPlayer` 等包装对象，因此桥接并非纯展示层。任何跨层变更都以目标模组目录中合并后的 DLL、XML、Python、文本和资源为验证对象，而不是只检查单个仓库文件。

## 公共契约索引

| ID | 固定契约 | 生产方 → 消费方 | 深入文档 |
|---|---|---|---|
| IC-01 | XML 文件路径、根路径与 Schema 内容模型 | XML / 装载器 → `CvInfo` | [XML → C++](modules/xml-cpp-contract.md) |
| IC-02 | `Type` 字符串与全局类型索引 | XML → C++ / Python / UI | [XML → C++](modules/xml-cpp-contract.md) |
| IC-03 | 单位战斗与射程字段 | Unit XML → `CvUnitInfo` / `CvUnit` | [XML → C++](modules/xml-cpp-contract.md) |
| IC-04 | 单位地块成本、地形支撑与容量 Defines | XML → `CvPlot` / `CvUnit` / `CvCity` | [XML → C++](modules/xml-cpp-contract.md) |
| IC-05 | `COMMERCE_FOOD` 枚举与信息顺序 | C++ enum / XML → C++ / Python | [XML → C++](modules/xml-cpp-contract.md) |
| IC-06 | Global Defines 名称和值类型 | Defines XML → C++ | [XML → C++](modules/xml-cpp-contract.md) |
| IC-07 | `USE_*_CALLBACK` 开关 | callback Defines → DLL 回调点 | [事件与脚本](modules/events-and-scripting.md) |
| IC-08 | `DLLPublishToPython` 发布的类与枚举 | DLL → `CvPythonExtensions` | [C++ → Python](modules/cpp-python-contract.md) |
| IC-09 | `CyPlayer` 食物查询与写入 | C++ → Python UI / 脚本 | [C++ → Python](modules/cpp-python-contract.md) |
| IC-10 | `CyUnit`、`CvUnitInfo` 战斗查询 | C++ → HUD / 百科 | [C++ → Python](modules/cpp-python-contract.md) |
| IC-11 | `CvDefines.h` 的 Python 模块名 | DLL / 宿主 → Python 文件 | [C++ → Python](modules/cpp-python-contract.md) |
| IC-12 | `CvGameInterface` 规则回调名称与返回值 | DLL → Python `GameUtils` | [事件与脚本](modules/events-and-scripting.md) |
| IC-13 | `CvScreensInterface` 屏幕函数 | 宿主 / DLL → Python 屏幕对象 | [UI 入口](modules/ui-entrypoints.md) |
| IC-14 | `CvSpellInterface` 表达式上下文 | XML / DLL → Python `eval` | [事件与脚本](modules/events-and-scripting.md) |
| IC-15 | `CvEventInterface.onEvent` 事件信封 | DLL → Python 事件适配器 | [事件与脚本](modules/events-and-scripting.md) |
| IC-16 | `CvEventManager.EventHandlerMap` 标签分派 | 事件适配器 → Python handler | [事件与脚本](modules/events-and-scripting.md) |
| IC-17 | generic event 的嵌套参数形状 | C++ 结算 → Python handler | [事件与脚本](modules/events-and-scripting.md) |
| IC-18 | 战斗日志 `CombatDetails` 负载 | `CvUnit` → `CvEventManager` | [事件与脚本](modules/events-and-scripting.md) |
| IC-19 | UI dirty bit 与读取刷新 | C++ 状态变化 → Python UI | [UI 入口](modules/ui-entrypoints.md) |
| IC-20 | 文本键、任务名、模式名与资源路径 | XML / C++ → UI / 宿主 | [UI 入口](modules/ui-entrypoints.md) |

## 五类定制机制的接口面

移动机制中的距离统一指基于回合起点的 `plotDistance` 移动半径：`plotDistance = max(dx, dy) + floor(min(dx, dy) / 2)`。其等距边界是离散网格上的近似八边形，不是欧氏距离意义上的圆。

| 机制 | XML / 枚举 | C++ | Python / UI |
|---|---|---|---|
| 多属性多掷骰近战 | `iMaxHitPoints`、`iArmour`、`iDexterity`、`iAttackCount` | `CvUnitInfo::read`、`CvUnit::resolveCombat` | `CyUnit` / `CvUnitInfo` 查询、`combatLog*` |
| 最小/最大距离远程打击 | `iAirRangeMin`、`iAirRange`、`iAirCombat`、`iAirCombatCount` | `CvUnit::canRangeStrikeAt`、`rangeStrike` | `INTERFACEMODE_RANGE_ATTACK`、战斗日志 |
| 基于回合起点的 `plotDistance` 移动半径与地块容量 | `iMoves`、`iUnitPlotCost`、`iUnitPlotSupport`、容量 Defines | `CvUnit::canMoveInto`、`CvPlot::getUnitPlotCapacity` | 拒绝表现由宿主移动界面呈现 |
| 工人占格生产 | `BUILD_WORK_TILE`、地块 Yield、`COMMERCE_FOOD` | `CvUnit::updateCommerce` | HUD / 财务 dirty bit 刷新 |
| 玩家级食物经济 | `COMMERCE_FOOD` | `CvPlayer` 食物储备、收入、成本与结算 | `CyPlayer`、HUD、`CvFinanceAdvisor` |

## 证据语言

- **事实**：文件中的固定名字、调用、读取、分派或数据结构。
- **推断**：由多层静态调用链得到、但没有 Windows 宿主观察支撑的结论。
- **未知**：覆盖包缺少外部基础文件、预编译 DLL 来源或宿主运行证据时无法确定的内容。

仓库静态证据不能证明用户机器加载了 Rampage，也不能证明预编译 DLL 与源码一致。`CvGameInterfaceFile.py` 与 `CvEventInterface.py` 不在覆盖包中；它们属于外部 FFH2 基线输入。`CvPythonExtensions` 则是 DLL 发布的嵌入式扩展模块，不应按普通 `.py` 文件查找。

## 统一变更规则

1. 保留固定名字时，逐层核对 Schema、XML 数据、C++ 读取/消费者、Boost.Python 发布、Python 调用、文本和资源。
2. 修改固定名字时，同一交付切面同步处理所有生产方和消费方；不能依赖静默回退。
3. 修改 enum 顺序时，核对 XML 信息顺序、C++ 数组大小、Python enum 和存档/缓存影响。
4. 修改事件参数时，核对 C++ 添加顺序、事件适配器、`handleEvent` 尾部六字段剥离和 handler 解包。
5. 验证分为静态契约、Windows 构建、完整游戏运行三层；前一层不能替代后一层。

## 已知未知

- 外部 FFH2 Patch o 提供的 `CvGameInterfaceFile.py`、`CvEventInterface.py`、基础 Defines、脚本与资源精确内容未知。
- `RANGED_ATTACKS_USE_MOVES` 的合并后取值未知。
- XML Schema 的宿主校验严格度、XML 缓存命中与缓存清理行为需要游戏环境确认。
- `CvUnit` 回合起点字段没有对应的流序列化证据；回合中途存读档后的 `plotDistance` 移动半径语义未知。
- `CvPlayer::read/write` 未见对 `m_iFood`、`m_iFoodPerTurn` 的流读写；接口绑定本身不能证明二者存在存档持久化契约。仓库内 `m_iFoodPerTurn` 只有初始化与读取暴露，未见变更入口，运行包是否存在外部来源未知。玩家食物储备与每回合修正的存读档保留行为存在高风险，需在 Windows 游戏环境执行 save/reload 验证，不能仅凭静态证据断言具体表现（`CvPlayer.h:1184-1185`；`CvPlayer.cpp:416-417,8711-8739,16813-17328,17334-17800`）。
- `CvPlayer::getCommerceRate` 在 `getDisableResearch() > 0` 时对任意 `CommerceTypes` 直接返回 `0`，所以 `COMMERCE_FOOD` 的商业收入也归零并进入 `calculateBaseNetFood`。禁用研究是否应同时禁用食物商业收入属于产品意图未知；需在 Windows 游戏环境对账 HUD、财务顾问与回合结算，静态证据不构成运行复现结论（`CvPlayer.cpp:7181-7189,11577-11603`）。
- 预编译 DLL 与仓库 C++ 源码的对应关系未知。
