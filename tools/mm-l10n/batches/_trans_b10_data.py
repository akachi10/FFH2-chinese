# -*- coding: utf-8 -*-
# batch-10: MM 独有黑暗奇幻 lore/图鉴。key->简体中文明文。
# 忠实原意，不发挥。LINK 标记一律剥壳保留内文（锚点 A5），译文中不含 [LINK=*]。
# 标记 [PARAGRAPH]/[PARAGRAPH:N]/[ICON_BULLET]/[NEWLINE]/[TAB]/[H1]/[\\H1]/%D1 等原样保留。
# 字面 \r\n 原样保留（英文含此转义者，中文同位置保留）。
import re

# ---- 术语表：LINK 内文 -> 中文（与项目术语表对齐，MM 新专名自拟并记录） ----
GL = {
 # 7 基础宗教/议会（项目术语表已定）
 "The Ashen Veil":"混沌之灰烬","Council of Esus":"杰斯议会","The Council of Esus":"杰斯议会",
 "The Empyrean":"天空的教诲","The Order":"绝对秩序","Fellowship of Leaves":"绿叶之友",
 "The Fellowship of the Leaves":"绿叶之友","Runes of Kilmorph":"基鲁莫夫之痕","The Runes of Kilmorph":"基鲁莫夫之痕",
 "Octopus Overlords":"深渊霸主","The Undertow":"暗流","The Overcouncil":"至高议会","The Undercouncil":"影子议会",
 # MM 新增宗教（自拟）
 "The Ringgivers":"授环者","The Unblemished":"无瑕者","The Brotherhood of Wardens":"守望者兄弟会",
 "Brotherhood of Wardens":"守望者兄弟会","The House of Plenty":"丰饶之家","The Grey Council":"灰色议会",
 "The Ember Legion":"余烬军团","The Matronae":"圣母会","The White Hand":"雪之手",
 "The Sons of Discord":"纷争之子","The Stewards of Inequity":"不义之仆","Stewards of Inequity":"不义之仆",
 "The Anointed":"受膏者","The Laeran Cord":"莱兰之缚","Laeran Cord":"莱兰之缚","The Eternal Cabal":"永恒结社",
 "Cult of the Dragon":"巨龙教团","The Between":"夹隙","Ceridwen's Coven":"塞丽德温的女巫团",
 "The Children of The One":"独一之子","The Foxmen":"狐人","Foxmen":"狐人","The Anointed ":"受膏者",
 # 法术球/mana
 "Sun Mana":"太阳能量","Shadow Mana":"暗影能量","Spirit Mana":"精魂能量","Body Mana":"肉身能量",
 "Enchantment Mana":"附魔能量","Dimensional Mana":"位面能量","Life Mana":"生命能量","Nature Mana":"自然能量",
 "Death Mana":"死亡能量","Ice Mana":"寒冰能量","Creation Mana":"创造能量","Entropy Mana":"熵变能量",
 "Law Mana":"律法能量","Chaos Mana":"混沌能量","Earth Mana":"大地能量","Air Mana":"气流能量",
 "Water Mana":"水流能量","Fire Mana":"烈焰能量","Mind Mana":"心灵能量","Force Mana":"力场能量",
 "Meta Magic Mana":"元魔法能量","Body":"肉身","Undeath":"不死","Mind":"心灵","Shadow":"暗影",
 # 改良/设施/地貌
 "Mirror of Heaven":"天堂之镜","Spire of the Sun":"太阳尖塔","Citadel of Light":"光辉堡垒",
 "Citadels of Light":"光辉堡垒","Tower":"塔","Hallowed Ground":"圣化之地","Pool of Tears":"泪之池",
 "Bradeline's Well":"布拉迪来因之井","Grigi Abattoir":"格里吉屠场","Clockwork City":"发条之城",
 "Workshops":"作坊","Citadels":"堡垒","Tapestry House":"织锦之屋","Portals":"传送门","Portal":"传送门",
 "Yggdrasil":"世界树","Tomb of Sucellus":"苏塞鲁斯之墓","Herve's Mausoleum":"埃尔夫陵墓","Camps":"营地",
 "New Forests":"新生森林","Forests":"森林","Ancient Forests":"远古森林","Burnt Forests":"焦林",
 "Temple of Atonement":"赎罪神殿","Castles":"城堡","Forts":"堡垒工事","Carnivean's Craig":"卡尼维安峭壁",
 "Standing Stones":"立石","Mines":"矿场","Quarries":"采石场","Majen's Worskshop":"玛真的作坊",
 "Enclaves":"聚居地","Cave of the Ancestors":"先祖洞窟","the Cave of the Ancestors":"先祖洞窟",
 "Remnants of Patria":"帕提亚遗迹","the Remnants of Patria":"帕提亚遗迹","Ruins":"废墟","City Ruins":"城市废墟",
 "Seven Pines":"七松","the Seven Pines":"七松","Rings of Warding":"守护之环","Ring of Warding":"守护之环",
 "Maelstrom":"大漩涡","Windmills":"风车","Wode's Oak":"沃德橡树","Whispering Wood":"低语之林",
 "Aifon Isle":"艾冯岛","Fishing Boats":"渔船","Whaling Boats":"捕鲸船","Ring of Carcer":"卡瑟牢环",
 "Pyre of the Seraphic":"炽天焚坛","Graveyards":"墓地","the Broken Sepulchur":"破碎墓穴","Broken Sepulchur":"破碎墓穴",
 "Grave of Asmoday":"阿斯莫代之墓","the Grave of Asmoday":"阿斯莫代之墓","Pits of Torment":"折磨之坑",
 "Hellfire":"地狱之火","Necrototem":"死灵图腾","Tormented Souls":"受折磨的灵魂","Entropy Node":"熵变节点",
 "Chancel of the Guardians":"守护者祭室","Odio's Prison":"欧迪奥监牢","Jeteye":"杰特眼","Sanctify":"净化",
 "Snake Pillars":"蛇柱","Obsidian Plains":"黑曜石平原","Grigi Abattoir ":"格里吉屠场",
 # 地形
 "Desert":"沙漠","desert":"沙漠","Peaks":"山峰","Ice":"冰原","Glacier":"冰川","Wasteland":"荒原",
 "Tundra":"苔原","Glaciers of Gloom":"幽暗冰川","Fields of Perdition":"堕落之野","Broken Lands":"破碎之地",
 "Burning Sands":"燃烧之沙","Seas of Sorrows":"悲痛之海","Oceans of Despair":"绝望之洋","Coasts":"海岸",
 "Oceans":"海洋","Plains":"平原","Grasslands":"草原","Blizzards":"暴风雪","Sea Ice":"海冰","Scrub":"灌丛",
 "Flood Plains":"泛滥平原","Jungles":"丛林","Flames":"火焰","Smoke":"烟雾",
 # 资源
 "Wine":"葡萄酒","Grapes of Wrath":"愤怒之葡萄","Sheep":"绵羊","Pigs":"猪","Toads":"蟾蜍","Horses":"马匹",
 "Cows":"牛","Nightmares":"梦魇兽","Cotton":"棉花","Silk":"丝绸","Razorweed":"剃刀草","Bananas":"香蕉",
 "Sugar":"甘蔗","Gulagarm":"古拉加姆","Marble":"大理石","SHEUT_STONE":"舍乌特石","Sheut Stone":"舍乌特石",
 "Corn":"玉米","Wheat":"小麦","Rice":"稻米",
 # 单位/晋升/文明/科技/法术
 "Angel":"天使","Angels":"天使","Blessed":"受福","Crown of Brilliance":"辉光之冠","Demon":"恶魔",
 "Demons":"恶魔","Demon Possessed":"恶魔附身","Unholy Taint":"邪秽","Kanna's Whip":"卡娜之鞭",
 "Manes":"恶灵","Warriors":"战士","Drown":"溺死","Grey":"灰化","Hidden":"隐匿","Immortality":"不朽",
 "Shade":"影灵","Wane":"衰隐","Eremite":"隐修","Morale":"士气","Arcane":"魔法","Summoner":"召唤大师",
 "Sundered":"咒刻","Stigmata":"圣痕","Twincast":"双重施法","Spell Extension I":"法术延展 I",
 "Spell Extension II":"法术延展 II","Vampiric":"吸血","Vampire Lords":"吸血鬼领主","Brujah":"狂暴吸血鬼",
 "Brood Guards":"血族卫士","Losha Valas":"吸血鬼萝莎·瓦拉斯","Moroi":"血族战士","Feeding":"吸食",
 "Feasting":"盛宴","Gift Vampirism":"赐予吸血","Governor's Manor":"总督宅邸","Governor's Manors":"总督宅邸",
 "Feudalism":"封建制","Divine Essense":"神圣本质","Way of the Wise":"智者之道","Honor":"荣誉","Varn":"范恩",
 "Amurites":"阿姆莱特学院","Balseraphs":"巴尔塞拉弗族","Bannor":"班诺尔联邦","Calabim":"卡拉比姆公国",
 "Clan of Embers":"余灰部落","Doviello":"多维洛部落","Elohim":"埃洛希姆守护者","Grigori":"格利高里族",
 "Hippus":"希普斯佣兵国","Illians":"伊利安遗族","Infernal":"地狱军团","Infernals":"地狱军团","Khazad":"卡扎德王国",
 "Kuriotates":"库里奥塔特","Lanun":"拉努恩海盗","Ljosalfar":"勒约沙尔法","Luchuirp":"鲁崔尔普矮人部族",
 "Malakim":"马拉基姆游牧民","Mercurians":"天界军团","Sheaim":"塞安隐修会","Sidar":"希达永生者","Svartalfar":"斯瓦塔尔法",
 "Planar Gates":"位面之门","Armageddon Counter":"末日审判计数器","Hell Terrain":"地狱地形",
 "Arcane Lacuna":"魔法空白","Revelry":"狂欢","Rally":"集结","River of Blood":"血河","For the Horde":"为了部落",
 "Wild Hunt":"狂野狩猎","Sanctuary":"庇护","Ardor":"炽热","Warcry":"战吼","Stasis":"停滞",
 "Mother Lode":"富矿脉","Legends":"传奇","Raging Seas":"怒海","March of the Trees":"林木进军",
 "Gifts of Nantosuelta":"南托苏尔塔的馈赠","Religious Fervor":"宗教狂热","Divine Retribution":"神罚",
 "Worldbreak":"碎世","Into the Mist":"遁入迷雾","Veil of Night":"夜之帷幕","magic":"魔法",
 "Last Days":"末日将至","No Hell Terrain":"无地狱地形",
}
# 排序：先长后短，避免子串误替换
_KEYS = sorted(GL.keys(), key=len, reverse=True)

