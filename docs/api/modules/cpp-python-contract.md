# C++ → Python 接口契约

## 边界

GameCore DLL 通过两类接口进入 Python：`DLLPublishToPython()` 发布 `Cy*`、`Cv*Info` 和 enum；C++ `callFunction` 按固定模块名和函数名调用 Python。本文记录前者与模块身份；事件和规则回调见 [事件与脚本](events-and-scripting.md)，屏幕函数见 [UI 入口](ui-entrypoints.md)。

## IC-08：`CvPythonExtensions` 发布

`DLLPublishToPython()` 依次注册 enums、game、random、team、area、structs、map、map generator、selection group、art、text manager、info、hall of fame、game core utils、message control，并把较大的 `CyCity`、`CyPlayer`、`CyUnit`、`CyPlot`、`CyGlobalContext` 类分片注册到同一个 Python 类。

输入是 DLL 内 C++ 对象或 enum；输出是在嵌入式模块 `CvPythonExtensions` 中可导入的 Python 类型与方法。该模块由宿主/DLL 提供，不对应覆盖包中的 `.py` 文件。

方法公开契约以 Boost.Python `.def("名称", &符号, ...)` 为准。仅有 C++ getter、头文件注释或 `Cy*` 包装方法都不足以让 Python 调用。

事实证据：`CvDLLPython.cpp:1-84`；`CyEnumsInterface.cpp`；`CyInfoInterface1.cpp`；`CyPlayerInterface1.cpp`；`CyUnitInterface2.cpp`。

## 对象与生命周期

| 发布形状 | 约定 | 调用方责任 |
|---|---|---|
| 整数、布尔、字符串、enum | 按值返回 | 不保存为底层对象引用 |
| `manage_new_object` | Python 包装层接管新 `Cy*` wrapper | 不手工释放 C++ wrapper |
| `reference_existing_object` | 引用 DLL 管理对象 | 不跨越对象失效点长期持有 |
| 事件中的临时 `CyUnit` / `CombatDetails` | 只在同步回调内有效 | handler 不缓存对象供稍后使用 |

`CvDllPythonEvents::reportCombatResult` 在 `postEvent` 返回后删除两个临时 `CyUnit` wrapper；战斗日志把栈上的 `CombatDetails` 转成 Python 对象并同步分派。延迟保存这些对象会产生悬空引用风险。

事实证据：各 `Cy*Interface.cpp` 的 return policy；`CvDllPythonEvents.cpp:210-229`；`CvUnit.cpp:1750-1980,19470-19610`。

## IC-09：玩家食物接口

| Python 名 | C++ 目标 | 输入 | 输出 / 失败哨兵 | 消费方 |
|---|---|---|---|---|
| `CyPlayer.getFood()` | `CvPlayer::getFood` | 无 | 储备；空 wrapper 返回 `-1` | 财务顾问、脚本 |
| `setFood(i)` | `CvPlayer::setFood` | 新储备 | 无 | 脚本 |
| `changeFood(i)` | `CvPlayer::changeFood` | 差量 | 无 | 脚本 |
| `getFoodPerTurn()` | `CvPlayer::getFoodPerTurn` | 无 | `m_iFoodPerTurn`；空 wrapper `-1` | 未见仓库 Python 调用方 |
| `calculateFoodCosts()` | `CvPlayer::calculateFoodCosts` | 无 | 军事食物成本；空 wrapper `-1` | 财务顾问 |
| `calculateFoodRate()` | `CvPlayer::calculateFoodRate` | 无 | 净食物；空 wrapper `-1` | UI / 脚本 |
| `getCommerceRate(COMMERCE_FOOD)` | 玩家 commerce rate | enum | 食物商业收入；`getDisableResearch() > 0` 时返回 `0` | 财务顾问、食物结算 |

这些值属于玩家级食物，不是 `CyCity.getFood()` 的城市粮仓。UI 必须用对象类型和标签区分两者。

`m_iFood` 在 `reset` 中归零，并由 getter、setter 与结算代码使用。相比之下，仓库内 `m_iFoodPerTurn` 只见初始化为 `0`、C++ getter 和 Cy 读取暴露，未见 setter、change 方法或其他写入点；不能把它描述为当前可观察的非零输入，运行包是否存在仓库外来源仍未知。

`CyPlayer` 对食物储备的可读写绑定和对每回合修正的只读绑定，本身不能证明 `m_iFood` 与 `m_iFoodPerTurn` 存在存档持久化契约。`CvPlayer::read` 与 `CvPlayer::write` 中未见针对二者的流读写。运行时存档/读档能否保留玩家食物储备，以及外部来源若能改变每回合修正时能否保留该值，属于高风险未知，必须在 Windows 游戏环境执行 save/reload 验证；静态证据不足以断言具体丢失表现。

**静态耦合**：`CvPlayer::getCommerceRate` 在 `getDisableResearch() > 0` 时不区分 `CommerceTypes`，直接返回 `0`；因此 `getCommerceRate(COMMERCE_FOOD)` 的食物商业收入也变为 `0`。`calculateBaseNetFood` 使用该返回值加上 `getFoodPerTurn()`，再扣除 `calculateFoodCosts()`，所以该分支会进入玩家净食物计算。

**产品意图未知**：静态接口不能说明“禁用研究”是否应同时禁用食物商业收入，也不能据此把耦合定义为产品规则。

