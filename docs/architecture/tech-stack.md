# 技术栈与执行环境边界

## 定位

本文件记录仓库所声明和所依赖的技术栈，不把旧工具链描述为重新选型，也不承诺仓库能在任意机器上独立构建或运行。系统边界和数据流见 [架构总览](overview.md)。

## 技术栈分层

| 层 | 技术/格式 | 架构职责 | 仓库证据 | 确定性 |
|---|---|---|---|---|
| 游戏宿主 | Sid Meier's Civilization IV: Beyond the Sword；Fall from Heaven 2 模组基线 | 装载 DLL、XML、Python、场景与资源，提供引擎生命周期、渲染和存档 | `*.CivBeyondSwordWBSave`、`CvGameCoreDLL` SDK 命名、场景 `ModPath`、安装目标 | 宿主类别为事实；精确版本未知 |
| 原生规则核心 | C++、Win32 x86 DLL | 战斗、移动、容量、AI、经济、XML 装载、Python 桥接 | `Rampage/Assets/src/CvGameCoreDLL.041o/*.cpp/*.h`；DLL 为 PE32 Intel 80386 | 事实 |
| C++/Python 桥接 | Boost.Python 1.32、Cy* 包装对象 | 将 C++ 类型、枚举与查询发布给嵌入式 Python，调用 Python 模块 | `Makefile:9-10,63-73`；`CvDLLPython.cpp:42-84`；`CvDLLPythonIFaceBase.h:13-45` | 事实 |
| 脚本运行时 | Python 2.4 构建依赖与 Civ4 嵌入式 Python | 游戏回调、事件分派、规则脚本和界面 | `Makefile` 的 `Python24` include/libs；Python 入口使用 Python 2 语法/API | 构建依赖为事实；宿主内精确补丁版本未知 |
| 配置/数据 | Civilization IV XML 与 Microsoft XML-Data Reduced 风格 Schema | 定义类型、数值、全局参数、回调开关、文本键、资源路径 | `Assets/XML/**/*.xml`；`xmlns="x-schema:..."`；`CvXMLLoadUtilitySet.cpp` | 事实 |
| UI | Civ4 Python Screens + GameCore 界面接口 | 主界面、顾问页、战斗日志、选择范围和用户命令入口 | `Assets/python/Screens`、`entrypoints/CvScreensInterface.py`、`CvGameInterface.cpp` | 事实 |
| 资源 | DDS、NIF、KFM/KF、TGA、文本 XML、音频/资源路径 | 单位模型、动画、按钮、字体、本地化与音效引用 | `Assets/Art`、`Assets/res`、`CIV4ArtDefines_*.xml`、Text XML | 事实；许多基础资源由外部安装提供是推断 |
| 构建 | Microsoft Visual C++ Toolkit 2003、Windows SDK、NMake 风格 Makefile | 编译 C++、链接 Win32 DLL、编译资源 | `Rampage/Assets/src/CvGameCoreDLL.041o/Makefile:5-20,53-73,79-121,143-175` | 声明为事实；可复现性未知 |
| IDE 元数据 | Visual Studio `.vcproj` 与 VS Express 14 `.sln` 元数据 | 辅助项目组织 | 仓库含 `.vcproj`；solution 第 6 行引用未跟踪 `.vcxproj` | 事实；权威性未知 |
| 安装 | Windows batch、`xcopy`、`copy` | 把覆盖资产放入既有模组目录 | 四个 `installpatch.bat` | 事实 |
| 数据库 | 无 | 不属于此系统架构 | 无 schema、迁移、数据库驱动或数据服务 | 事实 |

## 运行时组合

```text
Windows x86 游戏进程
  ├─ Civilization IV / Beyond the Sword 引擎
  ├─ 完整 FFH2/目标模组基线
  ├─ CvGameCoreDLL.dll
  │    ├─ C++ 规则与状态
  │    ├─ XML 装载
  │    └─ Boost.Python / Cy* 桥接
  ├─ XML Schema + XML 数据
  ├─ 嵌入式 Python 2.x
  │    ├─ CvGameInterface
  │    ├─ CvEventInterface / CvEventManager
  │    ├─ CvSpellInterface
  │    └─ CvScreensInterface / Screens
  └─ Art / res / Text / Audio / Scenarios
```

