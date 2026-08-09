# MM汉化MOD-YK · 英克中文版专用覆盖包

适配对象:**英克(YK)官方简体中文版 Civ4/BtS**(日版 CyberFront 底子,本机安装于
`C:\Civilization4`)。与旧版 `MM汉化MOD/`(英文版 BtS 路线,已废弃)不同,本包采用
中文版 exe 的 6 列文本格式:

```
<Tag> <English>原文</English> <L1/> <L2/> <L3/> <L4/> <Chinese>译文实体</Chinese>
```

- 格式逆向自 `ffh2_041_o_ch` 补丁(civclub 社区,2010)与 YK 正版 BtS 自带文本;
  DLL 源码(`CvInfos.cpp` `CvGameText::read`)证实列按位置读取、每条必须齐 6 列。
- 译文 12,725 条,全部来自上一轮 Sprint 的翻译成果(经 `tools/mm-l10n/convert_yk6.py`
  转换并内置校验:结构、Tag 序列、往返等价、纯 ASCII)。
- `Resource/` 为 SimSun 字体 theme(与官方补丁同手法)。
- `Assets/res/Fonts/` 携带 **YK 排布的 GameFont.tga / GameFont_75.tga**(2026-07-24 推翻
  原决策 A3):MM 自带字模是**美版排布**,YK 日版 exe 按 CJK 排布取图标 → HUD 金币/科研/
  法力列、悬浮文本内嵌图标全部错位成乱码字符(☺/ق 等)。换用中文版 FfH(`ffh2_041_o_ch`
  谱系,本机 `Mods\Fall from Heaven 2` 现装)的字模后实测恢复(左上角 HUD 确认)。MM 原字模
  留存游戏目录 `.bak-font`;若发现个别 MM 独有图标图案不对(超出 FfH 0.41 图标集的行),
  属已知代价,届时再对照原字模补行。

## 安装