def strip_links(s):
    """[LINK=X]inner[\\LINK] -> 术语表映射(inner) 中文；其余标记原样。"""
    def repl(m):
        inner = m.group(1).strip()
        return GL.get(inner, GL.get(inner.strip(), inner))
    # 文件中闭合标记为双反斜杠 [\\LINK]（源字节两个反斜杠）
    return re.sub(r'\[LINK=[^\]]*\]([^\[]*)\[\\\\LINK\]', repl, s)

T = {}

# ============ 短条目 / 名称 ============
T["TXT_KEY_BUILDING_TOPHET"]="陀斐特"
T["TXT_KEY_BUILDING_TOPHET_HELP"]="[ICON_BULLET]赋予部分在此训练的单位火焰抗性"
T["TXT_KEY_BUILDING_SCHOOL_OF_SADISM"]="施虐学院"
T["TXT_KEY_BUILDING_SHRINE_OF_SIRONA_HELP"]="[ICON_BULLET]允许你每回合治疗你的一个单位。[NEWLINE][ICON_BULLET]在守望者兄弟会下花费减半"
T["TXT_KEY_BUILDING_SANGUINE_FOUNTAIN"]="血泉"
T["TXT_KEY_BUILDING_SANGUINE_FOUNTAIN_HELP"]="[ICON_BULLET]若敌方在别处建造它，则会消失[NEWLINE][ICON_BULLET]圣城地位随此奇观而增减。[NEWLINE][ICON_BULLET]只能在交战时建造[NEWLINE][ICON_BULLET]当你的战争结束时被摧毁"
T["TXT_KEY_BUILDING_ARCHIVE"]="档案馆"
T["TXT_KEY_BUILDING_CIRCLE_OF_CONJURERS"]="召唤法阵"
T["TXT_KEY_BUILDING_ARTIFICERY"]="造物工坊"
T["TXT_KEY_BUILDING_TEMPLE_GREY_COUNCIL"]="议决堂"
T["TXT_KEY_SPELL_FOUND_TRAILHEAD"]="建造启程点"
T["TXT_KEY_BUILDING_TEMPLE_FOXMEN"]="启程点"
T["TXT_KEY_BUILDING_TEMPLE_ANOINTED"]="屠场"
T["TXT_KEY_BUILDING_INTERSTICE"]="间隙"
T["TXT_KEY_BUILDING_AGORA"]="集市广场"
T["TXT_KEY_BUILDING_GALLERY"]="画廊"
T["TXT_KEY_BUILDING_PIXIE_GARDEN"]="精灵花园"
T["TXT_KEY_BUILDING_FREE_PROMOTION_PICK_RANGE"]="[ICON_BULLET]单位起始便带有 %D1 至 %D2 个免费晋升"
T["TXT_KEY_BUILDING_TEMPLE_OF_THE_OVERLORDS"]="暗流神殿"
T["TXT_KEY_BUILDING_TEMPLE_OF_THE_OVERLORDS_HELP"]="[ICON_BULLET]战士可在暗流神殿被献祭，化为溺死。"
# 城市名（音译，MM 独有）
T["TXT_KEY_CITY_NEW_MULYR"]="新穆利尔"
T["TXT_KEY_CITY_BALSERAPHS_21"]="微光之家废墟"
T["TXT_KEY_CITY_BALSERAPHS_22"]="新微光之家"
T["TXT_KEY_CITY_BANNOR_22"]="阿德丁"
T["TXT_KEY_CITY_CALABIM_17"]="莫近城堡"
T["TXT_KEY_CITY_CALABIM_18"]="羔羊堡"
T["TXT_KEY_CITY_CALABIM_19"]="灰烬门"
T["TXT_KEY_CITY_CALABIM_20"]="新烛速城"
T["TXT_KEY_CITY_INFERNAL_31"]="塔尔塔罗"
T["TXT_KEY_CITY_INFERNAL_32"]="盖·本-欣嫩"
T["TXT_KEY_CITY_INFERNAL_33"]="哲汉纳姆"
T["TXT_KEY_CITY_INFERNAL_34"]="哈维亚"
T["TXT_KEY_CITY_INFERNAL_35"]="哲希姆"
T["TXT_KEY_CITY_INFERNAL_36"]="萨卡尔"
T["TXT_KEY_CITY_INFERNAL_37"]="胡塔玛"
T["TXT_KEY_CITY_INFERNAL_38"]="纳尔"
T["TXT_KEY_CITY_INFERNAL_39"]="韦勒"
T["TXT_KEY_CITY_INFERNAL_40"]="阿勒阿扎卜"
T["TXT_KEY_CITY_INFERNAL_41"]="纳提"
T["TXT_KEY_CITY_INFERNAL_42"]="哈特玛"
T["TXT_KEY_CITY_INFERNAL_43"]="萨阿"
T["TXT_KEY_CITY_INFERNAL_44"]="措阿·罗塔哈特"
T["TXT_KEY_CITY_INFERNAL_45"]="斯科托斯·托·埃克索特隆"
T["TXT_KEY_CITY_INFERNAL_46"]="克劳斯莫斯"
T["TXT_KEY_CITY_INFERNAL_47"]="布鲁格莫斯·顿·奥东顿"
T["TXT_KEY_CITY_INFERNAL_48"]="普尔·托·艾奥尼翁"
T["TXT_KEY_CITY_INFERNAL_49"]="利姆嫩·图·普罗斯"
T["TXT_KEY_CITY_INFERNAL_50"]="普尔·托·阿贝斯顿"
T["TXT_KEY_CITY_INFERNAL_51"]="斯科耶克斯·胡·特柳塔"
T["TXT_KEY_CITY_INFERNAL_52"]="库隆"
T["TXT_KEY_CITY_INFERNAL_53"]="贝布莱泰"
T["TXT_KEY_CITY_INFERNAL_54"]="阿波莱塞·顿·米斯顿"
T["TXT_KEY_CITY_INFERNAL_55"]="阿拉夫"
T["TXT_KEY_CITY_INFERNAL_56"]="阿达卜·阿勒-卡布尔"
T["TXT_KEY_CITY_INFERNAL_57"]="菲特纳"
T["TXT_KEY_CITY_INFERNAL_58"]="塔·卡托特拉"
T["TXT_KEY_CITY_INFERNAL_59"]="塔·卡托塔塔"
T["TXT_KEY_CITY_INFERNAL_60"]="夫拉克"
T["TXT_KEY_CITY_LANUN_15"]="沉没沼泽"
T["TXT_KEY_CITY_LANUN_17"]="劳鲁斯湾"
T["TXT_KEY_CITY_MERCURIANS_18"]="阿勒-基亚玛"
T["TXT_KEY_CITY_SHEAIM_21"]="阿勒-巴尔扎赫"
T["TXT_KEY_CITY_SIDAR_21"]="奥蒂乌姆"
# civ help（LINK 已剥壳）
T["TXT_KEY_CIV_DOVIELLO_HELP"]="近战单位可在任意地点升级，并可使用挑战能力与彼此交战，而非只能与敌方交战"