`CvGameCoreDLL.cpp:85-114` 的 `DllMain` 明确表明 DLL 被装入宿主进程；Makefile 的 `/DLL`、`/SUBSYSTEM:WINDOWS` 与四个 DLL 的 PE32 x86 文件类型共同限定 Windows 原生 ABI。这个组合没有远程服务或进程间协议。

## 构建链

```text
VC++ Toolkit 2003 ─┐
Windows SDK ───────┤
Boost 1.32 ────────┼─► C++ 编译/链接 ─► Debug/Release CvGameCoreDLL.dll
Python 2.4 headers ┤                              │
GameCore C++ 源码 ─┘                              └─► Mods/Rampage/Assets
```

Makefile 的关键契约：

- `TOOLKIT` 与 `PSDK` 分别指向 Microsoft Visual C++ Toolkit 2003 和 Windows SDK（第 6-7 行）。
- `CIVINSTALL` 是相对的 Civ4 安装根，Boost 1.32 与 Python24 默认从该根解析（第 8-10 行）。
- `YOURMOD` 指向 `Mods\Rampage`，Debug 与 Release 目标会复制新 DLL 到目标 `Assets`（第 12、113-121 行）。
- 编译目标定义 `WIN32`、`_WINDOWS`、`_USRDLL`，链接器生成 Windows DLL（第 53-61 行）。
- 库依赖包含 `boost_python-vc71-mt-1_32.lib`、Python24、`winmm.lib`、`user32.lib`（第 63-73 行）。
- Makefile 使用 NMake 条件与推导规则生成对象清单并链接 Debug/Release（第 79-99、143-169 行）。

### 构建元数据冲突

**事实：** `CvGameCoreDLL.sln:2-17` 标记为 Visual Studio Express 14 / Win32，并引用 `CvGameCoreDLL.vcxproj`；仓库同目录只有 `CvGameCoreDLL.vcproj`，没有 `.vcxproj`。

**推断：** Makefile 与 solution 代表不同年代或不同机器上的构建尝试，不能仅凭文件存在认定任何一条流程可复现。

**未知：** 预编译 DLL 的确切编译命令、依赖哈希、编译器补丁级别及其与仓库 C++ 源码的对应关系。

## 覆盖安装链

| 目录 | 安装脚本覆盖内容 | 脚本目标 | 架构含义 |
|---|---|---|---|
| `Fall from Heaven 2` | XML、Python、DLL | `..\..\Fall from Heaven 2\Assets` | 依赖已存在的同名完整模组目录 |
| `Streak` | XML、Python、DLL | `..\..\Streak2\Assets` | 源目录名与安装目标名不一致，目标必须单独核实 |
| `Streak 3` | XML、Python、Art、DLL | `..\..\Streak 3\Assets` | 仍是覆盖，不包含完整基础内容 |
| `Rampage` | XML、Python、Art、res、DLL | `..\..\Rampage\Assets` | 内容最宽，但仍不自包含 |

脚本使用相对路径且没有版本检查、清单校验或事务性回滚。安装成功只说明复制命令完成，不能证明游戏加载了目标目录、目标 DLL 与正确基线。

## XML 与 Python 技术边界

### XML 装载

`CvXMLLoadUtilitySet.cpp:172-229` 按固定路径装载 `GlobalDefines.xml`、`GlobalDefinesAlt.xml` 与 `PythonCallbackDefines.xml`，并支持模块化 define；`CvXMLLoadUtilitySet.cpp:776-835` 把多个 XML 信息类别装入全局上下文。

XML 的技术角色包括：

- Schema：字段存在性、类型和结构约束。
- 数据：单位、地形、改良、科技、文本、资源等声明。
- 标识：C++、Python、UI 和资源层共享的 Type、枚举顺序、文本键与路径。
- 回调配置：决定宿主是否调用某些 Python 钩子，或为法术/单位/地物提供脚本表达式。

XML 不是数据库；它是启动时装入内存的静态配置和资源索引。

### Python 入口

宿主和 DLL 通过固定模块名调用 Python：