把 `Assets/`、`Resource/` 复制进 `C:\Civilization4\Beyond the Sword\Mods\Magister Modmod for FfH2\` 覆盖同名文件即可。

## 地图脚本汉化(2026-07-23)

地图选择界面的介绍与自定义选项来自 `PrivateMaps/*.py`。16 个脚本走 `TXT_KEY_*`
键(`CIV4GameText_MapScriptTools.xml` 已有中文,无需处理);其余裸英文串按
"**英文原串作文本键**"方案汉化,共 411 条,全部在 `Assets/XML/Text/YKMap_GameText.xml`:

- `getDescription()` 返回值引擎会过一遍 getText——英文原句建同名键即翻译,零脚本改动
  (Erebus / ErebusContinent / WorldOfErebus / PerfectWorld2 / Totestra / MountainCoast);
- `Erebus_mst` / SmartMap 标题本就把裸串传给 getText——同法零改动;
- 不走 getText 的选项函数(EC / WoE / PW2 / PW2_mst / Totestra / SmartMap 值表 /
  MountainCoast)曾在脚本尾部追加 3 行垫片(`# YK-L10N-SHIM`,经 `YKMapText.py` 转译);
  **2026-07-23 深夜已随"地图改动全回退"指令一并撤除**——这 7 张图的自定义**选项名
  显示英文**,地图介绍不受影响仍是中文。`YKMapText.py` 与 `YKMap_GameText.xml` 保留
  在包内(前者暂无引用,后者仍服务介绍文本)。

地图在下拉框里的**名字**是文件名,引擎不查文本库,故保持英文(改名会破坏脚本引用,不做)。

## 已知限制:地图上城市横幅显示问号(2026-07-23 定案)

城市横幅(城名/在造项)是全游戏唯一"宽字符 → 按**当前语言号**选代码页转窄 → 贴图"的
渲染路径:语言 0(英语槽)用西文代码页,中文必转 `?`;只有语言 5(YK 中文槽)走 GBK 才出汉字。
2026-07-23 已在全 6 列文本状态下重测语言 5:**仍启动崩溃**——排除数据原因,确认是 MM 的
MNAI DLL 槽 5 读文本的固有缺陷。故横幅问号在当前路线下无解,属已接受的限制;
根治需从 lfgr 的 MNAI-U 源码重编 DLL 修掉槽 5 缺陷后改用 Language=5(深水区,未启动)。
其余全部界面(HUD/百科/悬浮/城市画面)不受影响,均为中文。

## 安装期 Python 修补(汉化生效后必须,直接改 MM 安装目录,各有 .bak 备份)

中文进入第 0 列后,MM 自带 Python 里两处按"文本必为 latin-1"写死的代码会炸,需就地修补:

1. **`Assets/Python/Contrib/Sevopedia/SevoPediaMain.py`**(备份 `.bak-icons`):
   `categoryGraphics` 的 `TECHS`/`BUILDINGS`/`CIVICS` 三项图标字符改为 `u""`——
   YK 日版 exe 对这三个 GameFont 符号 ID 映射非法码位,会吞掉侧栏整行文字。
2. **`Assets/python/MapScriptTools.py`**(备份 `.bak-l10n`,2026-07-23):MST 在每次
   地图生成开局的 `getModInfo` 里做"模组识别"——取 `TXT_KEY_VERSION` 等文本、按英文原文
   做字符串比对。汉化后版本串"MagisterModmod - 2023 年 10 月 20 日,基于 More Naval AI
   v2.9.1u"**既含中文又保留英文关键词**,命中 `bMNAI` 分支后执行 `modName = str(sVersion)`
   → `UnicodeEncodeError` → 生成中断 → 引擎兜底铺**全平原地图**(报错被
   `HidePythonExceptions=1`/`LoggingEnabled=0` 完全静默)。**全部 12 张 `_mst` 地图中招**;
   Erebus 等不走 MST 的图无恙。修补:4 处 `str(sVersion)` 改
   `sVersion.encode('latin_1','replace')`(CJK 安全,英文关键词保留、探测结果不变);
   另 `bBTS` 探测补上对 YK 中文"刀剑"(`u"刀剑"` 转义,源码纯 ASCII)的匹配
   ——`TXT_KEY_BTS_CIVS` 已是中文,原探测会误判非 BtS 环境。
3. **编码雷区全量清扫**(2026-07-24 凌晨,日志开启后由 PythonErr.log 实锤,8 文件各备
   `.bak-l10n`):中文单位名/城市名进入按 ASCII/latin-1 写死的代码即炸。三类修法:
   - `str(X.getName())`(RNG 日志标签,123 处:CvEventManager 52 / CvSpellInterface 52 /
     MagisterEvents 18 / CvRandomEventInterface 1)→ `.getName().encode('latin_1','replace')`
     ——标签仅作随机数日志键,中文变 `?` 无碍;此前建单位/战斗/狼化等事件必炸
     (开局即刷 onUnitCreated 异常十余条);
   - 路牌/地标 API(`addSign`/`addLandmark` 需宽字符串):CustomFunctions 独特地貌标注 3 处、
     CvEventManager WB 标牌编辑 2 处、MapScriptTools `mapSetSign`、EventSigns 存档标牌恢复
     ——一律去掉 `convertToStr`/`encode('latin_1')` 包装,直传 unicode(此前中文标注
     触发 GameStart 报错弹幕);
   - `pyWB/CvWBDesc.py` 23 处 `.encode(fileencoding)` 加 `'replace'` 兜底(WB 存档描述文件
     仍 latin-1,中文写成 `?`,不再让 writeDesc 整体失败)。
   - **第二轮(BeginGameTurn 报错实锤)**:Badb 营地漂移的路牌逻辑(CvEventManager:878、
     CvSpellInterface:18095)把 GBK 窄串与引擎宽字符串比较,Py2.4 直接抛异常——去掉
     `convertToStr` 保持 unicode;同修建筑地标(CvEventManager:2580 `addLandmark`)与
     Somnium 纸牌界面(CvCorporationScreen 10 处,GBK 串塞回 getText 参数元组必炸)。
     **观察名单**:Revolution/DynamicCivNames/BarbarianCiv 里仍有 `convertToStr` 喂
     `setName` 等宽 API 的用法,仅在开启 Revolution 系选项时触发,日志会抓,届时再修。
4. **`Assets/python/CvUtil.py` · `convertToStr`**(备份 `.bak-l10n`,2026-07-23):
   原实现 `s.encode("latin_1")` 遇中文抛 `UnicodeEncodeError`。该函数被百科升级图/晋升树
   (`UnitUpgradesGraph.py` 每条边都 `pyPrint` 单位中文名,首条即断,页面全空)、地标/路牌、
   Somnium 纸牌界面、自动存档文件名等广泛调用。修补:latin-1 失败降级 `gbk`
   (本机 ACP=936,引擎窄字符串按系统代码页还原,中文可正常显示),再兜底
   `latin_1+replace`,保证永不抛异常。
