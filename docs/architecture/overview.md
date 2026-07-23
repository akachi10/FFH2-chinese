# 系统架构总览

## 文档目的与证据规则

本文定义 `ffh2-mods-ba` 仓库的架构边界、内容谱系、运行时组件、跨层数据流和约束。后续分析以 `Rampage` 为主要代码线，同时保留 `Fall from Heaven 2`、`Streak`、`Streak 3` 的历史语义。

结论按以下标签区分：

- **事实**：能直接定位到仓库文件、构建文件或 Git 历史。
- **推断**：由多项事实共同支持，但仓库没有直接声明。
- **未知**：必须通过用户机器、完整游戏安装或运行测试才能确认。

## 一页总览：项目分为七部分

| 部分 | 一句话职责 |
|---|---|
| 1. 外部游戏宿主与 FFH2 基线 | 启动游戏进程，并提供仓库没有携带的引擎、基础 Python 模块和基础资源 |
| 2. XML Schema 与 XML 数据 | 定义单位、地形、改良、经济、回调、文本和资源引用的类型化配置 |
| 3. C++ GameCore DLL | 持有权威游戏状态，执行战斗、移动、容量、工人收益、玩家食物和 AI 规则 |
| 4. C++/Python 桥接与 Python 入口 | 把 C++ 对象发布给 Python，并让宿主/DLL 按固定模块名调用规则与事件入口 |
| 5. Python UI 与反馈 | 在原生 HUD、单位面板、预览、日志、财务顾问和百科中解释规则结果 |
| 6. Art、res 与 Text 资源 | 为 XML/Python 引用提供模型、动画、贴图、字体、音效和本地化 |
| 7. 构建与覆盖安装 | 用旧 Win32 工具链生成 DLL，并把 DLL、XML、Python 和资源覆盖到既有模组目录 |

七部分在同一个游戏运行时中协作，不是七个独立服务。先读下方的组件图和数据流理解它们如何连接；工具和平台细节下钻到 [技术栈](tech-stack.md)，为什么以 Rampage 为重点下钻到 [ADR-0001](decisions/0001-rampage-focus.md)，为什么七部分必须联合验证下钻到 [ADR-0002](decisions/0002-cross-layer-consistency.md)。产品目标与交互分别见 [产品定义](../product/product-definition.md)、[PRD](../product/PRD.md) 和 [UE 交互规格](../product/UE-spec.md)。

产品契约把 `Rampage/` 定义为产品规则与内容的权威代码线，并把 `Mods\Rampage` 定义为目标目录；这是“系统应该是什么”的规范。仓库取证无法证明任一用户机器已经按该规范加载，因此运行诊断仍需独立确认模组目录和 DLL 身份。

这里的“外部 FFH2 基线”指用户环境中完整的基础安装，不表示运行时要把仓库顶层 `Fall from Heaven 2/`、`Streak/`、`Streak 3/` 与 `Rampage/` 混合复制。按照产品契约，前三个仓库目录只用于谱系对照。

## 架构结论

1. **事实：仓库是覆盖包，不是独立发行物。** 四个 `installpatch.bat` 都把仓库中的部分 `Assets` 内容复制到上两级的既有模组目录；`Rampage/installpatch.bat:1-5` 只覆盖 XML、Python、Art、res 和 DLL。仓库中的 Python 入口还引用未纳入版本库的基础模块，部分资源定义也指向未纳入版本库的文件。
2. **事实：运行核心是同一 Windows 进程内的原生 DLL、XML 数据、嵌入式 Python 与资源。** `CvGameCoreDLL.dll` 是 PE32 x86 Windows DLL；C++ 负责规则和 Python 桥接，XML 提供类型化配置，Python 提供回调、事件和界面，Art/res 提供这些定义引用的资源。
3. **事实：项目没有关系数据库。** 仓库中没有数据库 schema、迁移、数据库驱动或持久化服务；游戏状态由宿主游戏进程、存档及引擎数据结构承担。因此架构边界不包含数据库，也不建立 `docs/database/`。
4. **事实：跨层名称与枚举构成一份共同契约。** XML Schema 的字段名、XML 数据、C++ 读取字段、Python 暴露枚举/对象、入口模块名、文本键和资源路径必须匹配。
5. **推断：`Rampage` 是仓库中最后演化且最适合继续理解的代码线。** 它拥有完整 C++ 源码、XML、Python、定制资源和最晚的路径提交；该结论不证明用户机器加载的模组目录或 DLL。

