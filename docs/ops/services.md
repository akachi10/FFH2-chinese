# 服务生命周期

本项目没有常驻后端服务。“服务”指三个可操作生命周期：游戏加载、模组部署和 DLL 构建。它们的依赖顺序是：

环境前提与依赖清单见[环境配置](./environments.md)；执行前先看[环境状态](./status.md)，失败后转到[故障排查](./troubleshooting.md)。

`Civ4/BtS 可运行 → FFH2 Patch o 基线可运行 → Rampage 覆盖部署 → Rampage 游戏加载 → 可选 DLL 构建与替换`

任何文件变更前都必须退出游戏并确认 `Civ4BeyondSword.exe` 不在运行。安全回退使用目标目录的时间戳备份，不使用 Git 回退命令。

## 游戏加载服务

### 启动前检查

1. 确认 Windows 上 Civ4 和 BtS 能独立进入主菜单。
2. 确认完整 `Fall from Heaven 2` Patch o 能独立加载并开始新游戏。
3. 确认 BtS `Mods` 目录中存在独立的 `Rampage` 目录，且至少包含完整基线和覆盖后的 `Assets`。
4. 确认 `Rampage/Assets/CvGameCoreDLL.dll` 在目标机器上识别为 32 位 DLL。
5. 确认最近一次部署有可恢复的目标目录备份。

验证：每项检查都应记录实际绝对路径；FFH2 基线未通过时停止，不进入 Rampage 排查。

安全回退：启动前检查不修改文件；若发现目标目录异常，关闭游戏后恢复部署前备份。

### 启动

1. 优先从 BtS 的“高级 → 加载模组”选择 `Rampage`，避免沿用仓库中的历史用户工程参数。
2. 等待游戏重启并确认加载的模组名为 Rampage。
3. 进入主菜单后新建最小测试局。
4. 验证界面能读取 XML/Python，并验证至少一个 Rampage 可观察功能，例如玩家食物显示。

验证：主菜单、地图加载、Python 界面和 DLL 驱动功能都成功后，游戏加载服务才算可用。只到主菜单不能证明 DLL/XML/Python 契约完整。

安全回退：若启动失败，退出游戏，把失败目标目录改名保留现场，再将部署前备份恢复为 `Rampage`；先复验 FFH2 基线，再定位覆盖层。

### 停止

1. 保存到专用测试存档或放弃测试局。
2. 正常退出到桌面。
3. 在任务管理器确认 `Civ4BeyondSword.exe` 已结束。
4. 只有确认进程结束后才能替换 DLL、XML、Python、Art 或 res。

验证：游戏进程不存在，目标 DLL 可以被读取且不再被占用。

安全回退：正常停止不修改部署内容；强制结束进程只用于无响应测试实例，之后应把该次存档视为不可信。

## 模组部署服务

### 首次建立 Rampage 目标

1. 关闭游戏并记录 BtS `Mods` 的绝对路径。
2. 验证 BtS `Mods` 中外部已安装的 `Fall from Heaven 2` 是完整、可启动的 Patch o 基线。
3. 若目标 `Rampage` 已存在，将整个目录重命名为 `Rampage.backup-YYYYMMDD-HHMM`，不要覆盖该备份。
4. 完整复制该外部已安装基线为新的 `Rampage` 目录。
5. 分别把仓库 `Rampage/Assets/XML`、`python`、`Art`、`res` 合并到目标同名目录。
6. 单独复制仓库 `Rampage/Assets/CvGameCoreDLL.dll` 到目标 `Assets`。
7. 不需要把 `Assets/src` 复制到运行目录；源码不参与游戏加载。

验证：目标仍保留完整 FFH2 基线文件，覆盖目录存在，目标 DLL 的 SHA-256 与准备部署的 DLL 一致。随后按“游戏加载服务”执行最小测试局。

安全回退：删除或改名失败的目标 `Rampage`，把 `Rampage.backup-YYYYMMDD-HHMM` 恢复为原名。不要用仓库版本控制命令处理游戏安装目录。

### 更新现有 Rampage 目标

1. 关闭游戏并确认进程结束。
2. 将整个目标 `Rampage` 复制或重命名为新的时间戳备份。
3. 生成待覆盖文件清单，确认来源只属于本次批准的 XML、Python、Art、res 和 DLL。
4. 使用明确的绝对源路径和绝对目标路径执行合并复制。
5. 不使用镜像删除选项；旧文件清理由单独审查后的干净重建完成。
6. 对 DLL 和关键变更文件记录部署前后 SHA-256。

