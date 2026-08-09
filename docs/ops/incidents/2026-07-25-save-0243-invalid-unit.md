# 2026-07-25：回合 0243 无效单位导致读档崩溃

状态：坏对象、创建源和源码根因均已锁定；已完成 100% 定点复现、存档恢复和永久代码修复。

## 现象与范围

问题文件为 `zsts 回合-0243.CivBeyondSwordSave`。使用 `Magister Modmod for FfH2` 读档时，进程在加载后或单位回合处理中以访问冲突退出；`PythonErr.log` 没有能直接指出坏单位的异常。问题不是简单的 Python 导入错误。

## 结论

存档中存在且仅发现一个内部信息指针为空的 `CvUnit`：

| 字段 | 值 |
|---|---:|
| owner | `50`（野蛮人） |
| unit ID | `16548042` |
| unit type | `-1`（`NO_UNIT`） |
| 坐标 | `(141, 27)` |
| `m_pUnitInfo` | `0` |

它仍在玩家单位容器中，但类型已经是 `NO_UNIT`。读档时 `CvUnit::read` 因类型为 `NO_UNIT` 把 `m_pUnitInfo` 设为 `NULL`；Release DLL 中断言不能阻止该对象继续存在。之后单位回合和重载路径调用 `getSpecialUnitType()` 或 `getGroupDefinitions()`，直接解引用空 `m_pUnitInfo`，产生 `0xc0000005`。

仓库的对应 C++ 结构证据位于：

- `Rampage/Assets/src/CvGameCoreDLL.041o/CvUnit.cpp`：`CvUnit::read` 在读入类型后设置 `m_pUnitInfo`；`getSpecialUnitType()` 和 `getGroupDefinitions()` 直接访问它。
- `Rampage/Assets/src/CvGameCoreDLL.041o/CvPlayer.cpp`：`CvPlayer::doTurnUnits()` 会在单位循环中调用 `getSpecialUnitType()`。

运行 DLL 的崩溃点分别落在 `CvPlayer::doTurnUnits()` 内的 RVA `0x00190fa6`，以及 `CvUnit::getGroupDefinitions()` 内的 RVA `0x002687b6`。这些地址只用于识别本次 DLL，不是跨构建稳定接口。

## 排查证据链

1. 先保存并清空 Civ4 Python 日志，复现读档崩溃；没有发现能解释访问冲突的 Python traceback。
2. 在 `onLoadGame` 临时加入单位清单和 90 秒暂停。日志枚举了 `1272` 个单位，并写出了 `owner=50 id=16548042 type=-1 x=141 y=27`。
3. 内存扫描器从正常日志记录学习当前进程的 `CvUnit` vtable，再按本次 DLL 的字段布局扫描对象。
4. 扫描得到 `1208` 个可信候选；其中仅一个对象的 `m_pUnitInfo == 0`，身份与日志中的无效单位完全一致。
5. dump/反汇编确认崩溃指令从 `CvUnit + 0x1f4` 取 `m_pUnitInfo`，随后访问其成员；这与空指针证据一致。

因此，“XML 中缺少某个本应存在的单位定义”并不是准确表述：`UNIT_PRIEST_RINGGIVER` 和 `UNIT_HIGH_PRIEST_RINGGIVER` 的定义都存在。真正的问题是 Python 列表中两个相邻字符串之间少了逗号，解释器把它们自动拼成不存在的 `UNIT_PRIEST_RINGGIVERUNIT_HIGH_PRIEST_RINGGIVER`；`gc.getInfoTypeForString(...)` 随后返回 `-1`。

## 修复过程

1. 保留原文件，不原地覆盖。
2. 在带暂停的临时诊断会话中，找到一个单位类型 `4` 的活对象作为内部信息指针供体。
3. 只对 `owner=50 / id=16548042` 的坏对象临时写入类型 `4` 和供体 `m_pUnitInfo`，使 `kill` 调用不再先因空指针崩溃。
4. 第一次 `kill` 调用抛出 “unidentifiable C++ exception”。该会话另存出的 `zsts 回合-0243-已修复.CivBeyondSwordSave` 虽然可加载，但永久诊断日志随后证明对象仍被序列化为 `owner=50 / id=16548042 / type=4`。因此这个文件只是中间产物，不能视为最终修复。
5. 仅在一次恢复会话的 `onLoadGame` 中加入精确删除钩子：通过 `gc.getPlayer(50).getUnit(16548042)` 取得这个已经暂时可调用的对象，再执行 `kill(False, PlayerTypes.NO_PLAYER)`。
6. `PythonDbg.log` 明确记录了该对象的删除开始和完成；紧接着生成的诊断日志枚举 `1271` 个单位、`badUnits=0`，并且不再包含 ID `16548042`。
7. 另存为 `zsts 回合-0243-已修复-无坏单位.CivBeyondSwordSave`，退出游戏，撤掉精确删除钩子并恢复仓库中的常规诊断入口。
8. 从全新游戏进程加载最终文件；交付时将文件名统一为 `zsts 回合-0243-已修复.CivBeyondSwordSave`。