本文所称“基于回合起点的 `plotDistance` 移动半径/边界”采用 `CvGameCoreUtils.h:144-152` 的离散地图度量：令考虑地图包裹设置后的坐标差为 `dx`、`dy`，则 `plotDistance = max(dx,dy) + floor(min(dx,dy)/2)`。距离不大于给定半径的地块集合在方格地图上呈离散的近似八边形，具有非欧氏圆语义；后文统一使用 `plotDistance` 移动半径/边界描述该规则。

产品功能与架构承载关系：

| 产品功能 | 主要架构承载 |
|---|---|
| F001 外部依赖与元素氏族入口 | 外部宿主/FFH2 基线、Rampage 覆盖目录、XML 文明定义与完整跨层包 |
| F002 多属性多掷骰近战 | Unit XML/Schema、CvInfos、CvUnit、事件桥接、战斗预览与日志 |
| F003 最小/最大距离远程打击 | Unit/Interface XML、CvUnit、选择范围/任务入口、战斗日志 |
| F004 基于回合起点的 `plotDistance` 移动半径与地块容量 | Unit/Terrain/Feature/Improvement/Global Defines、CvUnit、CvPlot、CvCity |
| F005 工人占格生产 | Build/Unit/Improvement/Commerce XML、CvUnit/CvPlot/CvPlayer、HUD/财务顾问 |
| F006 玩家级食物经济 | Commerce/Text XML、CvPlayer、CyPlayer、HUD/财务顾问 |
| F007 原生信息与反馈闭环 | GameTextMgr、Python Screens、事件日志、百科与资源字体 |

## 内容谱系

这里的“谱系”表示仓库内容的演化关系，不表示四个目录是 Git 分支，也不表示任何一个目录处于用户机器的运行态。

| 代码线 | 仓库角色 | 直接证据 | 结论类型 |
|---|---|---|---|
| `Fall from Heaven 2` | FFH2 Patch o 基线及早期 SDK 修改来源 | `5b397cd` 的提交说明为 “FFH2 Patch o. No modifications.”；目录包含 XML、Python、DLL 与 C++ 源码 | 事实 |
| `Streak` | 从 FFH2 内容起步的第一条定制线 | `0786ba6` 添加目录；该提交中抽样的 `CIV4UnitInfos.xml` 与 `CvEventManager.py` 对象哈希分别与 FFH2 相同 | 事实；“从基线起步”是推断 |
| `Streak 3` | 组合并继续演化 Streak 与 FFH2 内容的中间线 | `bc6bf41` 添加目录；该提交中单位 XML 与 FFH2 相同，而 DLL 与 Streak 相同；目录增加部分 Art | 事实；“组合快照”是推断 |
| `Rampage` | 从 Streak 3 快照继续演化、并带完整 SDK 源码的重点线 | `4c9a642` 添加目录；添加时抽样的单位 XML、事件管理器与 DLL 和 Streak 3 相同，`CvUnit.cpp` 与 FFH2 相同；路径最后提交为 `49d4af0`（2016-01-26） | 事实；“继承后继续演化”是推断 |

关键 Git 锚点：

- `5b397cd`（2014-06-21）：FFH2 Patch o 基线。
- `0786ba6`（2014-10-15）：加入 `Streak`。
- `bc6bf41`（2014-10-18）：加入 `Streak 3`。
- `4c9a642`（2015-08-12）：加入 `Rampage`。
- `49d4af0`（2016-01-26）：`Rampage` 路径的最后提交，继续扩展玩家食物机制。

各路径最后提交也构成重点选择证据：`Fall from Heaven 2` 与 `Streak 3` 止于 `406849f`（2015-06-17），`Streak` 止于 `d41e7c3`（2015-01-09），`Rampage` 止于 `49d4af0`（2016-01-26）。

## 系统上下文与组件图

