# 环境配置

## 项目边界

本仓库是 Civilization IV: Beyond the Sword 上的 Fall from Heaven 2 派生模组覆盖包，不是完整、自包含的游戏发行物。运行时必须由仓库外部提供 Civ4、Beyond the Sword、完整的 Fall from Heaven 2 Patch o 基线及其 Python/资源文件。

`Rampage` 是重点维护代码线；`Fall from Heaven 2`、`Streak`、`Streak 3` 用于基线和历史谱系比对。仓库内容不能证明用户机器实际加载的是其中哪个模组。

## 阅读路径

- 先读本文，确认受支持环境、外部依赖和静态/运行证据边界。
- 需要知道本次工作区能做什么，读[环境状态](./status.md)。
- 需要部署、加载、构建或恢复操作，读[服务生命周期](./services.md)。
- 已经出现故障时，按[故障排查](./troubleshooting.md)逐层定位。
- 需要理解同进程 DLL/XML/Python/资源关系，转到[系统架构总览](../architecture/overview.md)和[技术栈](../architecture/tech-stack.md)。

## 环境矩阵

| 环境 | 用途 | 必需能力 | 本仓库能否独立提供 |
|---|---|---|---|
| macOS 静态检查 | 阅读源码、比较资源、解析 XML、检查 PE 文件和 Git 历史 | Git、文本检索、XML 解析器、PE 文件识别 | 可以 |
| Windows 游戏运行 | 加载 BtS、FFH2 Patch o 和 Rampage 覆盖层 | x86 兼容的 Windows 游戏环境、Civ4、BtS、完整 FFH2 Patch o | 不可以 |
| Windows DLL 构建 | 重建 32 位 `CvGameCoreDLL.dll` | VC++ Toolkit 2003、Windows SDK、Boost 1.32、Python 2.4 开发文件、`nmake` | 不可以 |
| Windows DLL 调试 | 加载 Debug DLL、PDB 并附加原生调试器 | 完整运行环境、匹配的 Debug DLL/PDB、32 位原生调试器 | 不可以 |

本项目没有数据库、网络服务端口或项目环境变量；不得套用 Web 服务、数据库迁移或云部署模板。

## Windows 运行基线

运行环境应按以下顺序准备：

1. 安装并验证 Civilization IV。
2. 安装并验证 Beyond the Sword。
3. 在 BtS 的 `Mods` 目录安装完整的 `Fall from Heaven 2` Patch o，并先单独启动验证。
4. 从该完整基线创建独立的 `Rampage` 模组目录。
5. 最后把本仓库 `Rampage/Assets` 中指定的覆盖内容合并到目标 `Rampage/Assets`。

Patch o 的目标版本属于运行契约；仓库中的源码目录名 `Rampage/Assets/src/CvGameCoreDLL.041o` 提供版本线索，但仓库没有 FFH2 安装器，不能据此重建完整基线。

基线验证至少包括：BtS 能进入主菜单、FFH2 Patch o 能单独加载、新建一局能进入地图。任一步失败时不得继续覆盖 Rampage。

## Windows 32 位构建工具链

`Rampage/Assets/src/CvGameCoreDLL.041o/Makefile:5-20` 声明以下外部依赖：

| 依赖 | Makefile 期望 | 用途 | 仓库状态 |
|---|---|---|---|
| Microsoft Visual C++ Toolkit 2003 | `C:\Dev\Microsoft Visual C++ Toolkit 2003` | `cl.exe`、`link.exe` 和 VC7.1 ABI | 未包含 |
| Windows SDK | `C:\Dev\WindowsSDK` | 头文件、库和 `rc.exe` | 未包含 |
| Boost | `Boost-1.32.0` | Boost.Python 头文件和 `boost_python-vc71-mt-1_32.lib` | 未包含 |
| Python | `Python24` | Python 2.4 头文件和链接库 | 未包含 |
| NMake | Visual C++ 工具链提供 | 执行 Makefile | 未包含 |
| fastdep | `$(MAKEDIR)\bin\fastdep.exe` | 生成 C++ 依赖关系 | 源码树包含 `bin/fastdep.exe`，未在 Windows 验证 |

构建目标固定为 Win32 DLL；Debug 使用 `/MD /Zi /Od /D_DEBUG /RTC1` 并产生 PDB，Release 使用 `/MD /O2 /DNDEBUG /DFINAL_RELEASE`。这些编译器、ABI、Boost.Python 和 Python 版本是一组整体约束，不应只替换其中一项后假定二进制兼容。

