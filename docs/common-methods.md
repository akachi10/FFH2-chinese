## ffh2-mods-ba（Rampage）

索引范围：`Rampage` 代码线中支撑玩家食物经济、工人占格收益、移动与地块容量、近战与远程战斗，以及 XML → C++ → Python/UI 契约的 C++ 与 Python 方法。

纳入标准：跨至少两处调用，或封装非平凡通用逻辑；SDK 通用方法仅在直接承载上述定制机制时登记。

### CvPlayer

`Rampage/Assets/src/CvGameCoreDLL.041o/CvPlayer.cpp:7139` — 汇总玩家食物收支、食物库存与百分制 commerce 账本。

- `int CvPlayer::calculateFoodCosts() const` — 计算玩家军事单位与额外单位成本形成的每回合食物支出。
- `int CvPlayer::calculateBaseNetFood() const` — 汇总食物 commerce、每回合修正和食物成本得到基础净食物。
- `int CvPlayer::calculateFoodRate() const` — 提供回合结算和界面共用的净食物速率。
- `int CvPlayer::getFood() const` — 读取玩家级食物库存。
- `void CvPlayer::setFood(int iNewValue)` — 更新食物库存并刷新相关界面脏标记。
- `void CvPlayer::changeFood(int iChange)` — 通过统一 setter 增减食物库存。
- `int CvPlayer::getFoodPerTurn() const` — 读取玩家级每回合食物修正。
- `int CvPlayer::getCommerceRate(CommerceTypes eIndex) const` — 读取按百分制内部值折算后的玩家 commerce 速率。
- `void CvPlayer::changeCommerceRate(CommerceTypes eIndex, int iChange)` — 增减玩家 commerce 内部账本并刷新游戏数据界面。
- `void CvPlayer::doFood()` — 执行回合食物结算并将负库存按固定倍率转为金币损失。

### CvUnitInfo

`Rampage/Assets/src/CvGameCoreDLL.041o/CvInfos.cpp:7013` — 加载并提供单位容量、生命、护甲、敏捷和攻击次数等 XML 配置。

- `bool CvUnitInfo::read(CvXMLLoadUtility* pXML)` — 从单位 XML 读取基础字段与 Rampage 定制战斗、射程和容量字段。
- `int CvUnitInfo::getUnitPlotCost() const` — 读取单位占用的地块容量成本。
- `int CvUnitInfo::getMaxHitPoints() const` — 读取单位类型的最大生命值。
- `int CvUnitInfo::getArmour() const` — 读取单位类型的护甲值。
- `int CvUnitInfo::getDexterity() const` — 读取单位类型的敏捷值。
- `int CvUnitInfo::getAttackCount() const` — 读取单位近战结算的攻击次数。
- `int CvUnitInfo::getAttackCountVariance() const` — 读取攻击次数浮动值。
- `int CvUnitInfo::getAirCombatCount() const` — 读取单位远程结算的攻击次数。

### CvPlot

`Rampage/Assets/src/CvGameCoreDLL.041o/CvPlot.cpp:3423` — 聚合地块已占单位成本和地形、地物、改良、城市提供的容量。

- `int CvPlot::getUnitPlotCost(bool flyingUnitsOnly) const` — 分别累计地块上可计费的空中或地面单位成本。
- `int CvPlot::getUnitPlotCapacity() const` — 计算地块或城市可承载的单位容量。

### CvUnit

`Rampage/Assets/src/CvGameCoreDLL.041o/CvUnit.cpp:1477` — 承载单位占格收益、移动限制、容量校验和定制战斗结算。

