# XML → C++ 接口契约

## 读者入口

本文回答三件事：XML 怎样进入 `CvInfo`；五类定制机制依赖哪些固定字段；字段或类型变化时哪些层必须共同变化。桥接到 Python 的方法见 [C++ → Python](cpp-python-contract.md)。

## IC-01：信息类装载

### 固定方向与输入输出

`CvXMLLoadUtility::LoadPreMenuGlobals` 按固定文件根、目录和 XML 节点路径调用 `LoadGlobalClassInfo<T>`。后者读取缓存或 `xml\{目录}/{文件根}.xml`，再由 `SetGlobalClassInfo<T>` 对每个目标节点：

1. 构造 `T`。
2. 调用 `T::read(CvXMLLoadUtility*)`。
3. 以 `Type` 查找既有索引；新类型追加，重复类型替换同一槽位。
4. 对 `bTwoPass=true` 的信息类执行 `readPass2`；若干类型随后由调用者执行 `readPass3`。

| 信息类 | 文件 | 固定节点路径 | 多遍读取 |
|---|---|---|---|
| `CvUnitInfo` | `XML/Units/CIV4UnitInfos.xml` | `Civ4UnitInfos/UnitInfos/UnitInfo` | `read`、`readPass2`、`readPass3` |
| `CvTerrainInfo` | `XML/Terrain/CIV4TerrainInfos.xml` | `Civ4TerrainInfos/TerrainInfos/TerrainInfo` | `read`、`readPass2`、`readPass3` |
| `CvFeatureInfo` | `XML/Terrain/CIV4FeatureInfos.xml` | `Civ4FeatureInfos/FeatureInfos/FeatureInfo` | `read`、`readPass2` |
| `CvImprovementInfo` | `XML/Terrain/CIV4ImprovementInfos.xml` | `Civ4ImprovementInfos/ImprovementInfos/ImprovementInfo` | `read`、`readPass2`、`readPass3` |
| `CvCommerceInfo` | `XML/Gameinfo/CIV4CommerceInfo.xml` | `Civ4CommerceInfo/CommerceInfos/CommerceInfo` | `read` |
| `CvSpellInfo` | `XML/Units/CIV4SpellInfos.xml` | `Civ4SpellInfos/SpellInfos/SpellInfo` | `read` |

输入是合并后模组目录中的 XML 和可能命中的 `.dat` 缓存；输出是 `CvGlobals` 中按索引保存的信息对象。模块化 XML 开启时，`modules\*_{文件根}.xml` 继续进入同一类型表，重复 `Type` 覆盖原槽位。

### 失败表现

- 文件载入失败：`LoadCivXml` 返回 `false`，装载器显示 `XML Load Error`。
- `read` 返回失败：断言触发并终止该类循环；不能假定其余条目可靠。
- 重复 `Type`：不是自动报错，而是替换同一索引对象。
- 缓存写失败：显示 `XML Caching Error`；缓存命中可能绕过文本读取。
- Schema 与数据不一致：宿主是否在载入期拒绝取决于其 XML 实现，必须在目标环境确认。

事实证据：`CvXMLLoadUtility.cpp:348-372`；`CvXMLLoadUtilitySet.cpp:775-932,1617-1696,1743-1821`。

## IC-02：`Type` 身份

`CvInfoBase::read` 提供的 `Type` 字符串是跨层主键。`SetGlobalClassInfo` 使用 `GC.getInfoTypeForString` 与 `GC.setInfoTypeFromString` 把字符串映射为数组索引；XML 的交叉引用、C++ enum/int、Python `gc.getInfoTypeForString` 和 UI widget 参数都依赖这个映射。

契约要求：

- `Type` 大小写和拼写固定。
- 重命名必须同步所有 XML 引用、Defines、C++ 字符串、Python 字符串、文本链接和场景引用。
- 删除或插入顺序敏感的信息项前，先核对 C++ enum、Python enum、数组序列化和存档兼容。
- 不把显示文本 `Description` 当成身份。工人逻辑通过本地化后的 `Work Tile` 比较来识别建造是一个静态脆弱点；身份契约仍应以 `BUILD_WORK_TILE` 为准。

事实证据：`CvXMLLoadUtilitySet.cpp:1649-1667`；`CvUnit.cpp:1477-1566`；`CIV4BuildInfos.xml:593-610`。

## IC-03：单位战斗与远程字段