## 构建工程入口

- `CvGameCoreDLL.vcproj` 是 Visual Studio 2008 格式的 Makefile 项目，Debug/Release 实际调用 `nmake`。
- `CvGameCoreDLL.sln` 是 Visual Studio 2015 格式，但引用仓库中不存在的 `CvGameCoreDLL.vcxproj`，不能视为可用构建入口。
- `Makefile` 是可见的实际构建契约；其中 `TOOLKIT`、`PSDK`、`CIVINSTALL`、`GLOBALBOOST`、`GLOBALPYTHON` 和 `YOURMOD` 都带历史目录假设。
- `CvGameCoreDLL.vcproj.Adrian-PCX.Adrian.user` 包含历史机器 `E:\Civ4`、远程主机和 `mod=\Streak 3`，不能直接用于 Rampage。

## 覆盖包与 Python 基线依赖

Rampage 覆盖层包含 `XML`、`python`、`Art`、`res`、预编译 DLL 和 C++ 源码，但不包含游戏可执行文件、完整 FFH2 资源或全部 Python 模块。

仓库内存在 `CvGameInterface.py`、`CvScreensInterface.py`、`CvRandomEventInterface.py`、`CvEventManager.py` 等覆盖入口；静态导入扫描同时发现 `CvEventInterface`、`CvPythonExtensions`、`PyHelpers`、`Popup`、`ScreenInput` 及多个基础游戏界面模块未在 Rampage 目录中提供。它们必须由 BtS/FFH2 基线或游戏嵌入式 Python 2.4 环境提供。

因此不能把 `Rampage` 目录复制到空白位置后认定安装完整；正确语义是“完整 FFH2 Patch o 基线 + Rampage 覆盖层”。

## 目录与安装脚本假设

四个 `installpatch.bat` 都以执行时当前目录为基准，从本地 `Assets` 覆盖到 `..\..\<模组>\Assets`。脚本本身没有切换到脚本所在目录，也没有创建备份或验证目标。

| 脚本 | 覆盖内容 | 目标假设 | 已知风险 |
|---|---|---|---|
| `Fall from Heaven 2/installpatch.bat` | XML、Python、DLL | `..\..\Fall from Heaven 2` | 带空格目标未加引号 |
| `Rampage/installpatch.bat` | XML、Python、Art、res、DLL | `..\..\Rampage` | 强依赖当前目录和两级相对位置 |
| `Streak/installpatch.bat` | XML、Python、DLL | `..\..\Streak2` | 源目录名与目标名不一致 |
| `Streak 3/installpatch.bat` | XML、Python、Art、DLL | `..\..\Streak 3` | 强依赖当前目录和两级相对位置 |

这些脚本使用 `xcopy /s /e` 和 `copy`，只覆盖或新增文件，不删除目标中的陈旧文件。运行前必须明确解析源、目标绝对路径，并先备份整个目标模组目录；默认推荐按明确绝对路径手动部署，而不是直接双击脚本。

## DLL 产物与同源性

`Rampage/Assets/CvGameCoreDLL.dll` 是 32 位 Windows PE DLL，SHA-256 为 `4e47e8769a0ddbb577d125cdff96aea4f550902f1c59039d6d0cdbdd6992005d`。

Git 提交 `49d4af0` 同时修改了该 DLL、`CvPlayer.cpp` 和相关 XML，这只能证明它们被一同提交。仓库没有构建日志、工具链快照、产物清单或可重复构建记录，因此预编译 DLL 与当前全部源码的精确同源性仍为未知。

后续构建必须记录：源提交、工具链版本、Debug/Release 配置、构建输出 SHA-256、PDB 是否匹配，以及实际部署目标。

## macOS 静态检查边界

macOS 可以执行文本检索、文件存在性检查、SHA-256、PE 类型识别和 XML well-formed 检查。macOS 不能据此证明：

- Windows VC7.1 工具链可以成功编译；
- DLL 可以被 BtS 加载；
- FFH2 基线 Python 模块完整；
- 游戏实际加载了 Rampage 而不是其他模组；
- 预编译 DLL 与源码运行行为一致。

这些结论只能在隔离的 Windows 游戏/构建环境中验证。
