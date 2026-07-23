# 原生 UI 入口契约

## 边界

Rampage UI 是 Civilization IV 原生屏幕系统。宿主和 DLL 调用 `CvScreensInterface`；具体屏幕读取 `CvPythonExtensions` 中的 `Cy*` / `Cv*Info`，并依靠 dirty bit 刷新。交互目标见 [UE 规格](../../product/UE-spec.md)。

## IC-13：`CvScreensInterface`

`PYScreensModule` 固定为 `CvScreensInterface`。入口函数通常不返回数据，而是把参数委托给模块级屏幕实例的 `interfaceScreen`、`handleInput`、`update` 或专用方法。

### 产品相关入口

| 固定函数 | 输入 | 委托目标 | C++ 调用方 |
|---|---|---|---|
| `showMainInterface()` | 无 | `CvMainInterface.interfaceScreen` | 宿主 |
| `showFinanceAdvisor()` | 无 | `CvFinanceAdvisor.interfaceScreen` | `CvGameInterface` control |
| `showMilitaryAdvisor()` | 无 | military advisor | `CvGameInterface` control |
| `showDomesticAdvisor(argsList)` | control 参数 | domestic advisor | `CvGameInterface` control |
| `showTechChooser()` | 无 | tech chooser | `CvGameInterface` control |
| `showForeignAdvisorScreen(argsList)` | advisor tab | foreign advisor | control / widget |
| `pediaShow()` | 无 | civilopedia | `CvGameInterface` |
| `pediaJumpToUnit(argsList)` | unit type | civilopedia unit page | widget data |
| `pediaJumpToSpell(argsList)` | spell type | civilopedia spell page | widget data |
| `refreshMilitaryAdvisor(argsList)` | 刷新参数 | military advisor | widget data |
| `handleInput(argsList)` | screen input | active screen | 宿主 |
| `update(argsList)` | delta / screen args | active screen | 宿主 |

`CvScreensInterface.py` 还定义世界编辑器、电影、选项、胜利、信息、历史和回调入口。外部基础安装必须提供其 import 的大量屏幕模块；覆盖包中的入口文件不等于自包含 UI。

失败表现：函数名或签名不匹配时 C++ `callFunction` 失败；被 import 的屏幕类缺失时模块导入失败；错误 screen ID 或 active-screen 路由可能把输入交给错误对象。

事实证据：`CvDefines.h:147-167`；`CvScreensInterface.py:1-983`；`CvGameInterface.cpp:1847-1986`；`CvDLLWidgetData.cpp:1426-1660,4655`。

## IC-19：dirty bit 刷新

UI 使用 pull 模式：C++ 改变游戏数据并设置 dirty bit，Python `CvMainInterface.updateScreen` 或具体顾问的 `update` 检测后重新读取 Cy 接口，再把 bit 清为 `False`。

| 数据变化 | C++ 设置 | Python 消费 |
|---|---|---|
| 工人进入/离开工作地块 | `GameData`、`Score`、`CityScreen`、`Financial_Screen`、`InfoPane` | 主界面、财务顾问、城市/信息面板 |
| 工作地块 build 改变产出 | 同上 | 同上 |
| 玩家食物储备/每回合修正 | `MiscButtons`、`SelectionButtons`、`GameData` | 主界面游戏数据区 |
| 单位属性/选择变化 | `InfoPane`、`SelectionButtons`、`UnitInfo` | 选中单位面板与动作栏 |

`CvFinanceAdvisor.update` 只在 `Financial_Screen_DIRTY_BIT` 为真时重画。若规则改变了财务数据却只设置 `GameData`，已打开的财务顾问可能不刷新。因此规则写入与 UI dirty bit 属于同一接口变更。

事实证据：`CvUnit.cpp:1477-1566,8407-8446`；`CvPlayer.cpp:8711-8759`；`CvMainInterface.py:884-938`；`CvFinanceAdvisor.py:278-284`。

## 五类机制的 UI 数据流

### 近战属性与预览

- 选中单位面板读取 `CyUnit.currHitPoints()`、`maxHitPoints()`、`armourValue()`、`baseCombatStr()`、`unitCombatAttacks()`。
- 百科单位页读取 `CvUnitInfo.getMaxHitPoints()`、`getArmour()`、`getCombat()`、`getCombatDefense()`、`getAttackCount()`。
- C++ 战斗预览由 `CvGameTextMgr` 直接读取同一规则对象；Python 不复制结算公式。
- 战斗日志通过 `combatLogCalc/Hit/Miss` 事件显示骰值、门槛、伤害和剩余生命。

事实证据：`CvMainInterface.py:3023-3057`；`CvPediaUnit.py:133-185`；`CvGameTextMgr.cpp:2771-2820`；`CvEventManager.py:602-682`。

### 远程目标模式

XML 固定身份：

```text
INTERFACEMODE_RANGE_ATTACK -> MISSION_RANGE_ATTACK
```