| XML 字段 | C++ 成员 / getter | 语义消费者 | Python 可见性 |
|---|---|---|---|
| `iCombat` | `m_iCombat` / `getCombat()` | 近战强度 | `CvUnitInfo.getCombat` |
| `iCombatDefense` | `m_iCombatDefense` / `getCombatDefense()` | 防守强度 | `CvUnitInfo.getCombatDefense` |
| `iMaxHitPoints` | `m_iMaxHitPoints` / `getMaxHitPoints()` | 承伤上限 | info 与 `CyUnit.maxHitPoints` |
| `iArmour` | `m_iArmour` / `getArmour()` | 单次伤害 | info 与 `CyUnit.armourValue` |
| `iDexterity` | `m_iDexterity` / `getDexterity()` | 闪避/命中门槛 | DLL 内可用；未见 Boost.Python `.def` |
| `iAttackCount` | `m_iAttackCount` / `getAttackCount()` | 近战掷骰数 | info 与 `CyUnit.unitCombatAttacks` |
| `iAttackCountVariance` | `m_iAttackCountVariance` | 攻击次数方差 | DLL 内可用；未见 Boost.Python `.def` |
| `iAirRangeMin` | `m_iAirRangeMin` / `getAirRangeMin()` | 远程最小距离 | DLL 内可用；未见 info `.def` |
| `iAirRange` | `m_iAirRange` / `getAirRange()` | 远程最大距离 | info 与 `CyUnit.airRange` |
| `iAirCombat` | `m_iAirCombat` / `getAirCombat()` | 远程单次伤害 | `CvUnitInfo.getAirCombat` |
| `iAirCombatCount` | `m_iAirCombatCount` / `getAirCombatCount()` | 远程射击数 | `CvUnitInfo.getAirCombatCount` |

所有字段输入为整数。结算输出不是新的 XML 对象，而是 `CvUnit` 的生命、移动力、战斗事件与 UI dirty bit。Python 可见性只能以 `.def` 发布为准，`CvInfos.h` 的 “Exposed to Python” 注释不构成发布证据。

### Schema 闭合风险

`CIV4UnitSchema.xml:303-359` 声明了上述若干 `ElementType`，但 `UnitInfo` 内容模型在 `:655-705` 没有列入 `iAirRangeMin`、`iMaxHitPoints`、`iArmour`、`iDexterity`、`iAttackCount`、`iAttackCountVariance`、`iAirCombatCount`；XML 数据与 `CvUnitInfo::read` 却使用这些名字。完整契约要求“类型声明、`UnitInfo` 内容模型、数据节点、C++ 读取”四者闭合。

另一个静态风险是 `CvUnitInfo` 构造器的初始化列表没有显式初始化其中若干自定义成员，而 Schema 把字段声明为可选。任何省略字段的条目都必须通过目标编译与运行验证其值，不能假定为零。

事实证据：`CIV4UnitSchema.xml:303-359,655-705`；`CIV4UnitInfos.xml:110-155`；`CvInfos.cpp:4837-4910,7262-7302`；`CvUnit.cpp:1750-2049,19352-19631`。

## IC-04：基于回合起点的 `plotDistance` 移动半径与地块容量

### 数据输入

| 固定名 | 来源 | C++ 读取/消费 |
|---|---|---|
| `iMoves` | UnitInfo | 单位基础移动格数；有效最大移动格数的一项输入 |
| `iUnitPlotCost` | UnitInfo | 单位占用成本 |
| `iUnitPlotSupport` | Terrain / Feature / Improvement | 地块容量加项 |
| `City_Unit_Capacity` | `GlobalDefinesAlt.xml` | 城市基础容量；大小写固定 |
| `AIR_SPACE_CAPACITY` | 同上 | 飞行单位容量 |
| `HILLS_CAPACITY_MODIFIER` | 同上 | 丘陵容量修正 |
| `CITY_POPULATION_CAPACITY_DIVISOR` | 同上 | 人口容量除数 |
| `CITY_POPULATION_CAPACITY_FACTOR` | 同上 | 人口容量因子 |

`iMoves` 只提供 `CvUnitInfo::getMoves()` 的基础值；`CvUnit::baseMoves()` 还会加上单位额外移动 `getExtraMoves()` 和团队按领域额外移动。`maxMoves()` 将该有效最大移动格数乘以 `MOVE_DENOMINATOR`，`CvUnit::canMoveInto()` 再以 `maxMoves() / MOVE_DENOMINATOR` 得到本回合的 `plotDistance` 移动半径。因此最终边界不是直接取原始 `iMoves`。