```text
┌───────────────────────────────────────────────────────────────────┐
│ 外部宿主：Civilization IV / Beyond the Sword + FFH2 完整安装       │
│ 提供可执行程序、引擎接口、嵌入式 Python、基础脚本与未覆盖资源       │
└──────────────────────────────┬────────────────────────────────────┘
                               │ 加载同进程模组内容
              ┌────────────────▼────────────────┐
              │ XML Schema + XML 数据/定义       │
              │ 类型、数值、回调开关、文本/资源键 │
              └─────────┬─────────────────┬──────┘
                        │ 解析为信息对象     │ 名称/路径引用
              ┌─────────▼──────────┐      ┌▼──────────────────┐
              │ CvGameCoreDLL.dll   │      │ Art / res / Text   │
              │ C++ 规则、状态、AI、 │      │ 模型、贴图、字体、  │
              │ 战斗、移动、经济     │      │ 音频与本地化资源     │
              └──────┬────────┬─────┘      └─────────┬─────────┘
                     │        │ Boost.Python/Cy*      │
               事件/回调      ▼                       │
                     │  ┌───────────────────────┐     │
                     └─►│ Python 入口与脚本层     │◄────┘
                        │ Game/Event/Spell/Screens│
                        └───────────┬───────────┘
                                    │ 界面命令、日志、顾问页
                              ┌─────▼─────┐
                              │ 游戏 UI    │
                              └───────────┘
```

这不是客户端—服务器架构。DLL 与 Python 都由外部游戏宿主装载并在同一运行时内交互；仓库没有独立后端、网络协议或数据库。

## 模块边界

| 边界 | 责任 | 输入 | 输出 | 不承担 |
|---|---|---|---|---|
| 外部宿主与基础模组 | 启动进程、提供引擎 ABI、嵌入式 Python、基础资产和基础脚本 | 覆盖后的模组目录 | 引擎生命周期、渲染、存档与脚本运行环境 | 仓库不能替代的完整发行内容 |
| XML Schema 与数据 | 约束字段结构，声明单位、地形、改良、全局参数、文本键、回调开关和资源引用 | XML 文件 | C++ 信息对象、Python 可查询定义、资源标识 | 回合状态与规则执行 |
| 原生 GameCore DLL | 执行战斗、移动、容量、玩家经济、AI、XML 装载和 Python 桥接 | 引擎调用、XML 信息、Python 回调结果 | 游戏状态变化、Cy* 对象、事件、界面脏标记 | 独立进程服务与数据库持久化 |
| Python 入口与规则脚本 | 接收宿主或 DLL 调用，分派事件，执行 XML 指定的脚本回调 | Cy* 对象、事件参数、XML 回调字符串 | 规则返回值、事件处理、界面调用 | 替代 DLL 的底层状态所有权 |
| Python UI | 将 C++/XML 暴露的数据转换为主界面、顾问页、战斗日志与选区显示 | Cy* 查询、文本键、资源键 | 玩家可见界面 | 核心规则权威状态 |
| Art、res、Text | 满足 XML 与 UI 中的模型、贴图、字体和本地化引用 | 资源路径和文本键 | 可渲染/可显示内容 | 规则计算 |
| 构建与覆盖安装 | 将 C++ 编译为 Win32 DLL，把选定资产覆盖到既有模组目录 | C++ 源码、旧工具链、仓库资产 | DLL 与覆盖后的目标目录 | 创建完整可运行的游戏安装 |

边界所有权的核心规则：游戏状态以 DLL/宿主为权威；XML 是类型化配置来源；Python 只能通过已发布的 Cy* 接口、模块入口和事件参数访问或影响状态；资源只通过稳定标识和路径被引用。

## 关键数据与控制流

### 1. XML 配置进入 C++ 规则

```text
XML Schema ──约束──► XML 数据 ──字段名──► CvXMLLoadUtility/CvInfos
                                                │
                                                ▼
                                        GameCore 规则对象
```

单位战斗字段提供了完整抽样：

- `CIV4UnitSchema.xml:350-359` 声明生命、护甲、敏捷、攻击次数、攻击次数浮动和远程攻击次数。
- `CIV4UnitInfos.xml:140-150` 为单位提供值。
- `CvInfos.cpp:7290-7302` 按相同字段名读取。
- `CvUnit.cpp:9691-9718`、`10310-10445`、`10471-10505` 在生命、护甲、敏捷和攻击次数相关规则中消费这些信息。

因此 Schema、数据和 DLL 不是三个可独立替换的模块，而是一个按名称耦合的加载契约。

### 2. C++ 暴露数据给 Python/UI