**Windows 运行验证**：需要在 `COMMERCE_FOOD` 非零时切换 `getDisableResearch()` 条件，对账财务顾问、HUD 与回合食物结算；仓库静态证据不构成运行复现结论。

事实证据：`CyPlayerInterface1.cpp:123-130,178-191`；`CyPlayer.cpp:519-531,788-807`；`CvPlayer.cpp:7139-7189,8711-8759,11577-11603`；`CvFinanceAdvisor.py:95-122`。持久化静态证据：`CvPlayer.h:1184-1185`；`CvPlayer.cpp:416-417,8711-8739,16813-17328,17334-17800`。

## IC-10：战斗查询

### `CvUnitInfo` 静态数据

| Python 方法 | 语义 |
|---|---|
| `getMaxHitPoints()` | 单位类型最大生命 |
| `getArmour()` | 单位类型基础护甲 |
| `getAttackCount()` | 单位类型近战攻击次数 |
| `getCombat()` / `getCombatDefense()` | 攻击 / 防守强度 |
| `getAirCombat()` / `getAirCombatCount()` | 远程强度 / 次数 |
| `getAirRange()` | 最大远程距离 |
| `getMoves()` | XML 移动格数 |

### `CyUnit` 实例数据

| Python 方法 | 语义 |
|---|---|
| `maxHitPoints()` / `currHitPoints()` | 实例生命上限 / 剩余生命 |
| `armourValue()` | 带实例修正的护甲 |
| `unitCombatAttacks()` | 带实例修正的近战次数 |
| `baseCombatStr()` | 实例基础攻击强度 |
| `airRange()` | 实例远程最大距离 |

空 `CyUnit` wrapper 对这些整数查询通常返回 `-1`；Python UI 不应把 `-1` 当成合法属性展示。`getDexterity()`、`getAttackCountVariance()`、`getAirRangeMin()`、`getUnitPlotCost()` 与地形 `getUnitPlotSupport()` 在 C++ 信息类存在，但 Rampage 的 `CyInfoInterface` 没有对应 `.def` 证据，因此不属于 Python 公共接口。

事实证据：`CyInfoInterface1.cpp:211-245,330-335`；`CyUnitInterface2.cpp:125-170`；`CyUnit.cpp:643-681`。

## IC-11：固定 Python 模块名

`CvDefines.h` 的字符串是 DLL 调用 Python 的 ABI：

| 宏 | 固定模块名 | 主要职责 |
|---|---|---|
| `PYScreensModule` | `CvScreensInterface` | 屏幕入口 |
| `PYGameModule` | `CvGameInterface` | 游戏规则回调 |
| `PYEventModule` | `CvEventInterface` | 事件统一入口 |
| `PYRandomEventModule` | `CvRandomEventInterface` | 随机事件函数 |
| `PYSpellModule` | `CvSpellInterface` | 法术及 XML 表达式 |
| `PYCivModule` | `CvAppInterface` | 宿主应用入口 |
| `PYWorldBuilderModule` | `CvWBInterface` | 世界编辑器 |
| `PYPopupModule` | `CvPopupInterface` | 弹窗 |
| `PYDiplomacyModule` | `CvDiplomacyInterface` | 外交 |
| `PYTextMgrModule` | `CvTextMgrInterface` | 文本回调 |
| `PYSomniumModule` | `CvSomniumInterface` | Somnium |
| `PYDataStorageModule` | `CvDataStorageInterface` | trophy 数据 |

还包括 `CvDebugInterface`、`CvUnitControlInterface`、`CvPerfTest`、`DebugScripts`、`PbMain`、`CvTranslator`。更名任何模块都必须同步 C++ 宏、目标 Python 文件/外部基础模块和所有 import。

覆盖包包含 `CvGameInterface.py`、`CvScreensInterface.py`、`CvSpellInterface.py`，但不包含 `CvEventInterface.py` 与 `CvGameInterfaceFile.py`。后两者是外部基础依赖；接口文档不推测其内部实现。

事实证据：`CvDefines.h:147-167`；`CvGameInterface.py:1-18`；覆盖包文件清单。

## 失败表现

- 模块或函数名不匹配：`callFunction` 返回失败或 Python 抛错；C++ 调用点不都有安全回退。
- `.def` 缺失：Python 得到 `AttributeError`，即使同名 C++ getter 存在。
- enum 顺序漂移：Python 传回的整数会指向错误信息项，通常不会产生类型安全错误。
- 空 wrapper：多数整数查询用 `-1`，布尔查询用 `false`；调用方必须区分哨兵与业务值。
- 生命周期越界：缓存临时 event 对象可能访问已释放 wrapper 或栈数据。
- DLL/Python ABI 不兼容：`CvPythonExtensions` 可能无法导入，无法用普通 `.py` 回退。

## 变更联动

| 变更 | 必查范围 |
|---|---|
| 增加或删除 Cy 方法 | 底层 C++、Cy wrapper、头文件、`.def`、Python 调用、空对象哨兵、生命周期 |
| 改返回对象 | return policy、所有权、事件同步/异步使用、调用方缓存 |
| 改 enum | C++ enum、Cy enum、XML 顺序、Python 比较、数组和存档 |
| 改模块名 | `CvDefines.h`、Python 文件、imports、所有 `callFunction`、外部基础清单 |
| 改玩家食物语义 | `CvPlayer`、CyPlayer、Commerce enum/XML、HUD、财务顾问、文本、DLL |
