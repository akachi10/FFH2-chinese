# ffh2-mods-ba

这是一个为《Civilization IV: Beyond the Sword》及 Fall from Heaven 2（FFH2）派生内容保存规则修改与资源覆盖的仓库。它的价值不只在于保存代码，还在于让近战、远程、移动、地块容量、工人收益和玩家食物经济等定制规则能够被继续理解、修改和验证。

> 本仓库是覆盖包，不是可独立启动的游戏或完整模组发行物。运行与构建依赖仓库外的 Civ4/BtS、完整 FFH2 基线、旧版 Win32 工具链和匹配资源。

## 代码线焦点

仓库保留 `Fall from Heaven 2/`、`Streak/`、`Streak 3/` 和 `Rampage/` 四条内容谱系。`Rampage/` 拥有最完整、最后演化的 C++、XML、Python 与资源组合，因此是理解和维护的重点；这不表示任何用户机器当前实际加载的版本就是 Rampage。

## 项目组成

- 外部游戏宿主与完整 FFH2 基线：提供仓库没有携带的引擎、脚本和基础资源。
- XML Schema 与数据：声明单位、地形、改良、经济、文本和资源配置。
- C++ GameCore DLL：执行战斗、移动、容量、工人收益、玩家经济与 AI 规则。
- C++/Python 桥接与 Python：承接宿主回调、事件、脚本规则和界面逻辑。
- Art、`res` 与 Text：提供模型、贴图、字体、音效和本地化内容。
- 构建与覆盖安装：生成 Win32 DLL，并将成套资产覆盖到既有模组目录。
- `docs/`：保存产品、架构、接口、运行环境、测试、通用方法与 Sprint 文档。

这些部分在同一个游戏进程中协作。DLL、XML、Python、文本与资源之间的名称和行为是一份共同契约，修改玩法时不能只验证单层文件。

## 推荐阅读顺序

1. 从 [项目文档地图](docs/README.md) 选择与你的任务匹配的阅读路径。
2. 读 [产品定义](docs/product/product-definition.md)，理解产品边界和核心玩法。
3. 读 [系统架构总览](docs/architecture/overview.md)，理解运行时组件与跨层数据流。
4. 动手前查看 [接口契约](docs/api/README.md)、[环境状态](docs/ops/status.md) 和 [测试计划](docs/testing/test-plan.md)。

仓库内的静态证据可以说明结构与契约，但不能单独证明旧工具链可构建、覆盖包已正确安装，或游戏实际加载了哪一份 DLL。涉及运行结论时，应以目标机器上的加载与验收证据为准。