```text
C++ 状态/查询 ─► Cy* 包装 ─► Boost.Python 注册 ─► Python Screen
       │                                             │
       └────────────── 界面脏标记/文本键 ─────────────┘
```

`CvDLLPython.cpp:42-84` 发布 `CyPlayer`、`CyUnit`、`CyPlot` 等对象；玩家食物查询在 `CyPlayerInterface1.cpp:123-130` 暴露，财政界面在 `CvFinanceAdvisor.py:94-122` 读取玩家食物、食物 commerce 和食物成本。

### 3. C++ 事件进入 Python

```text
GameCore 事件 ─► CvEventReporter/CvDllPythonEvents
               ─► CvEventInterface.onEvent
               ─► CvEventManager.handleEvent
               ─► 日志、脚本响应或 UI
```

模块名由 `CvDefines.h:147-167` 固定；`CvDllPythonEvents.cpp:9-26` 调用 `CvEventInterface.onEvent`；`CvEventManager.py:203-216` 按事件标签分派。近战与远程结算还通过 `combatLogCalc`、`combatLogHit`、`combatLogMiss` 发送结构化战斗日志事件，例如 `CvUnit.cpp:1775-1784`、`1838-1875` 与 `19484-19513`。

### 4. XML 指定 Python 回调

`PythonCallbackDefines.xml` 控制部分回调是否启用，`CvXMLLoadUtilitySet.cpp:172-229` 装载这些定义。`CvSpellInterface.py:19-65` 展示另一类契约：XML 信息对象提供 Python 表达式，入口脚本在既定参数上下文中执行它们。字段值、入口名、参数形状和脚本可见对象必须共同演化。

### 5. 覆盖安装流

```text
C++ 源码 ──旧 Win32 工具链──► CvGameCoreDLL.dll ─┐
XML / Python / Art / res ─────────────────────────┼─► 既有 Mods/Rampage/Assets
                                                  │   （覆盖，不是全量安装）
Rampage/installpatch.bat ─────────────────────────┘
```

## 定制规则域

### 核心战斗

单位最大生命、护甲、敏捷、攻击次数和攻击次数浮动由单位 XML 驱动。`CvUnit.cpp:1743-1915` 的近战结算按双方攻击次数循环，以敏捷相关闪避值决定命中，并把结果送入 Python 战斗日志；`CvUnit.cpp:10310-10445` 把护甲和敏捷纳入强度/闪避计算。

架构边界：字段定义属于 XML 契约，权威结算属于 DLL，玩家可见日志属于 Python/UI。任一层单独变化都会改变可配置范围、运行规则或可观察结果。

### 远程攻击

`CvUnit.cpp:19352-19429` 校验单位类型、最小/最大射程、可见性和目标；该路径明确忽略视线阻挡。`CvUnit.cpp:19433-19535` 按 XML 的远程攻击次数结算并发送战斗日志事件；`CvGameInterface.cpp:200-229` 使用相同最小/最大射程绘制选区。

架构边界：XML 数值、DLL 合法性/结算、C++ 选区渲染调用与 Python 日志必须表达同一射程语义。

### 基于回合起点的 `plotDistance` 移动半径与地块容量

`CvUnit.cpp:1303-1305` 在回合边界记录起点，`CvUnit.cpp:3591-3596` 以最大移动格数为半径，拒绝 `plotDistance` 超出边界的目标地块。该判断使用前述近似八边形的离散地图距离，不是累计路径长度或欧氏距离。`CvUnit.cpp:3439-3572` 建立单位容量检查并尝试累计运输货物成本；货物累计量是否真正进入拒绝计算存在下述静态风险。`CvPlot.cpp:3453-3486` 聚合地形、地物、改良、丘陵、城市和人口提供的容量。相应 XML 字段出现在 `CIV4UnitSchema.xml:303-305` 与 `CIV4TerrainSchema.xml:30-70`。

架构边界：移动合法性由 DLL 统一裁决；容量值由 XML 提供；界面或 AI 不应建立另一份独立容量语义。

### 工人占格收益

`CvUnit.cpp:1477-1560` 在工人进入或离开可工作地块时计算食物/商业产出、更新玩家 commerce、更新地块 worked 状态并标记相关界面为脏；坐标迁移在 `CvUnit.cpp:12673-12674` 调用进入/离开更新。Git 提交 `c671900` 同时改动 DLL、C++、Commerce/Improvement/Build/Unit XML、文本和动作资源，显示该能力天然跨层。

