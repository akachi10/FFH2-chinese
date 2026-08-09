# 故障排查

先按[环境配置](./environments.md)确认外部依赖，再按[服务生命周期](./services.md)识别失败阶段；本文件不重复安装和构建全流程。

## 排查原则

1. 先验证 Civ4/BtS，再验证未覆盖的 FFH2 Patch o，最后验证 Rampage。
2. 先确认实际路径、实际加载模组和文件哈希，再推断代码问题。
3. 修改部署内容前退出游戏并备份整个目标模组目录。
4. 一次只替换一个层次：DLL、XML、Python 或资源。
5. 安全恢复依赖部署前备份，不使用 Git 回退命令。

## 安装脚本复制到错误位置

**现象**：脚本运行但游戏内容不变，或文件出现在意外目录。

**检查**：

- 打印命令行当前目录；相对路径按执行时目录解析，不一定按脚本位置解析。
- 解析 `..\..\<模组>\Assets` 的绝对路径。
- 检查带空格的目标是否被正确引用。
- 对 `Streak/installpatch.bat` 特别核对目标 `Streak2` 是否确属预期。
- 比较源和目标 DLL SHA-256。

**恢复**：关闭游戏，保留错误目标用于审计，恢复正确目标的部署前备份；改用明确绝对路径逐目录复制。

**验证**：目标 DLL 哈希等于计划产物，目标 XML/Python 文件时间和内容与源一致，最小测试局通过。

## 覆盖后出现陈旧或混合行为

**现象**：已经删除或改名的功能仍出现，不同机器行为不一致。

**原因候选**：`xcopy /s /e` 只新增和覆盖，不删除目标旧文件；目标可能经历过多次不同覆盖。

**检查**：把目标目录文件清单与“完整 FFH2 Patch o 基线 + 当前 Rampage 覆盖层”比较，不只检查修改过的文件。

**恢复**：从完整 FFH2 Patch o 重新建立一个全新的 staging `Rampage`，应用一次当前覆盖层并验证；验证通过后再替换正式目标，保留旧目标备份。

**验证**：全新 staging 与正式目标文件清单一致，游戏行为一致。

## BtS 或 FFH2 基线无法启动

**现象**：进入 Rampage 前游戏已经崩溃、退出或无法新建游戏。

**检查**：分别启动未加载模组的 BtS 和未经 Rampage 覆盖的 FFH2 Patch o。确认问题发生在哪一层。

**恢复**：停止 Rampage 部署；修复或重装仓库外部的游戏/FFH2 基线。不要用 Rampage 文件覆盖一个本身不可运行的基线。

**验证**：BtS 和 FFH2 Patch o 各自能进入地图后，才重新建立 Rampage staging。

## XML 加载错误

**现象**：加载模组时出现 XML 错误、缺少 Info 类型或主菜单前退出。

**检查**：

- 对目标模组 XML 执行 well-formed 检查。
- 确认 Schema 和数据文件来自同一覆盖批次。
- 检查 XML 类型名、路径大小写和依赖文件是否由 FFH2 基线提供。
- 与仓库静态基线对比；四条代码线各自 `Assets/XML` 下共有 384 个游戏 XML（96 × 4）。Git 跟踪的大小写不敏感 `*.xml` 总数为 385，额外的 `Rampage/Assets/src/CvGameCoreDLL.041o/UpgradeLog.XML` 是构建升级日志而非游戏 XML；本次 385 个文件均通过 well-formed 检查。

**恢复**：关闭游戏，恢复部署前目标备份；在新 staging 上只重新应用 XML 覆盖并复验。

**验证**：XML 检查通过，游戏加载不再报告 XML 错误，并能进入最小测试局。

## Python 导入失败或界面缺失

**现象**：界面空白、按钮无响应、Python 异常或找不到模块。

**检查**：

- 确认目标不是只有仓库中的 40 个 Rampage Python 文件，而是基于完整 FFH2 Patch o。
- 核对 `CvEventInterface`、`CvPythonExtensions`、`PyHelpers`、`Popup`、`ScreenInput` 和基础界面模块的提供来源。
- 核对 `python/entrypoints`、`python/Screens` 与根 Python 搜索路径。
- 查看游戏实际 Python 日志；日志目录和开关取决于用户的 BtS 安装配置，仓库未固定。

**恢复**：恢复完整 FFH2 Python 基线，再应用 Rampage Python 覆盖；不要用现代系统 Python 执行这些 Python 2.4 游戏模块来替代游戏内验证。

**验证**：Python 日志无新的 import/traceback，主界面、财政界面和百科界面可以打开。

## 存档加载或单位回合中访问冲突

**现象**：特定存档在加载后或回合开始时崩溃，`PythonErr.log` 没有足以解释问题的 traceback，怀疑存档中存在无效单位。

**检查**：启用独立的存档诊断日志，搜索 `FFH2_SAVE_DIAG_BAD_UNIT`，先用 `owner + unit ID` 锁定对象，再用只读内存扫描确认类型和 `m_pUnitInfo`。完整配置、命令、安全限制和验证流程见[存档加载与坏单位诊断](./save-load-diagnostics.md)。

