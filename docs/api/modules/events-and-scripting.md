# 事件与脚本接口契约

## 边界

本文件定义三条脚本入口：`CvGameInterface` 的规则回调、`CvEventInterface.onEvent` 的事件信封、`CvSpellInterface` 的 XML 表达式执行。它们都由固定模块名、函数名、参数顺序和返回语义组成。

## IC-12：`CvGameInterface` 规则回调

`CvGameInterface.py` 是宿主固定入口。其函数不得随意改名；文件本身把参数委托给 `normalGameUtils = CvGameInterfaceFile.GameUtils`。覆盖包没有 `CvGameInterfaceFile.py`，因此具体 `GameUtils` 行为属于外部基础依赖。

代表性回调：

| Python 函数 | 典型输入 | 返回语义 | 开关 |
|---|---|---|---|
| `canBuild(argsList)` | plot x/y、build、player | 非零允许 Python 覆盖 | `USE_CAN_BUILD_CALLBACK` |
| `cannotTrain(argsList)` | city、unit、continue/visible/ignoreCost | 非零拒绝 | `USE_CANNOT_TRAIN_CALLBACK` |
| `cannotConstruct(argsList)` | city、building、continue/visible/ignoreCost | 非零拒绝 | `USE_CANNOT_CONSTRUCT_CALLBACK` |
| `cannotResearch(argsList)` | player、tech、trade | 非零拒绝 | `USE_CANNOT_RESEARCH_CALLBACK` |
| `cannotDoCivic(argsList)` | player、civic | 非零拒绝 | `USE_CANNOT_DO_CIVIC_CALLBACK` |
| `unitCannotMoveInto(argsList)` | unit、plot | 非零拒绝 | `USE_UNIT_CANNOT_MOVE_INTO_CALLBACK` |
| `getWidgetHelp(argsList)` | widget 类型与数据 | 文本 | C++ UI 调用点 |
| `AI_*` | 各自 argsList | `0` 交回 C++，`1` 表示 Python 处理 | 对应 C++ guard |

准确参数以 C++ `CyArgsList.add` 顺序为准，不能从 Python 变量名反推。`PythonCallbackDefines.xml` 的开关先决定 C++ 是否调用；关闭时 handler 不会收到事件。

事实证据：`CvGameInterface.py:1-306`；`PythonCallbackDefines.xml:1-119`；`CvGame.cpp`、`CvPlayer.cpp`、`CvCity.cpp`、`CvUnit.cpp` 中的 `callFunction(PYGameModule, ...)`。

## IC-15：事件信封

所有 `CvDllPythonEvents` 事件先添加标签与业务参数，再由 `postEvent` 固定追加六个尾字段：

```text
[tag, ...payload, bDebug, false, bAlt, bCtrl, bShift, bAllowCheats]
```

随后同步调用：

```text
CvEventInterface.onEvent(tuple) -> long
```

只有 `callFunction` 成功且返回 `1` 时，C++ 认为事件被 Python 消费。`preEvent()` 要求 Python 接口已经初始化。

`CvEventManager.handleEvent` 读取 `tag=argsList[0]`，把最后六项解释为上述控制字段，并只把中间业务参数传给 `EventHandlerMap[tag]`。添加、删除或重排尾字段必须同步适配器与 `handleEvent`。

覆盖包没有 `CvEventInterface.py`，因此从 `onEvent` 到 `CvEventManager.handleEvent` 的适配实现未知；`CvEventManager.py` 只证明 handler 侧契约。

事实证据：`CvDllPythonEvents.cpp:9-26`；`CvEventManager.py:90-216`。

## IC-16：事件标签

标签区分大小写并作为字典键。代表性标签与业务负载：

| 标签 | 业务负载（不含六个尾字段） | handler |
|---|---|---|
| `kbdEvent` | event、key、cursor x/y、plot x/y | `onKbdEvent` |
| `mouseEvent` | event、cursor x/y、plot x/y、consumed、screen IDs | `onMouseEvent` |
| `BeginGameTurn` | turn | `onBeginGameTurn` |
| `BeginPlayerTurn` | turn、player | `onBeginPlayerTurn` |
| `combatResult` | winner `CyUnit`、loser `CyUnit` | `onCombatResult` |
| `unitMove` | plot、unit、old plot | `onUnitMove` |
| `unitSetXY` | plot、unit | `onUnitSetXY` |
| `improvementBuilt` | improvement、x、y | `onImprovementBuilt` |
| `OnPreSave` | 无 | `onPreSave` |
| `gameUpdate` | generic tuple | `onGameUpdate` |