`CvPlot::m_bIsWorked` 的静态闭环不完整：当前 C++ 源码树只见初始化、`setWorked` 写入与 `isWorked` 读取定义，未见其他规则消费该 getter；`CvPlot` 的存档流也未见读写该字段。由此只能确认玩家 commerce 账本和地块 worked 标记是两个独立状态，不能确认标记会随存档恢复或参与账本重建。

架构边界：单位占格是触发源，DLL 中玩家账本是权威状态，XML/文本/动作资源描述能力，UI 只呈现结果；地块 worked 标记是否构成可持久化、可恢复的规则状态仍需运行验证。

### 玩家食物经济

`COMMERCE_FOOD` 同时存在于 C++ 枚举、Python 枚举暴露和 `CIV4CommerceInfo.xml`。`CvPlayer.cpp:2886-2893` 把食物纳入回合流程；`CvPlayer.cpp:7139-7189` 按军事单位成本计算净食物；`CvPlayer.cpp:13799-13824` 更新库存并把负数按固定倍率转为金币损失；`CyPlayerInterface1.cpp:123-130` 与 `CvFinanceAdvisor.py:94-122` 把成本和库存呈现给 Python 界面。

当前源码存在跨机制静态耦合：`CvPlayer::getCommerceRate` 在 `getDisableResearch() > 0` 时不区分 commerce 类型而直接返回 `0`，因此 `COMMERCE_FOOD` 也归零，并通过 `calculateBaseNetFood` 影响玩家净食物。该行为是否符合产品意图、加载 DLL 是否具有相同行为以及实际玩家影响均需运行验证。

架构边界：食物是玩家级经济账本，不是城市食物条的别名；C++ 枚举、XML commerce、DLL 状态、Python 暴露、文本和 UI 是同一个功能切面。

## 外部依赖边界

| 依赖 | 用途 | 仓库证据 | 是否由仓库提供 |
|---|---|---|---|
| Civilization IV: Beyond the Sword 游戏宿主 | 加载 GameCore DLL、XML、Python、资源和场景 | `*.CivBeyondSwordWBSave`、DLL/SDK 文件名和安装目标 | 否 |
| Fall from Heaven 2 完整模组内容 | 提供未覆盖的基础脚本和资源 | Python 入口引用未跟踪模块；场景 `ModPath` 指向 FFH2；大量 Art 路径不在覆盖包内 | 否 |
| Windows x86 ABI | 运行 `CvGameCoreDLL.dll` | 四个 DLL 均识别为 PE32 Intel 80386；Makefile 使用 `/SUBSYSTEM:WINDOWS` | DLL 产物是，宿主环境否 |
| Microsoft Visual C++ Toolkit 2003 与 Windows SDK | 编译、链接和资源编译 | `Rampage/Assets/src/CvGameCoreDLL.041o/Makefile:5-20` | 否 |
| Boost 1.32 / Boost.Python vc71 | C++ 与 Python 对象桥接 | `Makefile:9-10,63-73`，`CvDLLPythonIFaceBase.h:13-14` | Makefile 允许项目内或外部路径；完整可用性未知 |
| Python 2.4 headers/libs 与宿主嵌入式 Python | 编译绑定并执行脚本 | `Makefile:10,63-73`；Python 使用 Python 2 风格 API | 构建依赖完整性未知，运行时由宿主提供 |

## 约束矩阵

