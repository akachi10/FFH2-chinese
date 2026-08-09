# 项目文档地图

本页是 `ffh2-mods-ba` 的第二层入口：先按任务选择阅读路径，再进入负责细节与证据的专题文档。文档以 `Rampage/` 作为仓库理解重点和最后演化的代码线，但不会据此断言用户机器当前加载的是 Rampage。

返回 [项目入口](../README.md)。

## 七类文档

| 领域 | 负责回答 | 什么时候读 | 专题文档 |
|---|---|---|---|
| 产品 | 系统为谁服务、提供什么规则、玩家如何感知、需求如何编号 | 判断需求、玩法语义或 UI 表达时 | [产品定义](product/product-definition.md) · [PRD](product/PRD.md) · [UE 交互规格](product/UE-spec.md) · [产品文档变更日志](product/changelog.md) |
| 架构 | 仓库边界、内容谱系、同进程组件、技术栈与关键决策 | 判断改动落在哪一层、依赖什么宿主或为何必须跨层验证时 | [系统架构总览](architecture/overview.md) · [技术栈](architecture/tech-stack.md) · [ADR-0001：Rampage 焦点](architecture/decisions/0001-rampage-focus.md) · [ADR-0002：跨层一致性](architecture/decisions/0002-cross-layer-consistency.md) |
| 接口 | XML、C++、Python、事件、脚本与原生 UI 之间共享哪些名称、对象和调用形状 | 修改字段、绑定、入口模块、事件、脚本回调或界面入口前 | [接口总览](api/README.md) · [XML/C++ 契约](api/modules/xml-cpp-contract.md) · [C++/Python 契约](api/modules/cpp-python-contract.md) · [事件与脚本契约](api/modules/events-and-scripting.md) · [原生 UI 入口](api/modules/ui-entrypoints.md) |
| 运行环境 | 外部依赖、目录身份、服务生命周期、当前证据和排障方法 | 准备构建/运行环境、覆盖安装或定位“修改未生效”时 | [环境配置](ops/environments.md) · [服务生命周期](ops/services.md) · [环境状态](ops/status.md) · [故障排查](ops/troubleshooting.md) · [存档加载与坏单位诊断](ops/save-load-diagnostics.md) |
| 测试 | 静态、构建与运行验收分别能证明什么，如何记录证据 | 修改前确定验证边界，修改后判断能否交付时 | [测试计划](testing/test-plan.md) · [静态验证](testing/static-validation.md) · [运行验收](testing/runtime-acceptance.md) |
| 通用方法 | 哪些跨调用点或非平凡逻辑已有唯一实现 | 写 C++ 前查重、定位共用业务入口或合并重复实现时 | [通用方法索引](common-methods.md) |
| Sprint | 当前知识基线如何推进、任务与阻塞如何记录 | 查看本轮文档工作的执行状态与后续待办时 | [知识基线 Sprint](sprints/sprint-documentation-baseline.md) · [文档 Backlog](sprints/backlog.md) |

专题文档保存详细事实、代码证据和执行记录；入口页只负责导航，不复制这些细节。

## 按任务阅读

### 第一次理解项目

[产品定义](product/product-definition.md) → [系统架构总览](architecture/overview.md) → [接口总览](api/README.md) → [技术栈](architecture/tech-stack.md) → [环境状态](ops/status.md)

先确定产品与覆盖包边界，再理解组件和接口；最后检查哪些环境结论已经被验证、哪些仍然未知。

### 修改玩法

[PRD](product/PRD.md) → [UE 交互规格](product/UE-spec.md) → [跨层一致性决策](architecture/decisions/0002-cross-layer-consistency.md) → [接口总览](api/README.md) → [通用方法索引](common-methods.md) → [测试计划](testing/test-plan.md)

先确认最终语义，再沿 XML、DLL、桥接、Python、文本和资源查全影响面；写新逻辑前先确认没有可复用的唯一实现。

### 排查运行问题

[环境状态](ops/status.md) → [环境配置](ops/environments.md) → [服务生命周期](ops/services.md) → [故障排查](ops/troubleshooting.md) → [存档加载与坏单位诊断](ops/save-load-diagnostics.md) → [运行验收](testing/runtime-acceptance.md)

先区分已有事实与未知项，再逐层确认外部基线、目标目录、DLL 身份、XML、Python 和资源；不要把“文件已复制”等同于“游戏已加载”。

### 验证改动

[跨层一致性决策](architecture/decisions/0002-cross-layer-consistency.md) → [接口契约](api/README.md) → [静态验证](testing/static-validation.md) → [运行验收](testing/runtime-acceptance.md) → [环境状态](ops/status.md)

静态检查只能证明结构和名称契约；构建证据与目标机器中的实际加载、行为和视觉证据需要分别记录。
