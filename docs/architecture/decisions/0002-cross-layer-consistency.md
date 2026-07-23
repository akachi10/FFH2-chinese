# ADR-0002：DLL、XML、Python 与资源构成单一一致性边界

- **状态：** 接受
- **日期：** 2026-07-15
- **范围：** 规则、数据、界面与分发内容的变更和验证
- **依据：** Rampage 的 XML 装载、C++ 规则、Python 桥接、资源引用与覆盖安装证据

## 背景

Civilization IV 模组不是由互相独立部署的服务组成。宿主在同一模组目录中装载 `CvGameCoreDLL.dll`、XML、Python 和资源；这些层通过字符串、枚举顺序、字段名、模块/函数名、事件参数、文本键和资源路径直接耦合。

代表性证据：

- `CIV4UnitSchema.xml:350-359` 定义生命、护甲、敏捷、攻击次数与远程攻击次数，`CIV4UnitInfos.xml:140-150` 提供数据，`CvInfos.cpp:7290-7302` 按同名字段读取，`CvUnit.cpp` 消费这些值。
- `COMMERCE_FOOD` 同时位于 `CvEnums.h:700`、`CyEnumsInterface.cpp:496` 和 `CIV4CommerceInfo.xml:46-47`；玩家食物状态经 CyPlayer 绑定进入 Python 财政界面。
- `CvDefines.h:147-167` 固定 Python 模块名，`CvDllPythonEvents.cpp:14-26` 调用 `CvEventInterface.onEvent`，`CvEventManager.py:203-216` 按事件标签分派。
- `CvSpellInterface.py:19-65` 执行 XML 信息对象提供的 Python 表达式，参数上下文也是契约的一部分。
- Art XML 通过路径引用模型、动画和字体；`Rampage/installpatch.bat:1-5` 把 DLL、XML、Python、Art 和 res 覆盖到同一目标目录。
- Git 提交 `c671900` 为工人占格收益同时修改 DLL、C++、多个 XML、文本和动作资源；`49d4af0` 为食物机制同时修改 DLL、XML 文本、Python UI、C++ 与 Python 绑定。

## 决策

把以下内容定义为一个跨层一致性边界：

1. C++ 源码及由它生成的 `CvGameCoreDLL.dll`。
2. XML Schema、XML 数据、Global Defines、Python callback defines 和文本键。
3. C++/Python 桥接中的 Cy* 类型、枚举、模块名、函数名与事件参数。
4. Python 入口、规则脚本、事件处理和 UI。
5. XML/Python 引用的 Art、res、字体、模型、动画、音频与本地化资源。
6. 把上述内容放入最终目标目录的覆盖清单和基础模组版本。

“单一边界”不表示所有文件必须在一个目录或由一个角色维护；它表示一项跨层规则不能只验证其中一层。变更的最小一致性单位由受影响契约决定，验证目标是覆盖后的最终文件集合和实际加载 DLL。

## 契约面

| 契约面 | 生产方 | 消费方 | 一致性要求 |
|---|---|---|---|
| XML 字段与结构 | XML Schema | XML 数据、C++ 装载器 | 字段名、类型、可选性和顺序符合装载预期 |
| XML 类型/枚举 | XML 数据、C++ enum | C++ 规则、Python enum、UI | 标识与序号映射稳定，不能单层插入或删除后假设其他层自动适配 |
| GameCore 查询与状态 | C++ 规则/Cy* 包装 | Python 规则与 UI | 发布的方法、返回语义和生命周期匹配调用方 |
| Python 模块与函数 | Python 入口 | 游戏宿主与 C++ `callFunction` | 模块名、函数名和参数形状保持一致 |
| 事件标签与负载 | C++ EventReporter | Python EventManager | 标签、参数顺序、双方状态对象和返回约定一致 |
| 文本键 | XML/C++/Python | 文本 XML/UI | 键存在且格式参数数量、顺序匹配 |
| 资源路径 | Art XML/Python/XML 数据 | 游戏资源加载器 | 合并后的目标目录存在资源，路径大小写和格式可被宿主识别 |
| 源码/二进制 | C++ 构建链 | 游戏宿主 | DLL 可追溯到对应源码和依赖，ABI 与宿主兼容 |
| 覆盖清单 | 安装脚本/分发包 | 目标模组目录 | 所有受影响层被复制，且不会与错误基线混合 |