| 约束维度 | 强度 | 架构影响 | 证据/原因 |
|---|---|---|---|
| 性能：同进程回合与战斗延迟 | 高 | 战斗循环、单位移动校验、地块容量和玩家回合经济必须在游戏主循环可接受范围内完成；不能假设有异步服务卸载 | 规则直接位于 `CvUnit`、`CvPlot`、`CvPlayer`，并调用宿主接口 |
| 性能：启动装载 | 中 | XML 数量、Schema 一致性和资源查找影响启动；缓存不能掩盖契约错误 | `CvXMLLoadUtilitySet.cpp:172-229,776-835` 装载全局定义和信息类 |
| 成本：运行基础设施 | 低 | 没有服务器和数据库运维成本 | 单机模组、同进程 DLL/Python 架构 |
| 成本：环境复原 | 高 | 需要旧 Windows 游戏、旧编译器、SDK、Boost/Python ABI 和完整基础模组；人员与机器成本高于代码托管成本 | Makefile 的硬编码旧工具链与覆盖安装模式 |
| 运维复杂度：安装 | 高 | 覆盖目标目录、目标名称和基线版本必须准确，且需要能回溯被覆盖文件 | `installpatch.bat` 使用相对路径 `xcopy/copy`，不创建独立发行包 |
| 运维复杂度：构建 | 高 | NMake 路径与 VS solution 元数据不完全一致，构建可复现性不能由仓库单独保证 | Makefile 指向 VC++ 2003；solution 指向未跟踪的 `.vcxproj`，仓库只有 `.vcproj` |
| 一致性：跨层名称/枚举 | 极高 | Schema、XML、C++、Python、文本和资源必须作为单个变更单元验证 | 单位战斗字段、`COMMERCE_FOOD`、Python 模块名和 Art 路径均按字符串/枚举耦合 |
| 一致性：源码/二进制 | 极高 | C++ 源码与分发 DLL 必须来自同一构建；否则代码审查无法证明游戏实际行为 | 仓库同时保存源代码和预编译 DLL，部分提交只替换 DLL |
| 兼容性：宿主与基线 | 极高 | 覆盖包必须匹配目标 Civ4/FFH2 的 ABI、Python 模块和资源布局 | 缺失基础 Python 模块与资源只能由外部安装补齐 |
| 可观察性与验证 | 高 | 静态检查只能证明结构一致，游戏行为仍需 Windows 宿主中的构建/加载/存档/场景验证 | 仓库没有独立运行入口或自包含测试宿主 |

## 失败场景