临时写成类型 `4` 只是让对象能够被安全删除，并不代表坏单位原本应该是类型 `4`。

## 验证结果

- 已撤掉临时删除钩子；运行目录的 `CvEventManager.py` 与仓库常规版本哈希一致。
- 最终修复存档可从全新进程正常加载并进入第 `243` 回合。
- 冷启动日志 `save-load-20260725-193643-turn-0243-pid-44228.log` 为 `units=1271 badUnits=0`，全文没有 `id=16548042`。
- 冷启动后的 `PythonErr.log` 为 `0` 字节。`PythonDbg.log` 包含模组正常调试输出，但没有 `FFH2_SAVE_REPAIR` 临时钩子标记。
- 游戏可以正常退出，未再次触发原访问冲突。

文件指纹：

| 文件 | SHA-256 |
|---|---|
| `zsts 回合-0243.CivBeyondSwordSave` | `0DB3961CDDCDF730052D98794ECFDA5099C8D02053F1A7FBA705D8A0000338D5` |
| 第一次可加载但仍含伪类型单位的中间产物（已废弃） | `0BAF01D91E24110EDB27E3E3BC1DE6F64DE4868ED55490BAB41443A5C3C6D339` |
| `zsts 回合-0243-已修复.CivBeyondSwordSave`（最终交付） | `C26A5A118AF8830C056E2888EC828920E3ACDD78761D1115565CEDB39E9044EA` |

第一次带注入的修复会话在 `kill` 后曾报告异常，该会话退出时也出现 Runtime Error。永久单位清单在此处发挥了关键作用：它证明“能读档”并不等于“坏对象已经删除”，避免把类型 `4` 的伪造单位留在正式存档。最终结论只以精确 ID 消失、`badUnits=0`、干净进程成功加载且正常退出为准。

## 100% 根因复现

使用回合 `0242` 的干净存档，把发条之城“大恶事件”的选择临时定点到疑似字符串，并在原生 `initUnit` 调用前后写日志。玩家 `0` 的刺客 `owner=0 / id=999464 / type=143` 当时位于发条之城 `(141,27)`；执行“探索史诗巢穴”后，日志得到：

```text
FFH2_CLOCKWORK_REPRO_PICK monster=UNIT_PRIEST_RINGGIVERUNIT_HIGH_PRIEST_RINGGIVER resolved=-1 x=141 y=27 casterOwner=0 casterId=999464 casterType=143
FFH2_CLOCKWORK_REPRO_INIT_BEFORE owner=50 type=-1 x=141 y=27
```

没有出现 `INIT_AFTER`。`PythonErr.log` 的完整调用链为：

```text
CvSpellInterface.cast
  -> spellExploreLairEpic
  -> CustomFunctions.exploreLairBigBad
  -> CvPlayer.initUnit(-1, 141, 27, UNITAI_LAIRGUARDIAN, ...)
RuntimeError: unidentifiable C++ exception
```

这解释了整个损坏过程：

1. `CustomFunctions.py` 的发条之城怪物列表原来写成：

   ```python
   'UNIT_PRIEST_RINGGIVER'
   'UNIT_HIGH_PRIEST_RINGGIVER'
   ```

   Python 将两个字面量静默拼接，而不是报语法错误。
2. 随机选择命中该拼接项后，类型解析为 `NO_UNIT (-1)`。
3. `initUnit(-1)` 在原生层创建/登记对象后才抛出异常，给野蛮人玩家 `50` 留下半初始化 `CvUnit`。
4. 事件异常被 Python 事件框架记录后，游戏仍继续执行 `OnPreSave`；自动档于是把坏对象持久化。
5. 下一次读档恢复该对象时，`m_pUnitInfo` 为空；后续单位回合直接解引用并崩溃。

