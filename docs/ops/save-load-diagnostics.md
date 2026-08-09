# 存档加载与坏单位诊断

本功能用于处理“存档在加载后崩溃、回合开始时崩溃，怀疑存在无效 `CvUnit`”的问题。它和 BUG Autolog 分开：Autolog 记录游戏事件，本功能在每次读档时枚举所有单位并记录 `owner`、单位 `id`、单位类型和坐标，因此可以直接锁定坏对象。

## 组成与默认策略

| 组成 | 项目位置 | 作用 |
|---|---|---|
| 游戏内日志模块 | `MM源码/Assets/python/SaveDiagnostics.py` | 在 `onLoadGame` 中生成单位清单 |
| BUG 配置定义 | `MM源码/Assets/Config/Save Diagnostics.xml` | 定义开关、目录、暂停和保留数量 |
| 事件入口 | `MM源码/Assets/python/CvEventManager.py` | 读档后调用诊断模块 |
| 内存扫描器 | `tools/save-diagnostics/scan_civ4_units.py` | 用日志样本在运行进程中定位 `CvUnit` 和空 `m_pUnitInfo` |
| 扫描器配置 | `tools/save-diagnostics/config.json` | 配置日志和 JSON 报告目录 |

仓库中的 BUG 默认值是关闭，避免普通发布包每次读档都生成大型清单。本机排障环境已单独启用，配置文件为：

```text
$USERPROFILE\Documents\My Games\beyond the sword\FFH - More Naval AI\Settings\Save Diagnostics.ini
```

本机日志目录配置为：

```text
$USERPROFILE\Documents\My Games\Beyond the Sword\Logs\FFH2SaveDiagnostics
```

扫描报告默认进入其 `reports` 子目录。路径可在上述 INI 和 `tools/save-diagnostics/config.json` 中修改；两处应保持一致。`PythonDbg.log` 和 `PythonErr.log` 仍由 Civ4 自身写入固定的 `Beyond the Sword\Logs`，不受本功能控制。

## 配置项

```ini
[SaveDiagnostics]
Enabled = True
Log Directory = $USERPROFILE\Documents\My Games\Beyond the Sword\Logs\FFH2SaveDiagnostics
Pause Seconds = 0
Max Files = 20
```

- `Enabled`：是否在每次读档时生成单位清单。
- `Log Directory`：绝对路径、使用 `$VARNAME`/`${VARNAME}` 的环境变量路径、BUG 根目录相对路径，或 `Default`。旧版 BUG 配置会错误处理 Windows `%VARNAME%` 写法，因此不要在此 INI 中使用百分号语法。
- `Pause Seconds`：日志关闭前的等待秒数。日常保持 `0`；需要让外部扫描器附加到即将崩溃的进程时可临时设为 `90`。
- `Max Files`：保留最新的诊断日志数量；小于 `1` 表示不自动清理。

日志文件名形如 `save-load-20260725-123456-turn-0243-pid-12345.log`。重点标记为：

```text
FFH2_SAVE_DIAG_BAD_UNIT owner=50 id=16548042 type=-1 x=141 y=27
```

只要出现 `FFH2_SAVE_DIAG_BAD_UNIT` 或 `FFH2_SAVE_DIAG_UNIT_EXCEPTION`，就应先复制原存档并停止覆盖保存。

## 标准排查流程

1. 关闭游戏，复制原存档并计算 SHA-256；所有试验都在副本上进行。
2. 启用 `Save Diagnostics.ini`。通常先保持 `Pause Seconds = 0`，加载一次问题存档。
3. 查看最新 `save-load-*.log`，搜索 `BAD_UNIT`、`UNIT_EXCEPTION` 和最后的 `SUMMARY`。
4. 如果日志已经给出无效类型，记录 `owner` 和 `id`；如果仍需确认内部指针，把暂停改为 `90` 后重新读档。
5. 在暂停期间取得进程号：

   ```powershell
   (Get-Process Civ4BeyondSword).Id
   ```

6. 从仓库根目录执行只读扫描：

   ```powershell
   python tools\save-diagnostics\scan_civ4_units.py --pid <PID>
   ```

   未显式传入 `--log` 时，工具读取配置目录中最新的诊断日志；未传入 `--output` 时，JSON 报告写到配置的 `report_directory`。