| 场景 | 触发条件 | 可见后果 | 架构防线/验证重点 |
|---|---|---|---|
| DLL 与 XML 字段不匹配 | 只更新 Schema/数据或只更新读取 DLL | XML 装载失败、字段取默认值，或游戏规则与数据设计不符 | 将 Schema、数据、`CvInfos` 读取和 DLL 产物作为同一变更单元；启动装载验证 |
| DLL 与 Python 接口不匹配 | Python 调用未发布的 Cy* 方法，或 DLL 改变枚举/事件参数 | 导入后运行时报错、界面缺值、事件分派失败 | 校验 `DLLPublishToPython`、Cy* 绑定、入口模块名、事件参数与 UI 调用 |
| 覆盖包安装在错误或不完整基线上 | 相对安装路径解析到错误目录，或目标缺少 FFH2 基础脚本/资源 | DLL/数据未生效、Python import 失败、资源缺失，甚至加载到另一模组 | 安装前确认绝对目标与基线版本；验证被加载 DLL/模块，而不是只检查复制成功 |
| 源码与预编译 DLL 漂移 | 修改 C++ 但未重建 DLL，或提交只替换 DLL | 文档和源码描述与游戏实际行为不同 | 对 DLL 建立来源/哈希证据；运行验收必须记录被加载二进制 |
| 资源键或路径断裂 | XML/Text/Python 引用覆盖包和基础模组都没有的文件或键 | 缺图、缺字形、模型/界面加载错误 | 枚举全部资源引用并在合并后的目标目录检查；关注大小写和字体文件 |
| 场景路由到非预期模组 | 使用仓库场景文件，而其 `ModPath` 仍指向 `Fall from Heaven 2` | 场景可能加载 FFH2 而不是 Rampage 规则 | 把场景 `ModPath` 当作外部路由配置验证；不能由目录名推断加载目标 |
| 旧工具链或 ABI 不可复原 | 缺少 VC++ 2003、Windows SDK、Boost 1.32、Python 2.4 或兼容库 | 无法重建 DLL，或构建产物不能被宿主装载 | 分层验证工具链、Win32 产物、导出与宿主加载；非 Windows 静态检查不能替代运行验证 |
| 边界规则与 UI 语义漂移 | DLL 改变射程、容量或食物计算，但选区/顾问页/文本不变 | 允许行为与玩家看到的信息不一致 | 对每个定制规则同时验证规则结果、查询接口、文本和可视反馈 |
| 战斗辅助值影响未知 | `CvUnit.cpp:10471-10505` 的部分辅助函数返回固定值 `999`、`97`，而局部计算未用于返回 | 依赖这些辅助值的 AI、预览或胜率可能与实际结算不一致 | 先追踪所有调用者并做运行对照；在证据不足时不得断言具体玩家影响 |
| 玩家食物状态未见进入存档流，且每回合修正缺少非零写入入口 | **静态事实：** `m_iFood`、`m_iFoodPerTurn` 声明于 `CvPlayer.h:1184-1185` 并在 `CvPlayer::reset` 归零；完整 `read/write` 流程未见读写二者（`CvPlayer.cpp:416-417,16813-17328,17334-17800`）。当前源码中 `m_iFoodPerTurn` 除归零、净食物读取、getter 与 Cy 查询暴露外，未见 setter、change 或其他赋值入口（`CvPlayer.cpp:417,7185,8737-8739`；`CyPlayer.cpp:805-807`；`CyPlayerInterface1.cpp:189`） | **推断风险：** 存读档后玩家食物储备或修正可能与保存前漂移；`m_iFoodPerTurn` 更像只读的静态扩展位，当前源码路径可能无法产生非零修正 | **运行未知：** 实际运行包是否存在当前源码未见的写入来源、save/reload 是否保留数值均未复现；必须用非零储备与修正值的 Windows 存档对账，并记录 DLL 哈希 |
| 禁用研究状态清零所有 commerce 查询结果 | **静态事实：** `CvPlayer::getCommerceRate` 在 `getDisableResearch() > 0` 时对任意 `CommerceTypes` 直接返回 `0`（`CvPlayer.cpp:11577-11603`）；`calculateBaseNetFood` 使用 `getCommerceRate(COMMERCE_FOOD)` 计算净食物（`CvPlayer.cpp:7181-7189`） | **推断风险：** 原本面向研究能力的状态可能同时清零食物商业收入，使研究规则跨机制影响玩家食物账本、HUD 与财务展示 | **运行未知：** 同时清零全部 commerce 是否符合产品意图、实际加载 DLL 是否一致以及具体玩家影响均未复现；需在 `COMMERCE_FOOD` 非零时切换禁用研究条件，对账所有 commerce、HUD、财务顾问与回合结算，并记录 DLL 哈希 |
| Work Tile 的地块标记未见存档与规则消费闭环 | **静态事实：** `m_bIsWorked` 只见初始化为 `false`、`setWorked` 写入与 `isWorked` getter 定义（`CvPlot.cpp:74,4880-4888`；`CvPlot.h:512-513,659`）；当前 C++ 源码树未见其他规则调用 `isWorked()`，完整 `CvPlot::read/write` 区段也未见该字段（`CvPlot.cpp:9181-9420,9426-9667`） | **推断风险：** 存读档后的 worked 标记、恢复语义与玩家 commerce 账本可能不同步；标记也可能不参与任何后续规则判断 | **运行未知：** 宿主或其他路径是否重建标记、账本在 save/reload 后如何变化以及玩家可见表现均未复现；需保存带 Work Tile 工人的局面，重载后对账地块标记相关行为、玩家食物/金币 commerce，并验证工人再次进入和离开时的增减 |
| 运输货物成本被累计但未参与容量拒绝 | **静态事实：** `CvUnit::hasMaxUnitPerTile` 把运输者与可防守货物成本累计到 `iActualUnitWithCargo`（`CvUnit.cpp:3466-3499`），后续返回判断只使用 `iLandUnitCost`、`iFlyingUnitCost` 与容量，未读取该累计变量（`CvUnit.cpp:3523-3572`） | **推断风险：** 运输者携带的可防守货物可能未增加地块容量占用，与 F004 的货物计入目标漂移 | **运行未知：** 当前加载 DLL 对陆地/飞行运输者、不同货物和满容量地块的实际拒绝行为未复现；需在记录 DLL 身份后做成对容量场景 |
| 城市训练检查未计入候选单位成本 | **静态事实：** `CvCity::canTrain` 读取城市地块现有陆地/飞行成本；候选单位成本只用于判断是否为零，没有加到两个占用总量后再比较（`CvCity.cpp:1834-1870`，尤其 `1852-1867`） | **推断风险：** 当前占用尚未超限时，训练一个正成本单位可能被允许并在完成后造成超容 | **运行未知：** 生产完成或单位放置路径是否另有二次容量门禁、等值边界如何处理均未复现；需覆盖“现有占用 + 候选成本”低于、等于和高于容量的场景 |
| 近战死亡检查位于双方同轮掷骰之后 | **静态事实：** 近战循环先处理防守方掷骰并可对攻击方调用 `changeDamage`，随后仍进入攻击方掷骰分支；`isDead()` 检查位于两段之后（`CvUnit.cpp:1796-1996`） | **推断风险：** 防守方先造成致死伤害时，攻击方可能仍在同一轮反击，与 F002“任一方死亡立即停止剩余掷骰”的产品目标漂移 | **运行未知：** 死亡状态、副作用、撤退/先攻分支或实际加载 DLL 是否阻止该反击均未复现；需用可确定首击致死的存档和逐次日志验证 |