- `void CvUnit::updateCommerce(CvPlot* pPlot, bool isLeavingPlot)` — 在可工作单位进入或离开地块时同步玩家食物与金币 commerce。
- `void CvUnit::updateInitialPlot(int x, int y)` — 记录单位本回合移动半径的起始坐标。
- `void CvUnit::resolveCombat(CvUnit* pDefender, CvPlot* pPlot, CvBattleDefinition& kBattle)` — 按攻击次数、敏捷、护甲和撤退规则结算近战并发送战斗日志事件。
- `int CvUnit::combatEffectiveness(const CvUnit* pAttacker) const` — 估算单位面对指定攻击者时的防守效能。
- `bool CvUnit::isBetterDefenderThan(const CvUnit* pDefender, const CvUnit* pAttacker) const` — 使用定制效能比较选择更优防守者。
- `bool CvUnit::hasMaxUnitPerTile(const CvPlot* pPlot) const` — 按地面与飞行容量、地块现有单位成本、单位可防守性和零成本规则判断目标格是否超载。
- `bool CvUnit::canMoveInto(const CvPlot* pPlot, bool bAttack, bool bDeclareWar, bool bIgnoreLoad) const` — 统一校验回合移动半径、地块容量和基础进入条件。
- `bool CvUnit::isAdjacentToEnemy(CvPlot* pPlot, bool checkInvisible)` — 检查目标格八邻域内是否存在交战敌军。
- `void CvUnit::move(CvPlot* pPlot, bool bShow)` — 扣除移动力、应用敌军邻接区耗尽移动力规则并迁移单位。
- `bool CvUnit::canAttackPlotAt(const CvPlot* pPlot, int iX, int iY) const` — 校验相邻目标、攻击次数状态和目标防守者以决定显式地块攻击是否可用。
- `bool CvUnit::build(BuildTypes eBuild)` — 执行地块建设并在产出变化前后重算工人贡献的食物与金币 commerce。
- `int CvUnit::maxHitPoints() const` — 提供单位类型配置驱动的最大生命值。
- `int CvUnit::armourValue() const` — 提供单位类型配置驱动的护甲值。
- `int CvUnit::maxCombatStr(const CvPlot* pPlot, const CvUnit* pAttacker, CombatDetails* pCombatDetails, bool bSurroundedModifier) const` — 计算包含护甲、地块、晋升和伤害类型修正的战斗强度或伤害基值。
- `int CvUnit::currCombatStr(const CvPlot* pPlot, const CvUnit* pAttacker, CombatDetails* pCombatDetails, bool bSurroundedModifier) const` — 提供不随当前生命值衰减的当前战斗强度。
- `int CvUnit::currEvasionChance(CombatDetails* pCombatDetails) const` — 由敏捷与战斗修正计算当前闪避值。
- `int CvUnit::unitCombatAttacks() const` — 提供近战固定轮次使用的攻击次数。
- `int CvUnit::rangeCombatDamage(const CvUnit* pDefender) const` — 以远程基础强度减目标护甲计算单次远程伤害。
- `bool CvUnit::canRangeStrikeAt(const CvPlot* pPlot, int iX, int iY) const` — 校验可见性、最小和最大射程及有效防守目标。
- `bool CvUnit::rangeStrike(int iX, int iY)` — 按远程攻击次数、闪避和护甲结算远程攻击并发送战斗日志事件。
- `void CvUnit::setXY(int iX, int iY, bool bGroup, bool bUpdate, bool bShow, bool bCheckPlotVisible)` — 统一处理单位坐标迁移及迁移前后的工人 commerce 更新。

### CvSelectionGroup

`Rampage/Assets/src/CvGameCoreDLL.041o/CvSelectionGroup.cpp:674` — 把界面任务请求路由到单位移动、显式地块攻击和远程攻击能力。

- `bool CvSelectionGroup::canStartMission(int iMission, int iData1, int iData2, CvPlot* pPlot, bool bTestVisible, bool bUseCache)` — 汇总编组内单位能力判断任务是否可启动。
- `void CvSelectionGroup::startMission()` — 初始化任务队列头部任务及其单位状态。
- `void CvSelectionGroup::continueMission(int iSteps)` — 推进任务并调用单位显式地块攻击或远程攻击实现。

### CvGameCoreUtils 自由函数

`Rampage/Assets/src/CvGameCoreDLL.041o/CvGameCoreUtils.cpp:647` — 提供 C++ 战斗、AI 与 Python 桥接共用的战斗胜率计算。

- `int getCombatOdds(CvUnit* pAttacker, CvUnit* pDefender)` — 使用双方敏捷计算供战斗日志和 AI 使用的胜率值。

### CvGameTextMgr

`Rampage/Assets/src/CvGameCoreDLL.041o/CvGameTextMgr.cpp:288` — 生成供主界面显示的玩家食物库存和每回合变化文本。

- `void CvGameTextMgr::setFoodStr(CvWString& szString, PlayerTypes ePlayer)` — 格式化玩家食物库存及正负净食物速率。

### CyGameTextMgr

`Rampage/Assets/src/CvGameCoreDLL.041o/CyGameTextMgr.cpp:55` — 将 C++ 食物状态文本转换为 Python 可读取的字符串。

- `std::wstring CyGameTextMgr::getFoodStr(int iPlayer)` — 调用文本管理器生成指定玩家的食物状态文本。

### CyPlayer

`Rampage/Assets/src/CvGameCoreDLL.041o/CyPlayer.cpp:519` — 向 Python 财政界面暴露玩家食物库存与成本查询。

- `int CyPlayer::calculateFoodCosts()` — 转发玩家食物成本计算。
- `int CyPlayer::getFood()` — 转发玩家食物库存读取。

### CvEventReporter

`Rampage/Assets/src/CvGameCoreDLL.041o/CvEventReporter.cpp:37` — 将 C++ 自定义事件及参数统一送入 Python 事件管理器。

- `void CvEventReporter::genericEvent(const char* szEventName, void *pyArgs)` — 按事件名转发通用 Python 事件。

### CvEventManager

`Rampage/Assets/python/CvEventManager.py:204` — 分派 DLL 事件并把近战与远程命中结果写入双方战斗日志。

- `def handleEvent(self, argsList)` — 根据事件标签查找处理器并转发规范化参数。
- `def onCombatLogCalc(self, argsList)` — 解包战斗详情并调用公共战斗摘要构造器。
- `def onCombatLogHit(self, argsList)` — 根据攻击方标记生成命中、伤害和战败消息。
- `def onCombatLogMiss(self, argsList)` — 根据攻击方标记生成未命中消息。

### CvUtil

`Rampage/Assets/python/CvUtil.py:353` — 提供战斗日志处理器共用的双方状态与胜率摘要格式化。

- `def combatMessageBuilder(cdAttacker, cdDefender, iCombatOdds)` — 向交战双方输出单位生命和战斗胜率摘要。