7. 将扫描报告中的 `suspect_candidates` 与日志的 `owner`、`id`、类型和坐标交叉核对。只有日志与内存证据指向同一个对象，才进入修复。
8. 在游戏能完整加载、正常运行并正常退出后，才把新存档标记为已修复。复查诊断日志中 `badUnits=0`，同时检查 `PythonDbg.log`、`PythonErr.log` 和 Windows 崩溃记录。

## 从坏对象反推创建源

`type=-1` 只能证明对象无效，不能直接告诉我们原始字符串。要找真正的写入点，使用“好档/坏档差分 + 原生调用边界日志 + 定点复现”：

1. 比较最后一个好档和第一个坏档的单位坐标。重点查看坏对象所在格，以及同一时刻从该格移开的玩家单位。
2. 搜索所有可能调用 `initUnit`、`convert`、`kill` 的玩法入口，特别是回合效果、探索巢穴、随机事件和自动施法。
3. 在进入原生调用前记录：入口名、施法/触发单位的 `owner + id + type`、候选字符串、`getInfoTypeForString` 结果、坐标和随机分支。
4. 只在存档副本和临时运行目录中把目标分支调为 100%。同时把候选选择定点到疑似项，否则“事件必触发”仍不能保证命中有问题的列表元素。
5. 在原生调用后再写一条日志。若只有 `INIT_BEFORE`、没有 `INIT_AFTER`，再结合 `PythonErr.log` 的 traceback，即可把异常锁定在原生边界。
6. 观察异常后是否仍执行 `OnPreSave`。若执行，说明“异常已记录但半初始化对象仍被自动保存”是可能的持久化路径。
7. 实验结束后立刻退出、不手动保存；将实验自动档移出游戏存档目录，并撤销概率和定点选择代码。

对于 Python 列表，必须额外检查“相邻字符串少逗号”。Python 会把：

```python
'UNIT_A'
'UNIT_B'
```

静默编译成 `UNIT_AUNIT_B`。可用以下只读扫描先找候选，再逐处人工确认；第三方库中用于长错误消息的相邻字符串可能是合法写法：

```powershell
rg -n -U --pcre2 "'[^'\r\n]*'\s*\r?\n\s*'[^'\r\n]*'" MM源码\Assets\python -g "*.py"
```

所有由字符串解析出的单位、随从、晋升或建筑 ID，都应在进入原生创建/设置接口前检查是否为 `-1`。玩法侧推荐记录明确标记并中止，例如本项目的 `FFH2_LAIR_INVALID_TYPE_ABORT`。

## 内存修复模式

扫描器默认只读。修复模式会修改正在运行的 Civ4 进程，必须同时给出三个参数：

```powershell
python tools\save-diagnostics\scan_civ4_units.py `
  --pid <PID> `
  --repair-type <临时有效类型> `
  --repair-owner <owner> `
  --repair-id <unit-id>
```

工具只允许恰好一个可疑对象与 `owner + id` 匹配，否则拒绝写内存。它借用同类型活单位的 `m_pUnitInfo`，把坏对象临时变成可调用状态；随后仍需按精确 `owner + id` 调用该单位的 `kill(False, PlayerTypes.NO_PLAYER)`，再另存为新文件。临时类型不是业务修复，不能保留该伪造单位继续游戏。

修复模式有以下硬限制：

- 只用于 32 位 Civ4/BtS 进程。
- `CvUnit` 字段偏移针对本次 DLL 布局：ID `+0x0c`、坐标 `+0x18/+0x1c`、owner `+0x1e4`、类型 `+0x1ec`、`m_pUnitInfo +0x1f4`。
- 更换 DLL 或源码线后必须重新验证布局；不得直接假设偏移兼容。
- 先备份，绝不覆盖唯一原存档；修复后必须全新启动游戏复验。

## 能证明什么

游戏内清单能证明 Python 枚举到的单位身份和公开单位类型；内存扫描能进一步证明该进程中对象的 `m_pUnitInfo` 是否为空。二者都不能单独证明无效对象是在哪一回合、由哪段玩法逻辑创建的。若崩溃发生在 `onLoadGame` 之前，仍需要 Windows dump 或调试器调用栈。

本次实际案例和证据链见[2026-07-25：回合 0243 无效单位导致读档崩溃](./incidents/2026-07-25-save-0243-invalid-unit.md)。