**恢复**：只在原存档副本和临时进程中操作。内存修复必须精确指定 `owner + unit ID`，删除坏对象后另存新文件，不能覆盖唯一原件。

**验证**：关闭诊断暂停，从全新进程加载新存档；确认诊断摘要 `badUnits=0`、Python 日志无异常且游戏能正常退出。本项目已记录的实例如[2026-07-25：回合 0243 无效单位导致读档崩溃](./incidents/2026-07-25-save-0243-invalid-unit.md)。

## DLL 无法加载或游戏启动即退出

**现象**：选择 Rampage 后立即退出，或行为像未加载自定义 DLL。

**检查**：

- 确认目标 DLL 是 PE32/x86，而不是 64 位产物。
- 计算目标 DLL SHA-256，确认没有复制到错误模组目录。
- 确认 DLL 位于目标 `Rampage/Assets/CvGameCoreDLL.dll`。
- 先用部署前 DLL验证同一基线，以区分 DLL 与 XML/Python 问题。
- 自编译 DLL需核对 VC7.1 ABI、Boost.Python 1.32、Python 2.4 和运行库依赖。

**恢复**：关闭游戏，移走失败 DLL，恢复带时间戳和已知哈希的上一个 DLL；若仍失败，恢复整个模组备份。

**验证**：恢复后能进入最小测试局；新 DLL 只在 staging 中继续排查。

## Visual Studio solution 找不到项目

**现象**：打开 `CvGameCoreDLL.sln` 提示缺少或无法加载 `CvGameCoreDLL.vcxproj`。

**原因**：solution 明确引用 `.vcxproj`，但仓库只包含 `.vcproj` 和 Makefile。

**处理**：不要凭空生成项目后假定配置等价；使用 Visual Studio 2008 Makefile `.vcproj` 或从适配的命令行环境直接执行 `nmake`。

**恢复**：该操作不应修改运行目录；若 IDE 自动转换文件，只保留在隔离构建副本中并丢弃未经审查的生成物。

**验证**：实际构建命令最终进入仓库 Makefile，且使用 Win32 Debug/Release 目标。

## 构建报告缺少 Boost、Python 或 Windows SDK

**现象**：找不到 Boost.Python、`Python.h`、Windows 头文件、`rc.exe` 或链接库。

**检查**：核对 Makefile 的 `TOOLKIT`、`PSDK`、`GLOBALBOOST`、`GLOBALPYTHON` 与项目局部 include/lib 路径；确认 `boost_python-vc71-mt-1_32.lib` 存在。

**处理**：在隔离 Windows 环境补齐与 VC7.1 ABI 匹配的旧依赖，不从当前仓库推断或自动下载替代版本。

**恢复**：失败构建不得部署；清理隔离 Debug/Release 输出或丢弃构建副本，保留上一个已验证 DLL。

**验证**：依赖路径全部可读，`cl.exe`、`link.exe`、`rc.exe`、`nmake` 版本已记录，构建退出码成功。

## 构建成功但游戏仍加载旧 DLL

**现象**：源码修改未反映到游戏，目标 DLL 时间或哈希不变。

**检查**：

- Makefile 的 `YOURMOD` 是否仍指向历史路径。
- 构建的是 Debug 还是 Release，部署的是哪个目录的产物。
- 游戏实际加载的模组目录是否为 Rampage。
- 构建产物、staging DLL 和正式目标 DLL 的 SHA-256 是否一致。

**恢复**：停止继续覆盖；恢复正式目标备份，在 staging 中重新明确构建和部署链路。

**验证**：三处 DLL 哈希一致，启动参数或游戏菜单确认加载 Rampage，目标功能与构建批次一致。

## Debug 启动到了 Streak 3

**现象**：从 IDE 启动后加载的不是 Rampage。

**原因**：历史 `.user` 文件包含 `CommandArguments="mod=\Streak 3"`、`E:\Civ4` 和远程主机 `ADRIAN-PCX`。

**处理**：在隔离的用户级调试配置中改为本机 BtS 路径和 Rampage；不要把历史 `.user` 当作共享运行契约。

**恢复**：用户级调试配置不应影响仓库或已部署文件；删除该隔离配置即可恢复。

**验证**：游戏界面确认加载 Rampage，目标 DLL 哈希与调试产物一致，调试器加载匹配 PDB。

## 预编译 DLL 行为与源码不一致

**现象**：静态阅读到的逻辑无法在预编译 DLL 行为中复现。

**检查**：记录 Git 源提交、DLL SHA-256、实际目标路径和加载模组。`49d4af0` 同时提交 DLL与部分源文件，但没有可重复构建证明。

**处理**：把同源性标记为 UNKNOWN；在受控旧工具链中重建并在 staging 验证，不以提交时间相同替代构建证明。

**恢复**：保留并可恢复上一个已验证预编译 DLL；自编译产物未通过 staging 前不得替换正式目标。

**验证**：构建清单、源提交、工具版本、DLL 哈希和运行测试结果形成同一批次记录。