## 事实、推断与未知汇总

### 事实

- 四个顶层目录都提供覆盖式安装脚本；只有两个目录包含 C++ 源码，`Rampage` 还包含 Art 与 res。
- `Rampage` 的 XML Schema、XML 数据、C++ 读取和 Python/UI 暴露共同承载定制规则。
- `Rampage` 的 Makefile声明旧 Win32 C++ 工具链、Boost 1.32 和 Python 2.4 依赖。
- `CvGameCoreDLL.dll` 是 x86 Windows DLL；Python 通过 Boost.Python/Cy* 接口与它交互。
- 仓库没有关系数据库边界。

### 推断

- `Streak` 从 FFH2 数据快照起步，`Streak 3` 组合了 FFH2 数据与 Streak DLL，`Rampage` 从 Streak 3 内容快照继续演化，并重新纳入 FFH2 SDK 源码作为开发基础。
- `Rampage` 因最晚提交、完整源码和最宽资源覆盖而是最有信息量的维护焦点。
- 缺失模块和资源预期由完整 Civ4/FFH2 安装提供，因此仓库不能单独启动。

### 未知

- 用户机器实际加载的是 `Fall from Heaven 2`、`Streak`、`Streak 3`、`Rampage`，还是另一个复制后的目录。
- 用户机器加载的 DLL 哈希是否等于仓库中的任何 DLL。
- 覆盖包要求的 Civ4 BTS、FFH2 和补丁精确版本。
- 旧 Makefile、`.vcproj` 或 solution 中哪条构建路径曾作为权威发布流程；solution 引用的 `.vcxproj` 不在仓库中。
- 未纳入仓库的基础 Python 模块和资源来自哪个精确发行包。
- 所有场景在 Rampage 规则下是否兼容；场景文件的 `ModPath` 指向 FFH2。
- 固定战斗辅助返回值的完整调用影响。
- 外部全局定义 `RANGED_ATTACKS_USE_MOVES` 的值及其对重复远程动作的影响。
- 当前加载 DLL 的玩家食物储备是否进入存档流，以及 `m_iFoodPerTurn` 是否存在源码外的非零写入来源。
- “禁用研究”是否应同时清零包括 `COMMERCE_FOOD` 在内的所有 commerce，以及该静态耦合在实际加载 DLL 中如何影响 HUD、财务顾问与回合食物结算。
- 运输者携带的可防守货物是否增加陆地/飞行容量占用；源码中 `iActualUnitWithCargo` 的累计结果未进入后续拒绝判断。
- 城市训练完成或单位放置阶段是否存在第二次容量门禁，以及现有占用加候选成本等于或超过容量时的准确行为。
- 防守方先造成致死伤害时，攻击方是否仍执行同一轮反击；需要与 F002 的立即停止目标做运行对账。
- `Work Tile` 完成后的贡献与视觉行为；`m_bIsWorked` 是否由宿主或其他路径在存读档时重建，以及地块标记与玩家 commerce 账本是否保持同步。

## 架构阅读顺序

1. 先读本文确认边界、谱系和数据流。
2. 再读 [技术栈](tech-stack.md) 理解宿主、ABI、工具链和覆盖安装限制。
3. 修改任何规则前，先应用 [ADR-0002](decisions/0002-cross-layer-consistency.md) 的跨层一致性检查。
4. 判断目标目录或运行态前，先应用 [ADR-0001](decisions/0001-rampage-focus.md) 的证据限制。
