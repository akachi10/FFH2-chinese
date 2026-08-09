# 环境状态

环境能力边界见[环境配置](./environments.md)；本文件只记录本次只读检查结果。

> 最后更新：2026-07-15 02:07 PDT（UTC-07:00）  
> 更新者：devops agent  
> 检查模式：macOS 只读静态检查

## 当前环境

| 项目 | 状态 | 证据或说明 |
|---|---|---|
| 操作系统 | PASS | macOS 26.5.2，Darwin arm64 |
| Git/文本静态检查 | PASS | 仓库和源码可读取 |
| XML 解析器 | PASS | `/usr/bin/xmllint` 可用 |
| Windows 游戏运行 | NOT VERIFIED | 未在 macOS 启动 Civ4/BtS |
| Windows DLL 构建 | BLOCKED | 当前环境没有 `nmake`、`cl.exe`、VC++ Toolkit 2003、Windows SDK、Boost 1.32 或 Python 2.4 开发文件 |

## 服务状态

| 服务 | 状态 | 端口 | 说明 |
|---|---|---|---|
| 仓库静态检查 | Available | - | 可执行路径、哈希、文本和 XML 检查 |
| 游戏加载 | NOT VERIFIED | - | 未知用户机器是否安装 Civ4/BtS、FFH2 Patch o 或实际加载 Rampage |
| 模组部署 | NOT RUN | - | 四个 `installpatch.bat` 均未执行，未触碰游戏安装目录 |
| DLL Debug 构建 | BLOCKED | - | 旧 Windows 32 位工具链和依赖缺失 |
| DLL Release 构建 | BLOCKED | - | 旧 Windows 32 位工具链和依赖缺失 |

## 静态验证结果

| 检查 | 结果 | 详情 |
|---|---|---|
| 四条代码线游戏 XML well-formed | PASS | 仅统计各代码线 `Assets/XML` 下的游戏 XML：每条代码线 96 个，共 384 个 |
| Git 跟踪 XML 总清单（扩展名大小写不敏感） | PASS | 共 385 个；除上述 384 个游戏 XML 外，额外文件是构建升级日志 `Rampage/Assets/src/CvGameCoreDLL.041o/UpgradeLog.XML`；本次 385 个文件均通过 `xmllint --noout` |
| Rampage 预编译 DLL 存在 | PASS | `Rampage/Assets/CvGameCoreDLL.dll`，5,337,088 字节 |
| Rampage DLL 架构 | PASS | PE32 DLL，Intel 80386，Windows GUI 子系统 |
| Rampage DLL SHA-256 | PASS | `4e47e8769a0ddbb577d125cdff96aea4f550902f1c59039d6d0cdbdd6992005d` |
| Makefile 静态检查 | PASS | 能定位 Win32 Debug/Release 目标、外部依赖和自动复制步骤 |
| `.vcproj` 静态检查 | PASS | Visual Studio 2008 Makefile 项目，调用 `nmake` |
| `.sln` 完整性 | FAIL | 引用不存在的 `CvGameCoreDLL.vcxproj` |
| 本地 Boost/Python 开发目录 | FAIL | `Boost-1.32.0` 与 `Python24` 未包含在 Rampage 源码目录或仓库其他位置 |
| Python 覆盖入口 | PARTIAL | 40 个本地 `.py`；多个导入模块只可能由 BtS/FFH2/嵌入式 Python 提供 |

## DLL 来源状态

Git 提交 `49d4af0` 同时更新了 Rampage DLL、`CvPlayer.cpp` 和 XML。没有构建日志、工具链快照或可重复构建证明，故“预编译 DLL 与当前全部源码精确同源”状态为 UNKNOWN。

## 已知问题

- `CvGameCoreDLL.sln` 不能直接打开当前仓库中的目标项目，因为 `.vcxproj` 缺失。
- Makefile 包含历史绝对目录假设，且 Debug/Release 会复制 DLL 到 `YOURMOD`。
- `CvGameCoreDLL.vcproj.Adrian-PCX.Adrian.user` 指向历史 `E:\Civ4`、`ADRIAN-PCX` 和 `mod=\Streak 3`，不适用于 Rampage。
- 四个 `installpatch.bat` 无备份和目标验证；Fall from Heaven 2 路径未引用，Streak 目标写为 `Streak2`。
- 覆盖复制不会删除目标陈旧文件。
- 仓库没有完整 Civ4/BtS/FFH2 运行基线，Python 导入闭包不能在当前环境验证。

## 测试可用性

- [x] C++、Python、XML 和构建文件可静态阅读
- [x] 四条代码线 XML 可做 well-formed 检查
- [x] DLL 可做存在性、SHA-256 和 PE32 架构检查
- [ ] Windows VC7.1 DLL 可构建
- [ ] FFH2 Patch o 基线可启动
- [ ] Rampage 覆盖部署可执行
- [ ] Rampage 主菜单和最小测试局可运行
- [ ] 预编译 DLL 与源码行为同源可证明

当前 tester 只能执行静态验证；任何游戏运行、部署、DLL 加载或构建验收都需要隔离的 Windows 环境。