## 备选方案

| 方案 | 变更成本 | 运行风险 | 可追溯性 | 评估 |
|---|---:|---:|---:|---|
| 每层独立修改和验收 | 低（局部） | 极高；字符串和枚举错配只能在加载/运行时暴露 | 低 | 不采用 |
| 只绑定 DLL 与 XML | 中 | 高；Python、UI、文本和资源仍可漂移 | 中 | 不采用 |
| DLL、XML、Python、资源与覆盖基线统一验证 | 中至高 | 最低；覆盖真实耦合面 | 高 | 采用 |
| 将全部逻辑迁入单一语言/现代平台 | 极高且范围不明 | 未知；会改变宿主兼容面 | 未知 | 不在本决策范围；没有需求或证据支持 |

## 权衡

统一边界提高每项规则变更的检查范围，尤其是只改数值或只改 UI 时也必须确认上下游没有漂移；代价是文档、代码审查和验收需要跨 C++、XML、Python 与资源协作。

这种成本符合系统真实结构。局部修改看似便宜，但错误通常在游戏启动、特定单位交战、特定回合结算或特定 UI 页面才出现，定位成本远高于跨层静态核对。

## 一致性验证原则

验证按三层证据递进：

1. **静态契约：** XML 可解析；Schema 字段与 C++ 读取一致；类型、枚举、模块/函数、事件、文本键和资源路径可追踪。
2. **构建契约：** C++ 可由声明工具链生成 Win32 DLL；Cy* 暴露和导出与 Python/宿主匹配；产物记录来源与哈希。
3. **运行契约：** 完整 Windows 游戏环境加载预期模组、预期 DLL 和合并资产，并覆盖受影响规则及 UI 的行为。

任一层通过都不能替代下一层。非 Windows 环境可以提供第一层证据，但不能据此声明 DLL 可重建或游戏可运行。

## 典型变更切面

| 规则切面 | 必查范围 |
|---|---|
| 单位生命/护甲/敏捷/攻击次数 | Unit Schema、UnitInfos、CvInfos、CvUnit 结算、战斗日志、DLL |
| 远程攻击 | 射程/次数 XML、CvUnit 合法性与结算、范围显示、事件日志、资源动画、DLL |
| 移动与地块容量 | Unit/Terrain/Feature/Improvement/GlobalDefines、CvInfos、CvPlot、CvUnit、AI/UI 可见反馈、DLL |
| 工人占格收益 | Build/Unit/Improvement/Commerce/Text XML、CvUnit/CvPlot/CvPlayer、动作资源、经济 UI、DLL |
| 玩家食物经济 | Commerce/Text XML、C++ 枚举与玩家状态、Cy* 绑定、Python 枚举/UI、DLL |

这些是验证边界，不是实现步骤或字段设计。

## 后果

- 代码评审不能用“XML-only”“Python-only”标签结束判断；必须先证明该改动确实没有跨层消费者。
- 预编译 DLL 与 C++ 源码被视为同一规则交付物；只有其中之一变化时，状态保持未知，直到来源被证明。
- 安装验证面向合并后的目标目录，而不是只面向仓库文件；外部 FFH2 基线属于一致性输入。
- 文本和资源不是装饰性附属物。只要规则或 UI 引用它们，它们就属于相同契约面。
- 项目没有关系数据库，因此不存在用数据库迁移解决这些一致性问题的架构层。

## 已知风险与未知

- 仓库中的 Python 入口引用未跟踪的 `CvGameInterfaceFile.py` 与 `CvEventInterface.py`，它们的精确基线版本未知。
- Art 定义引用的部分字体和大量基础模型不在覆盖包中，只能在最终安装目录确认。
- solution 引用未跟踪 `.vcxproj`，预编译 DLL 的构建来源未知。
- 场景 `ModPath` 多数指向 `Fall from Heaven 2`，场景运行时可能绕过预期 Rampage 目录；具体行为需宿主验证。
- XML 缓存、存档兼容和枚举顺序变化的实际影响需要独立运行证据。

## 相关文档

- [系统架构总览](../overview.md)
- [技术栈与执行环境边界](../tech-stack.md)
- [ADR-0001：以 Rampage 作为仓库理解重点](0001-rampage-focus.md)