验证：复制工具无失败记录；目标文件哈希与源一致；XML 静态检查通过；最小测试局通过。

安全回退：关闭游戏，保留失败目标用于诊断，将本次部署前的完整备份恢复。不得在未知目标上反向运行 `xcopy`。

### 旧 `installpatch.bat` 的使用边界

四个脚本是历史覆盖捷径，不是安全部署器。使用前必须先在命令行打印并人工确认当前目录以及解析后的绝对目标；带空格路径必须正确引用；`Streak/installpatch.bat` 的 `Streak2` 目标必须视为疑点。

验证：脚本返回后逐个核对目标目录和 DLL 哈希，不能只依据命令窗口无报错判断成功。

安全回退：脚本没有内建回退；只能关闭游戏并恢复执行前的完整目标备份。没有备份时不得执行。

## DLL 构建服务

### 准备

1. 在隔离的 Windows 32 位构建环境准备 VC++ Toolkit 2003、Windows SDK、Boost 1.32、Python 2.4 开发文件和 `nmake`。
2. 进入 `Rampage/Assets/src/CvGameCoreDLL.041o`。
3. 按实际绝对路径校准 Makefile 的 `TOOLKIT`、`PSDK`、`CIVINSTALL`、`GLOBALBOOST` 和 `GLOBALPYTHON`。
4. 将 `YOURMOD` 指向一次性 staging 模组，而不是已验证的游戏目标；Makefile 的 Debug/Release 目标会自动复制 DLL。
5. 检查 `boost_python-vc71-mt-1_32.lib`、Python 2.4 include/libs、Windows SDK include/libs 和资源编译器均存在。

验证：`cl.exe`、`link.exe`、`rc.exe`、`nmake` 能执行并记录版本；所有 include/lib 路径都解析到文件；staging 目标不是正式 Rampage 目录。

安全回退：准备阶段只修改隔离构建环境或其 Makefile 副本；失败时丢弃该隔离副本，不触碰已部署模组。

### 构建 Debug

1. 在源码目录执行 `nmake /NOLOGO Debug_clean`。
2. 执行 `nmake /NOLOGO Debug`，保存完整输出和退出码。
3. 检查 `Debug/CvGameCoreDLL.dll`、`Debug/CvGameCoreDLL.pdb` 和导入库。
4. 记录 DLL SHA-256、源提交和工具版本。

验证：退出码成功、没有 `unfinished.@` 标记、DLL 为 Win32/x86、PDB 与本次构建同时产生。Makefile 中 Visual Studio 项目使用的 `/K` 会继续处理其他目标，不能以“最后仍有输出”代替错误检查。

安全回退：Debug 构建只写 Debug 与 staging；失败后保留日志，重新清理 Debug 输出或丢弃隔离副本，不替换正式 DLL。

### 构建 Release

1. 执行 `nmake /NOLOGO Release_clean`。
2. 执行 `nmake /NOLOGO Release`，保存完整输出和退出码。
3. 检查 `Release/CvGameCoreDLL.dll` 和相关链接产物。
4. 在隔离的 staging Rampage 上完成启动与最小测试局。

验证：退出码成功、DLL 为 Win32/x86、staging 能完成游戏加载验证，并记录 SHA-256 和构建清单。

安全回退：Release 未通过 staging 验证时不得进入正式部署；保留上一个已验证 DLL 和完整模组备份。

### 部署新 DLL

1. 关闭游戏并确认进程结束。
2. 备份目标 `Assets/CvGameCoreDLL.dll`，文件名包含时间戳和原 SHA-256。
3. 把 staging 已验证的 DLL 复制到目标 `Rampage/Assets`。
4. 复核目标 SHA-256。
5. 执行最小测试局；Debug 调试时同时保留匹配 PDB，但不要把历史 `.user` 中的 `Streak 3` 参数当作 Rampage 配置。

验证：目标哈希等于 staging 产物，游戏能加载并表现出对应功能。

安全回退：关闭游戏，移走失败 DLL，恢复时间戳备份并复核原 SHA-256；不使用 Git 回退游戏目录。