实验自动档 `AutoSave_回合-0243.CivBeyondSwordSave` 的 SHA-256 为 `24C5F83FD225B2AB19661760386D8CB51FEE192A1420AD7034F753F15FCEB7D7`。它已移出游戏存档目录，保存在排障隔离目录中，不得作为可玩存档使用。

## 单位归属与早期误判更正

坏对象不是给玩家的维尔吉尔，也不是维尔吉尔的游魂。坐标恰好位于发条之城，早期只根据位置推测 `UNIT_VELGYR`，但 100% 复现和调用栈已经否定该推测。

这条事件的预期结果是生成一个 `owner=50 / UNITAI_LAIRGUARDIAN` 的敌对野蛮人守卫；源码作者原本想把以下两个单位分别放进随机列表：

- `UNIT_PRIEST_RINGGIVER`：巧匠
- `UNIT_HIGH_PRIEST_RINGGIVER`：教官

由于原代码把两个候选意外合并，不能再从坏对象判断本次随机本来会落到“巧匠”还是“教官”。先前为玩法测试而手动创建的玩家 `0` 维尔吉尔不是正确替代物，未保存进正式存档；一次性创建钩子也已撤除。

## 永久代码修复

`MM源码/Assets/python/CustomFunctions.py` 已做两层修复：

1. 在 `UNIT_PRIEST_RINGGIVER` 后补上缺失的逗号，使“巧匠”和“教官”恢复为两个有效候选。
2. 在调用 `initUnit` 前同时验证怪物、随从和晋升的 `getInfoTypeForString` 结果。任何一项为 `-1` 时，写出 `FFH2_LAIR_INVALID_TYPE_ABORT` 并中止事件，禁止无效 ID 进入原生层。

同类静态扫描还发现 `doEffectCrucible` 的两个晋升列表各少一个逗号（`PROMOTION_EXTENSION1`/`PROMOTION_ILLUSIONIST`、`PROMOTION_ELEMENTAL`/`PROMOTION_UNDEAD`），也已一并修正。100% 实验分支和 `FFH2_CLOCKWORK_REPRO_*` 标记已从运行目录删除。

## 两个有效候选的回归验证

永久修复后又分别把两个预期候选临时设为 100%，均从回合 `0242` 的干净存档在发条之城执行“探索史诗巢穴”：

```text
FFH2_CLOCKWORK_VALID_TEST_PICK phase=ARTIFICER monster=UNIT_PRIEST_RINGGIVER unit=228 x=141 y=27 casterOwner=0 casterId=999464
FFH2_CLOCKWORK_VALID_TEST_CREATED phase=ARTIFICER owner=50 id=16580652 type=228 x=141 y=27

FFH2_CLOCKWORK_VALID_TEST_PICK phase=INSTRUCTOR monster=UNIT_HIGH_PRIEST_RINGGIVER unit=227 x=141 y=27 casterOwner=0 casterId=999464
FFH2_CLOCKWORK_VALID_TEST_CREATED phase=INSTRUCTOR owner=50 id=16580652 type=227 x=141 y=27
```

两轮都完整经过 `PICK -> CREATED`，没有 `NO_UNIT`，也没有原来的 `initUnit(-1)` C++ 异常。两轮实验自动档均已移出游戏存档目录；测试结束后 `FFH2_CLOCKWORK_VALID_TEST_*` 和 100% 分支已撤销，运行模组恢复正常随机。

测试日志仍记录了 `CvEventManager.onUnitBuilt/onUnitCreated` 的中文名称 `UnicodeEncodeError`。它不影响这两个单位完成创建，也不是本次坏档根因，应作为独立的本地化日志问题处理。

## 未来处理

按[存档加载与坏单位诊断](../save-load-diagnostics.md)保留诊断功能。出现同类问题时，先用日志找 `BAD_UNIT` 的 `owner + id`，再用只读内存扫描确认指针；只有证据唯一一致时才在副本上使用修复模式。若出现 `FFH2_LAIR_INVALID_TYPE_ABORT`，应直接修正日志给出的玩法配置/列表字符串，不要再尝试创建该单位。若日志没有无效类型，不要假定仍是同一原因，应重新获取 dump 和调用栈。