`CvPlot::getUnitPlotCapacity()` 计算地形、地物、改良、丘陵和城市项；城市分支会减去地形支撑。`CvUnit::canMoveInto()` 使用 `m_iXinital/m_iYinital` 记录的回合起点与上述有效移动半径限制移动边界，并在非攻击性进入时应用容量拒绝。`plotDistance` 遵循 `max(dx, dy) + floor(min(dx, dy) / 2)`，其边界呈离散网格上的近似八边形，而非欧氏圆。

输出是 `bool` 合法性和移动提交结果。除数为零、Define 缺失、字段负值或未初始化都没有文档化的安全降级，属于配置错误。

静态未知：回合起点在 `doTurn` 更新，但未找到 `m_iXinital/m_iYinital` 的流读写；回合中途存读档语义需运行确认。

事实证据：`CIV4UnitSchema.xml:303,670`；`CIV4TerrainSchema.xml:30,70,174,513`；`GlobalDefinesAlt.xml:434-452`；`CvInfos.cpp:7270,15312,16466,17037`；`CvGameCoreUtils.h:143-152`；`CvUnit.cpp:1303-1305,3591-3595,3608-3641,9377-9386`；`CvPlot.cpp:3423-3488`。

## IC-05：`COMMERCE_FOOD`

`COMMERCE_FOOD` 必须在三处保持相同序位：

1. `CvEnums.h` 的 `CommerceTypes`：位于 gold、research、culture、espionage 之后。
2. `CyEnumsInterface.cpp` 的 `CommerceTypes.COMMERCE_FOOD`。
3. `CIV4CommerceInfo.xml` 的第五个 `CommerceInfo`，`Type=COMMERCE_FOOD`。

`SetCommerce` 按子节点顺序写入长度为 `NUM_COMMERCE_TYPES` 的数组，不根据 `Type` 重新排序。因此调整 enum 或 XML 顺序必须作为同一变更处理。

工人占格把地块食物 Yield 乘以 100 后写入玩家 `COMMERCE_FOOD` rate；玩家食物收入再读取该 rate。这个缩放是否与所有基础消费者一致需要运行对账。

事实证据：`CvEnums.h:692-705`；`CyEnumsInterface.cpp:490-500`；`CIV4CommerceInfo.xml:7-54`；`CvXMLLoadUtility.h:317-353`；`CvUnit.cpp:1518-1554`；`CvPlayer.cpp:7139-7189`。

## IC-06 / IC-07：Global Defines 与回调开关

装载顺序固定为 `GlobalDefines.xml`、`GlobalDefinesAlt.xml`、`PythonCallbackDefines.xml`，再加模块化 Defines。值节点类型决定写入 `FVariableSystem` 的 float、int、boolean 或字符串类型；同名后载入值会覆盖先载入值。

Rampage 覆盖包没有 `XML/GlobalDefines.xml`，因此第一层来自外部基础安装。`PythonCallbackDefines.xml` 提供的开关包括：

- `USE_CAN_BUILD_CALLBACK=1`
- `USE_CANNOT_TRAIN_CALLBACK=1`
- `USE_CANNOT_CONSTRUCT_CALLBACK=1`
- `USE_CANNOT_RESEARCH_CALLBACK=1`
- `USE_CANNOT_DO_CIVIC_CALLBACK=1`
- `USE_ON_UNIT_CREATED_CALLBACK=1`
- `USE_COMBAT_RESULT_CALLBACK=1`

其余开关值以该 XML 为准。开关为 `0` 表示对应 C++ 位置不进入 Python；它不是 Python handler 自行决定是否执行。

事实证据：`CvXMLLoadUtilitySet.cpp:20-223`；`PythonCallbackDefines.xml:1-119`；相应调用点散布于 `CvGame.cpp`、`CvPlayer.cpp`、`CvCity.cpp`、`CvUnit.cpp` 与 `CvDllPythonEvents.cpp`。

## 变更联动清单

| 变更 | 同步核对 |
|---|---|
| UnitInfo 字段 | Schema 类型与内容模型、所有 UnitInfo、构造默认值、流读写、getter、规则消费者、Cy 发布、UI、DLL |
| `Type` 重命名 | 全部 XML 引用、Defines、C++/Python 字符串、文本链接、场景、缓存 |
| Commerce 项 | C++ enum、XML 顺序、Python enum、所有定长数组、UI、存档 |
| 容量 Define | 名称大小写、值域、除零、AI/城市/单位三个消费者、最终基础合并值 |
| callback Define | XML 值、C++ guard、Python 函数名/参数/返回值、性能影响 |
| Spell 表达式字段 | Spell Schema、Info getter、C++ 参数上下文、Python 作用域与目标函数 |