`CvSelectionGroup::canDoInterfaceMode` 判断组是否可进入模式，`canDoInterfaceModeAt` 判断目标地块，任务队列最终调用 `CvUnit::rangeStrike`。`iAirRangeMin/iAirRange` 是距离闭区间。远程攻击始终执行 `changeMoves(movesLeft())`，清空剩余移动力；`RANGED_ATTACKS_USE_MOVES` 不控制这项消耗，而是在值为 `0` 时额外设置 `setMadeAttack(true)`，因此影响 `madeAttack` 状态与重复动作资格。该 Define 的合并后取值仍未知。

XML 同时给 `INTERFACEMODE_RANGE_ATTACK` 与 `BUILD_WORK_TILE` 使用 `B` 热键的静态证据，实际上下文分派需宿主验证。

事实证据：`CIV4InterfaceModeInfos.xml:286-305`；`CvSelectionGroup.cpp:2037-2280`；`CvUnit.cpp:19352-19631,19456-19460`；`CIV4BuildInfos.xml:593-610`。

### 移动与容量拒绝

容量没有独立 Python 查询或专用提示契约。C++ `canMoveInto` 返回 `false` 后，原生路径/任务层不提交移动；UI 的可靠表现是目标不可执行或单位保持原位。不要在 Python 侧重复计算容量，否则 XML、AI 和宿主路径会产生第二套规则。

事实证据：`CvUnit.cpp:3439-3641`；`CvPlot.cpp:3423-3488`；`CvCity.cpp:1834-1870`。

### 工人占格生产

`CvUnit::updateCommerce` 根据 `BUILD_WORK_TILE` 条件把地块 commerce 计入 `COMMERCE_GOLD`、食物计入 `COMMERCE_FOOD`，并设置 dirty bits。UI 只读取玩家聚合值。由于 C++ 以本地化文本 `Work Tile` 识别 build，文本翻译变化可能使规则入口失效；`BUILD_WORK_TILE` 的 Type 与显示文本应分别验证。

事实证据：`CIV4BuildInfos.xml:593-610`；`CvUnit.cpp:1477-1566,12671-12681`。

### 玩家食物经济

| UI 面 | 读取接口 | 展示职责 |
|---|---|---|
| HUD | `CyGameTextMgr.getFoodStr(ePlayer)` | 储备与带符号净变化 |
| 财务顾问 | `getFood()`、`getCommerceRate(COMMERCE_FOOD)`、`calculateFoodCosts()` | 储备、收入、成本分列 |

`CvMainInterface` 通过 Python 查询入口 `CyGameTextMgr.getFoodStr(ePlayer)` 获取 HUD 文本。该入口绑定到 `CyGameTextMgr::getFoodStr`；C++ wrapper 创建字符串缓冲区并调用 `GAMETEXT.setFoodStr`，真实格式化实现是 `CvGameTextMgr::setFoodStr`，由它读取 `CvPlayer::getFood()` 与 `calculateFoodRate()`。财务顾问则直接走 CyPlayer。因此两处不应自行维护第二份食物状态。

事实证据：`CyGameTextMgrInterface.cpp:20`；`CyGameTextMgr.cpp:55-60`；`CvGameTextMgr.cpp:288-307`；`CvMainInterface.py:2089-2091`；`CvFinanceAdvisor.py:95-122,192-195,245-247`。

## IC-20：名称与资源

以下字符串都是 UI ABI，而非自由文案：

- `INTERFACEMODE_RANGE_ATTACK`、`MISSION_RANGE_ATTACK`、`BUILD_WORK_TILE`。
- `TXT_KEY_COMBAT_MESSAGE_HIT`、`TXT_KEY_COMBAT_MESSAGE_MISS`、`TXT_KEY_COMBAT_MESSAGE_DEFEATED`。
- `TXT_KEY_FINANCIAL_ADVISOR_FOODSTORES`、`TXT_KEY_FINANCIAL_ADVISOR_FOOD`、`TXT_KEY_FINANCIAL_ADVISOR_FOOD_COST`。
- `INTERFACE_PANE_HP_ARMOUR`、`INTERFACE_PANE_STRENGTH` 及百科属性文本键。
- XML 中 `Button`、Art Define、音频和模型路径。

文本键的格式参数数量与顺序必须和 `gDLL->getText` / `localText.getText` 调用一致。资源路径必须在合并后的目标目录存在；覆盖包缺少资源不能单凭仓库判定为坏引用，因为基础安装也是输入。

## 变更联动

| UI 变化 | 必查范围 |
|---|---|
| 屏幕入口改名 | `CvDefines.h`、所有 C++ `callFunction`、`CvScreensInterface`、screen import |
| 属性展示变化 | XML/CvInfo、规则 getter、Cy `.def`、文本键、HUD/百科/预览对账 |
| 远程模式变化 | InterfaceMode XML、Mission enum/info、selection group、CvUnit、动作资源、热键 |
| 财务字段变化 | CvPlayer、CyPlayer、Commerce enum/XML、dirty bit、FinanceAdvisor、文本 |
| 文本格式变化 | 所有调用点参数数量/顺序、全部语言节点、回退语言 |
| 图标/模型变化 | Art Define、XML/Python 路径、最终覆盖目录、大小写与格式 |