未知标签不会报专用错误：`handleEvent` 不调用 handler 并返回 `0`。这意味着拼写漂移表现为静默丢事件。

事实证据：`CvDllPythonEvents.cpp` 的各 `report*`；`CvEventManager.py:90-216`。

## IC-17 / IC-18：generic event 与战斗日志

`CvEventReporter::genericEvent(name, pyArgs)` 进入 `reportGenericEvent`，事件业务负载是一个嵌套的 Python tuple。`CvEventManager` 的战斗 handler 用 `argsList[0][0]` 取得原始参数。

| 标签 | `genericArgs` 固定顺序 | 输出 |
|---|---|---|
| `combatLogCalc` | attacker `CombatDetails`、defender `CombatDetails`、combat odds | `CvUtil.combatMessageBuilder` |
| `combatLogHit` | attacker details、defender details、`iIsAttacker`、damage、roll、required roll | 双方 combat message；生命归零时 defeated message |
| `combatLogMiss` | 同上 | 双方 miss message |

`iIsAttacker` 表示受伤方/掷骰方向的含义由 C++ 和 Python 分支共同定义，不能改成直觉布尔而不同步两端。近战和远程都复用相同三个标签。事件只有在 `USE_COMBAT_RESULT_CALLBACK` 非零且至少一方是 human 时发送。

`CombatDetails` 与 `CyUnit` 在同步回调后可能失效，handler 不得缓存。文本键 `TXT_KEY_COMBAT_MESSAGE_HIT`、`MISS`、`DEFEATED` 的格式参数数量和顺序也是接口的一部分。

事实证据：`CvEventReporter.cpp:37-40`；`CvDllPythonEvents.cpp:1138-1148`；`CvUnit.cpp:1750-1980,19470-19610`；`CvEventManager.py:602-682`。

## IC-14：`CvSpellInterface` 表达式

Spell、promotion、improvement、feature、vote 与 unit info 可保存 Python 表达式字符串。C++ 只在字符串非空时调用固定 dispatcher；dispatcher 从 info 对象取字符串并在固定局部变量上下文中 `eval`。

| dispatcher | argsList 解包 / 可用变量 | 表达式 getter | 返回 |
|---|---|---|---|
| `canCast` | `pCaster, eSpell, pPlot, pTarget` | `CvSpellInfo.getPyRequirement()` | `eval` 的布尔/整数结果 |
| `cast` | 同上 | `getPyResult()` | 无显式返回 |
| `miscast` | `pCaster, eSpell` | `getPyMiscast()` | 无显式返回 |
| `effect` | `pCaster, eProm` | promotion `getPyPerTurn()` | 无显式返回 |
| `onMove` | `pCaster, pPlot, eImp` | improvement `getPythonOnMove()` | 无显式返回 |
| `atRange` | 同上 | improvement `getPythonAtRange()` | 无显式返回 |
| `onMoveFeature` | `pCaster, pPlot, eFeature` | feature `getPythonOnMove()` | 无显式返回 |
| `vote` | `eVote, int` | vote `getPyResult()` | 无显式返回 |
| `postCombatWon/Lost` | `pCaster, pOpponent` | unit info post-combat expression | 无显式返回 |

XML 表达式示例 `reqTeleport(pCaster, pPlot, pTarget)` 依赖变量名与 `CvSpellInterface` 全局作用域中的函数。函数重命名、参数名变化、import 缺失或表达式语法错误都会在运行时暴露；不存在类型检查或沙箱。

事实证据：`CIV4UnitSpellSchema.xml:89-91,186-188`；`CIV4SpellInfos.xml` 的 `Py*` 节点；`CvSpellInterface.py:1-69`；`CvUnit.cpp:15246-15260,15991-16002,16128-16143,18225-18245`。

## 失败表现与联动

| 变化 / 故障 | 表现 | 必查范围 |
|---|---|---|
| 事件标签拼错 | handler 静默不执行 | C++ tag、适配器、`EventHandlerMap` |
| 参数顺序漂移 | 解包错误或错误对象参与规则 | 所有 `add`、dispatcher、handler |
| 六尾字段漂移 | 业务 payload 被截断或控制键错位 | `postEvent`、`handleEvent` |
| callback 开关为 `0` | Python 回调完全不发生 | 合并后 Defines、C++ guard |
| `onEvent` 返回非 `1` | C++ 认为未消费 | 外部 `CvEventInterface`、handler 返回 |
| XML 表达式错误 | `eval` 异常或错误规则效果 | Schema/data、info getter、dispatcher、函数/import |
| 临时对象被缓存 | 回调后悬空引用 | event 构造、Boost.Python policy、handler |