- `CvGameInterface`：宿主规则回调门面；文件警告函数名由应用直接调用（`CvGameInterface.py:4-24`）。
- `CvEventInterface` / `CvEventManager`：事件入口与标签分派（`CvDefines.h:160-162`、`CvDllPythonEvents.cpp:14-26`、`CvEventManager.py:203-216`）。
- `CvSpellInterface`：执行 XML 信息对象提供的脚本表达式（`CvSpellInterface.py:19-65`）。
- `CvScreensInterface`：持有并调用 Python Screen 对象（`CvScreensInterface.py:69-105`）。

`CvGameInterface.py` 引用的 `CvGameInterfaceFile.py` 与 `CvEventInterface.py` 不在仓库中。该事实与覆盖安装脚本共同说明 Python 层依赖外部基线。

## 资源栈

`Rampage/Assets/Art` 包含 DDS、PDN、KF、NIF、KFM 和图像文件；`Assets/res/Fonts` 包含部分字体贴图。XML 通过相对路径引用资源，例如 `CIV4ArtDefines_Unit.xml:16114-16131` 的 Highlander 模型和动画。

资源边界有两类来源：

1. 覆盖包自带资源：由 `installpatch.bat` 复制。
2. 基线资源：定义中引用、但仓库不包含，依赖完整游戏/FFH2 安装。

例如 `CIV4ArtDefines_Interface.xml:373-391` 引用四个字体文件，而覆盖包只含 `GameFont.tga` 与 `GameFont_75.tga`，不含 `MonoSpacedConsoleFont.tga` 和 `NumberFont-Sylfaen64px.tga`。不能把“仓库缺失”直接判定为“目标安装缺失”，但必须在合并后的目标目录验证。

## 平台与验证边界

| 环境 | 可证明内容 | 不能仅凭该环境证明的内容 |
|---|---|---|
| 任意可读 Git 工作区 | 文件结构、Git 谱系、文本契约、XML 解析、静态引用、DLL 文件格式 | 宿主实际加载目录、DLL ABI 兼容、游戏规则行为 |
| 非 Windows 工作区 | 上述静态事实 | VC++ 2003 工具链可用、Windows 游戏启动、DLL 被加载 |
| Windows 构建环境 | 工具链解析、编译、链接、产物格式 | 目标游戏基线正确、场景/存档行为，除非进一步运行 |
| 完整 Windows 游戏环境 | 安装目标、模块/DLL 加载、界面与规则行为 | 源码与 DLL 对应关系，除非同时记录构建来源和哈希 |

因此，静态检查、构建验证和游戏运行验收是三层不同证据，不能互相替代。

## 技术约束与维护规则

1. **ABI 固定。** DLL 必须匹配 Win32 游戏宿主与其期望的导出/接口；不能把重新编译成功等同于可装载。
2. **Python ABI 固定。** Boost.Python、编译器运行库、Python headers/libs 与宿主嵌入式解释器必须兼容。
3. **名称契约固定。** XML Type、枚举、Python 模块/函数名、文本键与资源路径都属于兼容面。
4. **覆盖顺序有语义。** 目标目录中的最终文件集合由基础安装和覆盖包共同决定；验证必须针对合并结果。
5. **源码与 DLL 成对。** 规则变更的交付单位同时包含来源明确的 C++ 和其 DLL；仓库历史中存在只替换 DLL 的提交，不能默认二者同步。
6. **没有数据库迁移层。** XML 结构变化走 XML/C++/Python 兼容验证，不套用关系数据库 schema 或迁移流程。
7. **不引入虚构现代化路径。** 仓库证据只支持遗留 Civ4 模组技术栈；任何升级编译器、替换 Python 或重新打包的方案都需要独立需求、兼容性研究和决策。

## 技术未知项

- Civ4 BTS、FFH2 Patch o 与外部基础文件的精确版本和获取来源。
- VC++ Toolkit 2003、Windows SDK、Boost 1.32、Python24 的完整目录内容和哈希。
- Makefile、`.vcproj`、缺失的 `.vcxproj` 中哪一个对应分发 DLL。
- `CvGameCoreDLL.dll` 的导出集合与目标宿主期望集合是否完全一致。
- 游戏加载时的 XML 缓存是否会掩盖覆盖内容，及清理缓存的具体操作约束。
- 用户机器的实际模组路径、实际加载 DLL 和基础资产集合。
- `Rampage` 场景仍指向 `Fall from Heaven 2` 的意图与兼容范围。
