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

# ============ civ HELP（LINK 剥壳） ============
T["TXT_KEY_CIV_INFERNAL_HELP"]="当邪恶单位死亡时获得恶灵。[NEWLINE][ICON_BULLET]城市起始便拥有免费建筑与混沌之灰烬宗教[NEWLINE][ICON_BULLET]城市逐渐蔓延地狱地形[NEWLINE][ICON_BULLET]地狱契约仪式允许玩家随机召唤一位地狱领袖，并可选择切换控制这个新玩家。它总共可使用 7 次，但每个团队仅限 3 次[NEWLINE][ICON_BULLET]地狱军团通过占领存在混沌之灰烬宗教的最佳可用敌方城市进入世界。否则，其单位会被放置在一处带有地狱之火设施的随机地块上。"
T["TXT_KEY_CIV_MALAKIM_HELP"]="独处于沙漠中的信徒获得隐修晋升，提升其被动经验获取以及作为施法者的强度。[NEWLINE][ICON_BULLET]范恩可在智者之道时创立天空的教诲，而无需荣誉"
T["TXT_KEY_CIV_MERCURIANS_HELP"]="每当善良单位死亡时获得天使。[NEWLINE][ICON_BULLET]地狱地形在本文明领土内消退得更快[NEWLINE][ICON_BULLET]开启天界之门能力（可在含有天界之门的城市中使用）会将这位巴希姆作为队友召唤出来，并授予切换控制这个新玩家的选项[NEWLINE][ICON_BULLET]巴希姆单位是领袖的化身，该单位死亡时会失去其特性[NEWLINE][ICON_BULLET]一旦巴希姆被杀，另一位玩家可使用召唤天界援军能力（需要天界之门）率一支天使大军将他带回。它还授予与他之间的和平及外交加成。[NEWLINE][ICON_BULLET]混沌之灰烬与暗流宗教会自动从天界军团城市中移除"
T["TXT_KEY_CIV_SIDAR_HELP"]="灰化者是那些已开始衰隐之人，他们运用曾为精灵者从冥界偷带出的一种仪式。这份“阿劳恩的馈赠”实为拉罗斯的陷阱，随着单位升级，他会攫取更大份额的灵魂。当他们能够在 7 级购买不朽（凭借神圣本质的知识）之时，死后已再无机会化为天使或恶魔。该种族特性还赋予死亡伤害抗性，提升脱离战斗的几率，并可能随机赋予隐匿。它阻断不死魔法与士气。7 级时，灰化单位可完成衰隐仪式化为影灵，作为伟人在城市中定居。希达宫殿提升所有专家（包括定居的伟人），并使本国领土内（但城市之外）的任何单位隐形，直到它们选择显形。希达首都不会通过大使馆向其他玩家揭示，其当前视野也不会通过至高议会共享地图决议或耳目网络与其他玩家共享。"
# ============ 政策 HELP/STRATEGY（LINK 剥壳） ============
T["TXT_KEY_CIVIC_ARETE_HELP"]="[ICON_BULLET]允许在山峰上建造矿场与采石场[NEWLINE][ICON_BULLET]需以基鲁莫夫之痕或授环者作为国教"
T["TXT_KEY_CIVIC_ARETE_STRATEGY"]="需以基鲁莫夫之痕或授环者作为国教。"
T["TXT_KEY_CIVIC_SLAVERY_STRATEGY"]="有 25% 几率将被击败的活体单位俘为奴隶[NEWLINE]可能被某项至高议会决议阻止"
T["TXT_KEY_CIVIC_GUARDIAN_OF_NATURE_STRATEGY"]="需以绿叶之友或无瑕者作为国教。"
T["TXT_KEY_CIVIC_OVERCOUNCIL_HELP"]="[ICON_BULLET]需要已创立天空的教诲[NEWLINE][ICON_BULLET]与杰斯议会国教不兼容[NEWLINE][ICON_BULLET]为你提供与其他至高议会成员的大使馆"
T["TXT_KEY_CIVIC_SOCIAL_ORDER_STRATEGY"]="需以绝对秩序或受膏者作为国教。[NEWLINE]此政策提升帝国的军事生产、来自倡导律法建筑的幸福，以及驻扎在城市中的军事单位。"
T["TXT_KEY_CIVIC_SACRIFICE_THE_WEAK_STRATEGY"]="此项不再需要以混沌之灰烬作为国教，但仅对邪恶玩家开放。此政策允许玩家在不采用混沌之灰烬国教的情况下进行地狱契约仪式"
T["TXT_KEY_CIVIC_SACRIFICE_THE_WEAK_HELP"]="[NEWLINE][ICON_BULLET]将每点人口的食物消耗减半[NEWLINE][ICON_BULLET][ICON_BULLET]允许玩家即便不采用混沌之灰烬国教也能进行地狱契约仪式"
T["TXT_KEY_CIVIC_UNDERCOUNCIL_HELP"]="[ICON_BULLET]需要已创立杰斯议会[NEWLINE][ICON_BULLET]与天空的教诲国教不兼容[NEWLINE][ICON_BULLET]为你提供与其他影子议会成员的大使馆"
# ============ DISCOUNT HELP（LINK 剥壳） ============
T["TXT_KEY_DISCOUNT_ANOINTED_HELP"]="[ICON_BULLET]在受膏者下花费减半"
T["TXT_KEY_DISCOUNT_BROTHERHOOD_OF_WARDENS_HELP"]="[ICON_BULLET]在守望者兄弟会下花费减半"
T["TXT_KEY_DISCOUNT_CHAIN_BREAKERS_HELP"]="[ICON_BULLET]在塞丽德温的女巫团下花费减半"
T["TXT_KEY_DISCOUNT_CULT_OF_THE_DRAGON_HELP"]="[ICON_BULLET]在巨龙教团下花费减半"
T["TXT_KEY_DISCOUNT_FOXMEN_HELP"]="[ICON_BULLET]在狐人下花费减半"
T["TXT_KEY_DISCOUNT_LAERAN_CORD_HELP"]="[ICON_BULLET]在莱兰之缚下花费减半"
T["TXT_KEY_DISCOUNT_STEWARDS_OF_INEQUITY_HELP"]="[ICON_BULLET]在不义之仆下花费减半"
T["TXT_KEY_DISCOUNT_UNBLEMISHED_HELP"]="[ICON_BULLET]在无瑕者下花费减半"
T["TXT_KEY_EFFECT_TAINT_HELP"]="[ICON_BULLET]将活体单位打入地狱的来世[NEWLINE][ICON_BULLET]腐蚀单位所在地块，依单位等级与末日审判计数器而定的速率，将其缓慢转化为地狱地形"
T["TXT_KEY_EQUIPMENT_ANGELORUM_CAVEA"]="天使囚笼"
# damage 简短
T["TXT_KEY_DAMAGE_PSYCHIC"]="心灵"
T["TXT_KEY_DAMAGE_PSYCHIC_DAMAGE"]="心灵伤害。"
T["TXT_KEY_DAMAGE_PSYCHIC_TAG"]="心灵"
T["TXT_KEY_CONCEPT_PUPPET_STATES"]="傀儡国"
T["TXT_KEY_CONCEPT_REVOLUTIONS"]="革命"

# ============ 叙事 lore PEDIA（忠实原意，LINK 剥壳） ============
T["TXT_KEY_BUILDING_SLYPH_SEARCH_PEDIA"]="狐人钟爱他们的探险。一股压倒一切的漫游欲驱使他们寻找任何借口踏上一场宏大的冒险。目标往往完全无关紧要，常常在旅程早期便被遗忘。然而，鲜有人愿意放弃与塔莉最美的造物之一寻得真爱的梦想。[PARAGRAPH]西尔芙是美丽的气之精灵，据说曾有人放弃她们在风与云间永恒的舞蹈，下嫁凡间男子。她们飘忽本性中唯一始终如一的，便是对配偶的忠贞，那配偶必将被赐予一段幸福的婚姻。但她们的子嗣，虽常常聪慧而富有创造力，却往往连续数代不安分而惹是生非。许多人猜测，塔莉创造西尔芙正是为了把这种秉性繁育进人类之中。"
T["TXT_KEY_BUILDING_TOPHET_PEDIA"]="巴尔教会没有多少能长久存续的结构。取而代之的是宗教剧变的爆发，大批狂热的追随者揭竿而起，反抗当地任何被声讨的事物。缘由并不如那股狂热、巴尔的祝福，以及叛乱随之而来的暴力那般重要。巴尔的大多数崇拜者会接受她印记的烙印，永远灼烧、施加痛楚。巴尔亦被称为烈焰女王与坠落之星。[PARAGRAPH]圣裁审判庭在第二次叛乱后组建，以清除帕提亚的腐败。这是一场献身于巴尔的运动，充满了挥舞金色炽天圣火的祭司、暴动者与审判官。此火能焚烧恶魔之躯、破除法术。巴希姆加入了圣裁审判庭，卡西尔则为战争中流离失所的难民建起了家园。虽然基洛林与叛乱最强大的敌人决斗，但真正在帕提亚各处打了上百场战役的是圣裁审判庭。[PARAGRAPH]在这些战役中，一些最虔诚的审判官经受了无烟之火仪式。他们跪下向巴尔祈祷，祈求胜利，祈求特许议会的覆灭，并献出自己的生命作为祭品，好让他们守护所爱之人。然后他们引火自焚。真正虔诚者会被七伊夫利特之一附身——那是无形的真天使，是巴尔的化身。他们在战场上化为小小的炽亮流星，免疫黑暗魔法，横扫敌阵，直至引爆造成更大破坏。尝试此仪式者中，只有一小部分会被伊夫利特附身，但成功者能扭转战局。[PARAGRAPH]在当今时代，巴尔教会被称为余烬军团。其成员大多是余灰部落的兽人。他们仍旧奉行自焚，尽管伊夫利特已鲜少以他们为宿主或降福于他们；他们也以将俘虏及自己的子女献祭于圣火而著称。"
T["TXT_KEY_BUILDING_SCHOOL_OF_SADISM_PEDIA"]="当一个灵魂从血野越入祈求神殿，混乱便告终结。阿隆的密库是为了训练恶魔掌握它们在厄瑞玻斯所需的一切技艺而设。它可被视为一座宏大的学院，但更贴切的说法是它是一座宏大的神殿。恶魔在此学习战斗、说谎与引导力量。它们学习伟大的欺瞒之术，学习臣服于上级。通过这番训练，它们成为地狱等级体系的一部分——既是祭司，也是战士、指挥官与士兵。许多恶魔作为训练的一部分，被派往厄瑞玻斯执行使命。小恶魔是训练早期的学徒。厄瑞玻斯许多有智慧的恶魔正处于此地训练的某个阶段。那些已越过此密库者，是被处理过的灵魂中最稀有、最强大的——恶魔领主与亲王。[PARAGRAPH]偶尔，特别邪恶的祈求者（法阵祭司等）会跳过所有较早的阶段，直接从阿隆的密库开始，准备受训。然而，直升阿隆密库最简便的途径，便是从施虐学院毕业。"
T["TXT_KEY_BUILDING_DIES_DIEI_PEDIA"]="天空的教诲曾是那缓缓沉入黑暗的帕提亚中最强大的向善之力。尽管它献身于罗格斯，至高议会却拥有来自所有神圣宗教的成员。它是帕提亚境内唯一能真正违抗特许议会的力量；天使们伫立在昼中之昼的城墙上。[PARAGRAPH]虽然曾有诸多阴谋企图颠覆这座城市与至高议会，却无一得逞。使它走向覆灭的，是那无尽的长夜。[PARAGRAPH]黑夜强化了幽暗王座。它强化了吸血鬼、狼人，以及那些被太阳逼回世界阴暗角落的生物。它削弱了罗格斯的天使，以及每个黎明受赐福的祭司。[PARAGRAPH]但那并非导致覆灭之因。是恐惧。[PARAGRAPH]第一个未至的黎明在昼中之昼引发了恐慌。至高议会试图劝导众人保持谨慎、祈祷与共融。但到第三天，他们已无力维持控制。骑手们纵马奔出城，去入侵尘埃公国——一切邪恶之事都被归咎于它（而它也常常确有其罪）。城中民众因惧怕即将到来的饥荒，开始为资源彼此争斗。[PARAGRAPH]阴影大天使伊阿古斯住在城外一处小农庄，佯装隐士与叛教者。他招来邻人的愤恨，当他们前来与他对质时，在他家中与地窖里发现了他们相信用于黑暗魔法的物件。[PARAGRAPH]伊阿古斯被捕，他却不停地诅咒任何靠近他的人。他被拖过城市时对着全城尖叫，说他们活该迎来那正朝他们逼近的黑暗。许多人相信正是伊阿古斯造成了这无尽长夜，他因束缚太阳、诅咒大地而被囚。[PARAGRAPH]城中的恐慌一时消退，全城转而归咎于伊阿古斯。城市要求速审、定罪并处决他。[PARAGRAPH]他在至高议会的地牢中被关了三天。一天天过去，民众对正义的呼声愈发急切。每一个太阳未升的日子，他们都哭喊着说，杀死伊阿古斯是阻止这一切的唯一办法。[PARAGRAPH]伊阿古斯在至高议会面前受审。审判只持续了一天。到最后，至高议会明白了真相：他确是个可怕的人，但他并未犯下被指控之罪。他没有造成黑暗。这真相在他们的审判中始终被昭示给他们，他们也一向遵从它。[PARAGRAPH]但全城已团结一致。抗议者即将冲击天空的教诲，他们要见血。至高议会反复商议，编造理论，寻找借口。他们对自己说，或许他们也如太阳一般被蒙蔽了。或许他有罪，纵然他们心中罗格斯的声音低语着并非如此。[PARAGRAPH]他们宣判他有罪。在本该是夜最深处的时刻，他们在城市中心将他处决。他脸上最后的神情是一个微笑。就在那一刻，罗格斯的神赐之力失落了，天使们逃离了昼中之昼。[PARAGRAPH]随后他们朝东方凝望，等待黎明降临。可当那时刻来临，太阳没有升起。取而代之的是马蹄声响彻全城。司夜的骑手，漆黑而缥缈，径直冲过城墙。他们闪烁的利剑无视钢铁与磐石，轻易割穿血肉。昼中之昼的居民究竟遭遇了什么，无人知晓。直到太阳重返造化多年之后，城门才再度开启，而当它开启时，城中已空无一人。"
T["TXT_KEY_BUILDING_SANGUINE_FOUNTAIN_PEDIA"]="这座名副其实的血之泉，为荣耀真正的血泉——百臂之神、战争与混沌之神卡穆洛斯本尊——而造。它只能在交战时建造，一旦其主人停止发动战争，泉便不再涌流。"
T["TXT_KEY_BUILDING_TEMPLE_OF_TEMPORENCE_PEDIA"]="[TAB]节制神殿是一座宏伟的圣殿，矗立在“希奥之岛”上。据说此地是造化的第一处所在，其控制权曾在众多国家与众多信仰之间几度易手。当前的建筑建在献给每一位神祇的神殿废墟之上，并融入那些废墟的元素，以平等地荣耀每一位神。据说这座建筑的恢弘，是凡人之眼所见过的最接近真天堂之物。正是在此，灰色议会的裁决者们聚首，裁定最严重的争端，颁布他们最具约束力的敕令。"
T["TXT_KEY_BUILDING_TEMPLE_GREY_COUNCIL_PEDIA"]="[TAB]怀恩领你走进达格达的神殿。里面你看见一座教堂的长椅，但在它们前方有一处台座，台座之前，一方高起的坛上立着七把巨大的宝座。这看上去是个举行审判、进行裁决之处，而非布道之所。[PARAGRAPH]这里有更多审判官把守，几间侧室，一段通往钟楼的楼梯，以及一间供审判官聚首商议判决的教士室。怀恩领你越过这一切，来到一间后室，一道石阶自那里通向下方的一间贮藏室。[PARAGRAPH]或者说，那曾是间贮藏室。除了两根巨大的支柱，一切都被清空。四名审判官立于此地，从香炉中焚香，低声祈祷。他们环绕着室中第五个身影——那身影被锁链缚在两柱之间。[PARAGRAPH]布里昂娜跪在石地上。她浑身肮脏，头发厚厚地纠结贴在头上。她的衣衫是一团污秽不堪的狼藉。你进来时她并未抬头，只是一动不动地盯着地面。这里弥漫着一股令人作呕的圣香与人类排泄物的混合气味。"
T["TXT_KEY_BUILDING_TEMPLE_FOXMEN_PEDIA"]="狐人以其漫游欲而闻名。他们无法忍受长久停留一处。他们没有定居的祭司团，也没有真正的神殿，但在厄瑞玻斯最偏远、最危险的地方散落着形形色色的圣所。什么使一处所在对塔莉而言神圣，往往并不明显。许多狐人会加入前往对其他神祇更为神圣的独特景观的朝圣。有人说目的地完全无关紧要，只不过是冒险的一个借口罢了。狐人倾向于避开拥挤的城市，但即便是他们，也会在城镇外围既有的启程点聚集，为漫长的旅程做准备。"
T["TXT_KEY_BUILDING_PIXIE_GARDEN_STRATEGY"]="库里奥塔特那些庞大的城市枢纽无法从千窟之城奇观中获益，因此它们转而得以建造精灵花园。这提升健康与幸福，但更重要的是，它允许训练精灵——精灵原本只能由拥有创造亲和的法师召唤。"
T["TXT_KEY_BUILDING_TEMPLE_OF_THE_OVERLORDS_PEDIA"]="[TAB]它静卧于神殿的核心，是珍珠与珊瑚的奇异混合体，一件被暗流之力触碰过的造物。它是活的，不断地泛起涟漪，如同暴风中的海面泛起涟漪，我们能在心中听见它的涟漪——那远方波涛的乐音。从我看见它的那一刻起，我就知道我不该来：可我内心另一部分却在欢欣，被它的诱惑吸引，如同飞蛾扑火。[PARAGRAPH:1]祭司们在每周之初举行集会，向所有人开放。新来者需被领往那间有珊瑚的密室，而我们其余人都识得路径，即便是只来过一次的人。从我们踏入神殿周遭的那一刻起，便能感到波涛微弱的低语，引我们走向神殿的核心。我们靠近时，外来者总感到不安，说不清缘由，只在下意识里察觉我们肩头那轻微的摆动——我们的身体正接上这密室的节律。[PARAGRAPH:1]我们会围着珊瑚起舞、欢笑、庆祝，看见一个如今已沉入海底的辽阔王国的奇异幻象。随着时辰流逝，舞蹈会越来越快，乐音会越来越响。只不过那乐音只在我们脑中，是一场令人陶醉、比任何甘露都更甜美的风暴。我们醉倒在珊瑚之下，愿意做任何事，那些夜里不止一个孩子是与全然的陌生人所孕育。有时祭司们会加入我们的庆祝，但大多数时候他们只是站在一旁，注视着，等待着。[PARAGRAPH:1]那些夜晚总让我精疲力竭，在我漠视身体的极限之后，它痛楚不堪。我担心自己走得太远——每年都有人死于力竭——偶尔我也试着远离。可波涛的乐音总会在我的梦中萦绕，一段微弱的曲调卡在我脑海里，恼人地就差那么一点、轻得听不真切。而在一个美妙的神殿之夜后我会有的那些幻象啊！我是个诗人、一个艺术家，没有什么能比这更令我灵感迸发，没有什么能与我聆听珊瑚之后所作的诗篇相比。究竟更多是为了我自己还是我的艺术，我说不清，但过一阵子我总发现自己又回去了。[PARAGRAPH:1]在我一次格外漫长的缺席后归来时，一位女祭司似乎对我起了特别的兴趣。她从不说什么，但我跳舞时能感到她的目光落在我身上，若有所思。我偶尔会瞥见她与旁人低声商议着什么，尽管我从未听清任何确切的字句。[PARAGRAPH:1]这样过了几个夜晚之后，乐音中的某种东西以一种前所未有的方式令我癫狂。我的舞蹈狂野，我的幻象狂热，随着夜的推进，我的身体在愈演愈烈的剧痛中嘶喊。我能看见其他人渐渐疲惫、离去，可我无法让自己停下，无法离开那突然间仿佛只为我一人歌唱的珊瑚。从其他人的舞姿中，我看得出他们听见的并非我所听见的曲调：他们的节律与舞步全然错乱。所以他们离去时我不理会他们，因为我知道他们对我所听见的真正乐音充耳不闻。[PARAGRAPH:1]随后，当只剩她与我独处时，那女祭司走来，加入了我的舞蹈。她的舞蹈完美无瑕，与波涛全然和谐，我望着她，被我骤然在她身上看见的美所迷醉。我试图模仿她的优雅，但我自己的笨拙于我而言昭然若揭——她却似乎并不介意，因为她只是微笑。她握住我的手，仍旧微笑着，领我离开珊瑚，来到神殿中我从未涉足的一隅。我全然无视周遭——珊瑚的迷醉与她关注所带来的愉悦相比不值一提，每当她望向我，我周身的每一块肌肉都会颤栗。我沉沦于她，她身躯的每一处细节都像一道我永远无法攀出的辽阔深谷。[PARAGRAPH:1]当我们来到那水池、她将我推入水中时，反抗从未闪过我的脑海。我感到有什么攫住我的手臂和双腿，将我往下拖，可女祭司朝我微笑，她的欢愉是我唯一在意之事。我张口想为她唱一首赞歌，直到那时我才意识到自己身在水下，水灌满了我的口与肺。有那么短暂的一瞬，恐慌攫住了我，打破了魔咒——我尖叫起来，女祭司却只是报以微笑。[NEWLINE][NEWLINE][NEWLINE][TAB]那女祭司仍朝我微笑，带着一种奇异而愉悦的神情，我很难解读。溺水之后，思考变得艰难。杀戮要容易得多——杀那些女祭司命我去杀的人。[PARAGRAPH:1]有那么一刻，当我砸碎女祭司命我杀的第一批人的头骨时，我以为自己感到了一段遥远的记忆。她定是看出了我的困惑，因为她用天使般的嗓音笑了。她眼中闪着欢快的光，告诉我，我脚边的尸体是我妻子与孩子们的。我看看她，又看看那些尸体，又一次有了短暂的、忆起什么的感觉，可那些话对我毫无意义。我看着尸体，耸了耸肩，我们便离去，她的欢愉在我耳畔回响。[PARAGRAPH:1]如今，我是那女祭司的护卫。只要她对我满意，波涛的乐音便永不会离我而去，而这就是一切之所在。"
T["TXT_KEY_BUILDING_TOWER_OF_COMPLACENCY_PEDIA"]="[TAB]自满之塔对建造它的城市市民施加强大的精神影响。人们沦为无异于工蜂之物，麻木地服从他们暗流的号令。一切不满都被消除，但城市的生产力随之受损。"

# ============ 大型 civ PEDIA / concept PEDIA（忠实原意，LINK 剥壳） ============
T["TXT_KEY_CIV_CALABIM_PEDIA"]="[TAB]卡拉比姆社会是一个残酷的等级体系，古老的吸血鬼贵族借由血畜、血族战士这些中间阶层——他们所孕育的野心勃勃的年轻附庸——将权力凌驾于作为牲口的人类之上。他们对臣民的幸福毫不在意，因为他们的总督宅邸能将恐惧与苦痛化为生产力。他们的军队大多是炮灰。他们真正的力量在于少数亲临战场的吸血officer。[PARAGRAPH]吸血单位可通过吸食低等灵魂来令自身复原，并通过在其城市中对市民举行盛宴而获得强大力量。吸血鬼萝莎·瓦拉斯、吸血鬼领主、狂暴吸血鬼与血族卫士起始便带有吸血晋升。一旦你学会封建制，至少 7 级（若为血族战士则 3 级）的活体单位便可使用赐予吸血能力化为吸血鬼。这要求该单位位于拥有总督宅邸的城市中，或与另一名吸血鬼处于同一地块。[PARAGRAPH]吸血鬼可在肉身、不死、心灵与暗影领域学习法师级别的魔法。当一名新的吸血鬼被孕育时，它可自动习得其血裔祖所知的此类魔法。这包括那些法术领域，以及魔法、邪秽、召唤大师、咒刻、圣痕、双重施法、法术延展 I 与法术延展 II 晋升。[PARAGRAPH:2]冰之纪元几乎宣告了吸血鬼的终结。当广袤的冰盖蔓延覆盖曾经肥沃的土地，他们的主要食物来源——人类——开始变得稀少，并愈发聚集于小小的部落之中。因惧怕一种比死亡更糟的命运——一个被剥夺新鲜滋养达数世纪之久的吸血鬼那阴影般、近乎死亡的存在——大多数吸血鬼试图紧紧依附于那些不断萎缩的幸存者社群。一个孤身困于小群人中的吸血鬼，很快便从猎手沦为猎物。吸血鬼被一个接一个地送入来世。[PARAGRAPH:1]在那少数逃过猎手之手的吸血鬼中，大多数过起了野兽般的生活，靠他们在荒野中所能搜刮到的任何劣等鲜血为生，偶尔捕食那些不幸落单的人类。但少数睿智者意识到，唯一的生存之路在于完成从寄生虫到主宰的自然过渡。[PARAGRAPH:1]在古老的手足艾莉柯西丝与弗劳诺斯的率领下，一小群幸存的吸血鬼“收养”了一个乌合之众般的人类部落。他们运用自己作为不朽者的力量——不受寒冷或疲惫影响，被赋予非凡的视力与速度——确保部落有充足的食物。而他们所求的回报，不过是一种无穷无尽、可任意消耗的资源：几滴血。但吸血鬼的力量并不限于超自然的感官与体力——他们真正的伟力在于心智。[PARAGRAPH:1]吸血鬼运用他们与生俱来的狡诈与劝诱之力，把“黑暗馈赠”当作诱饵，引诱最优秀、最强壮的人类助他们一臂之力，缓慢却稳妥地钻营到了他们那小小社会的顶端。鲜有人愿意反对他们，冒着失去自己宝贵狩猎技艺的风险。那些反对者要么遭遇“意外”，要么干脆消失。[PARAGRAPH:1]当人类终于意识到正在发生什么时，为时已晚。他们困于一种地狱般的境地，无异于一个日益壮大的寄生贵族阶层的牲口，而他们是出于自己的自由意志才落入其中的。[PARAGRAPH:1]如今，弗劳诺斯与艾莉柯西丝是一个由血畜与奴隶构成的堕落而绝望的社会的大亲王与大王妃，这个社会由各大血族掌控——那些吸血鬼家族将每座城市当作自己私人的庄园农场来统治，过着颓靡奢华的生活，随心所欲地满足他们对鲜血的渴求。卡拉比姆是吸血鬼进化的顶点，是一切神圣国度天生之敌的可憎之物。"
T["TXT_KEY_CIV_GRIGORI_PEDIA"]="[TAB]格利高里是唯一能获得强大冒险者单位的文明（除巢穴探索或狐人之外）。冒险者是一位伟人兼英雄，几乎可以升级为任何人类单位。格利高里将这些可定制的英雄用作精锐战士，他们能成长为游戏中最出色的一些单位。作为平衡，他们无法获得国教的益处。[PARAGRAPH:1]卡西尔曾是效力于达格达的一位天使。他在巨龙纪元中庇护那些躲避周遭交战诸神威能的人类。正是他的进言促使达格达缔结并签署了盟约，但卡西尔觉得盟约做得还不够。他希望诸神彻底退场，让人类构筑自己的世界。当盟约允许诸神借人类之手交战时，卡西尔弃达格达之职而去，开始了自己的征程，要引领人类远离一场与他们几无干系的战争。此举使他在诸神以及侍奉诸神的人类之中都少有盟友。少数勇敢的灵魂被卡西尔的信条所吸引，尽管他拒绝向他们提供任何神赐恩惠，甚至不给予直接的领导。他的追随者必须恪守他的理念、自行领导自己。历经诸多时代，格利高里的城市为那些想要主宰自己人生者提供了安全的庇护。魔法纪元的战争与冰之纪元的匮乏，一如对每一片土地那般也令他们付出了代价，但他们不向天庭、而向自身寻求援助。[PARAGRAPH:1]在重生纪元，卡西尔依旧屹立，向他人提供理念与指引，却别无其他，仍有少数勇者被他的理念所吸引。在那些在他的土地上寻求庇护者中，有天母审判官，他们宣讲：在厄瑞玻斯行事的诸神无一值得崇拜，唯有创造了它们的那一位更伟大之神才配。卡西尔当然赞同前半部分，尽管他对后半部分讳莫如深。"
T["TXT_KEY_CONCEPT_ALIGNMENT_PEDIA"]="[H1]阵营[\\\\H1][PARAGRAPH:2]《天堂陨落》中有三种阵营：善良、中立与邪恶。每位领袖起始便属于其中之一，某些单位与政策只能由特定阵营的玩家使用。它还影响你与其他玩家的外交关系，令你对同阵营玩家获得加成、对其他阵营玩家获得减益。[PARAGRAPH:2]改变阵营的唯一途径是采用某种国教。绝对秩序、授环者、丰饶之家、无瑕者或圣母会使采用它们的任何玩家变为善良。混沌之灰烬、余烬军团、女巫团、受膏者、纷争之子或雪之手（在完成抽取仪式后）使采用它们的任何玩家变为邪恶。灰色议会使任何玩家变为中立。天空的教诲、守望者兄弟会或基鲁莫夫之痕使邪恶玩家变为中立，而令善良者仍为善良。不义之仆、杰斯议会或暗流使善良玩家变为中立，而令邪恶玩家仍为邪恶。狐人国教可使阵营随机改变。"
T["TXT_KEY_CONCEPT_AFFINITY_PEDIA"]="[H1]亲和[\\\\H1][PARAGRAPH:2]某些生物对某一特定能量类型拥有亲和。这意味着，你每控制一处该类型能量的来源，它们便获得等同于其亲和值的力量加成。因此，一个拥有自然亲和：1 的生物，你每拥有一处自然能量便获得 +1。一个拥有死亡亲和：2 的生物，你每控制一处死亡能量便获得 +2 力量。[PARAGRAPH:2]亲和可能是单位或晋升所固有的。[PARAGRAPH:2]每位法师都被赐予一项亲和晋升，它不仅提升其力量，还赋予该领域内常规法术的更强版本。你必须拥有某类能量的有效供给，你的魔法单位才能在该领域获得亲和的天赋。有效供给包括你所控制的一切真实能量来源，加上每位领袖、国教、单位宗教所独有的修正，以及单位所在地块上的一切。[PARAGRAPH:2]近四分之一的法师——阿姆莱特人称之为“彼特拉克”——在 2 个领域拥有天赋。那些在 3 个领域拥有天赋者，阿姆莱特人称之为“德克利阿克”，极为罕见且总是强大。唯有精通了每一条法则之亲和的基洛林，曾在超过 3 个领域展现过亲和。[PARAGRAPH:2]若能量供给充足，信徒也可被赐予对其神祇领域的亲和。对祭司而言这不那么罕见，尤其是高阶祭司，但仍不常见。"
T["TXT_KEY_CONCEPT_ARMAGEDDON_COUNTER_PEDIA"]="[H1]末日审判计数器[\\\\H1][PARAGRAPH:2]当坏事发生时（城市被夷平、混沌之灰烬被创立、熵变节点被建造等），末日审判计数器上升；当好事发生时（马尔迪罗死亡、混沌之灰烬圣城被夷平等），它下降。取决于游戏中的文明，末日审判计数器要么在游戏过程中缓慢上升，要么倾向于增长至约 20-40 后趋于平稳（假定玩家不做任何影响它的举动）。圣化之地选项将其从游戏中消除。末日将至选项使其变动速率翻倍。[PARAGRAPH:2]它影响许多事物。它决定塞安位面之门所授予的免费单位数量，以及各种随机事件何时发生。地狱地形只会蔓延至地狱军团领土，直到计数器超过 10，届时它开始蔓延至以混沌之灰烬为国教的玩家所拥有的土地。到 25 时它可能开始蔓延至其他邪恶土地，30 时蔓延至无主土地，50 时蔓延至中立土地，90 时甚至蔓延至善良土地。计数器还影响带有邪秽、恶魔、恶魔附身或卡娜之鞭晋升的单位向其地块蔓延地狱地形的速率。[PARAGRAPH:2]若地狱开始侵入你的土地，你有几种应对之策。派出一些单位去劫掠混沌之灰烬圣城，将是控制末日审判计数器、把地狱挡在你土地之外的绝佳办法。你也可以将几个强大的单位赠予某个正与地狱军团交战的玩家，倘若你想有所贡献又不想直接卷入战争的话。[PARAGRAPH:2]末日审判计数器还影响火焰蔓延至邻近地块的几率，以及善恶文明之间的态度修正。有一项名为圣痕的晋升，赋予单位等同于末日审判计数器一半的百分比加成，此外还有其他机制会奖励某些玩家（尤其是塞安）拥有较高的末日审判计数。[PARAGRAPH:2]由于阵营态度受末日审判计数影响（对本阵营愈发友好、对相反阵营愈发恶劣），当末日审判计数升高时，往往会爆发大规模的善恶之战。[PARAGRAPH:2]凯尔的笔记：从功能上说，计数器的作用是为终局带来更多冲突。在《超越刀锋》中，Firaxis 加入了谍报与企业来解决游戏后期的停滞。我们试图解决同一个问题，但用计数器来做，以求为游戏后期带来冲突与紧迫感。"
T["TXT_KEY_CONCEPT_PUPPET_STATES"]="傀儡国"
T["XT_KEY_CONCEPT_PUPPET_STATES_PEDIA"]="[H1]傀儡国[\\\\H1][PARAGRAPH:2]当一个掌握如何组建附庸国之法的文明征服一座城市时，可以形成傀儡国。傀儡国作为征服方玩家的附庸而创建，与前城市所有者属于同一文明类型。傀儡国是一种特殊的附庸，它不设皇宫，且永为附庸，除非它取得合法地位。当傀儡国成为其文明类型中仅存的文明时，便取得合法地位。届时它将成为普通附庸，而非傀儡国。"
T["TXT_KEY_CONCEPT_REVOLUTIONS"]="革命"
T["TXT_KEY_CONCEPT_REVOLUTIONS_PEDIA"]="[H1]革命[\\\\H1][PARAGRAPH:2]此游戏选项允许帝国中心怀不满的部分一同揭竿而起，要求变革，或试图脱离母国。无论抱怨的根源为何，你都将得到一个选项：要么忽视抱怨，要么接受城市的要求。若他们的要求得不到满足、局势恶化，城市可能向你发出最后通牒，并在你不从时诉诸武力！[PARAGRAPH:2]运作方式：[PARAGRAPH:2]此组件旨在为游戏增添真实的动态，使让你的城市与地区保持满意变得更重要、也更具挑战。你帝国中的每座城市都会有令它想留下的因素，以及令它想反叛的因素。若你无法找到一个让每座城市都满意的平衡，你将面临叛乱！叛乱形形色色，包括要求更改政策、要求更改国教以及要求独立。无论何种情形，当你面对一座反叛的城市时，你总会得到选择。"
T["TXT_KEY_CONCEPT_WEREWOLVES_PEDIA"]="[H1]狼人[\\\\H1][PARAGRAPH:2]英雄狼人杜因·哈夫蒙的诞生将首个狼人引入世界，并可能引发一场狼化的瘟疫。[PARAGRAPH:1]当任何狼人在战斗中杀死一个单位时，受害者有几率化为饥渴狼人，受其杀手控制。当另一个单位杀死一个狼人时，胜者也有几率变成饥渴狼人，尽管几率要低得多，且这种情况下不会易主。[PARAGRAPH:1]狼化在战斗中传播的几率取决于交战双方单位的相对等级。若狼人是杜因，比凶残狼王更易传播；凶残狼王比嗜血狼人更易；嗜血狼人比饥渴狼人更易。它没有几率传播给非活体单位、动物、野兽，或带有免疫疾病、屠狼或精魂 III 晋升的单位。[PARAGRAPH:1]新生的饥渴狼人危险而不可预测。它们起始便处于狂暴状态，因而无视你的命令。除非其所有者同时控制着男爵，否则它们起始便处于反叛状态，最终可能成为蛮族单位。[PARAGRAPH:1]当一个饥渴狼人杀死一个活体单位时，它的狂怒得到平息，升级为嗜血狼人。嗜血狼人在杀死活体单位时，有小几率升级为忠诚的凶残狼王。[PARAGRAPH:1]沦于狼化的单位保留其所有晋升，但失去施展任何法术的能力。若你有英雄沦于狼化，在其狼人化身被杀之前，你将无法复活他。[PARAGRAPH:1]狼人杜因·哈夫蒙拥有一项独特能力，能支配其他狼人，将它们转为其所有者控制。狼化的受害者也会效忠于治愈其诅咒之人，而这只能通过精魂 III 法术抚慰来达成。[PARAGRAPH:2]凯尔的笔记：这是一种双赢机制，意即它奖励那些本已占优的玩家，拉大领先玩家与落后玩家之间的差距。尽管双赢机制难以平衡，它们却颇为有用，因为它们减少了在玩家已经获胜的情况下、逐一啃碎游戏中残余玩家的乏味苦工，让他能够势如破竹地赢得胜利。"
T["TXT_KEY_CONCEPT_WORLD_SPELLS_PEDIA"]="[H1]世界法术[\\\\H1][PARAGRAPH:2]每个文明都有一个可以使用的世界法术。这些法术效果巨大，但每局游戏只能使用一次，因此使用前请慎重考虑。以下是各文明的世界法术：[NEWLINE][NEWLINE]阿姆莱特学院 - 魔法空白[NEWLINE]巴尔塞拉弗族 - 狂欢[NEWLINE]班诺尔联邦 - 集结[NEWLINE]卡拉比姆公国 - 血河[NEWLINE]余灰部落 - 为了部落[NEWLINE]多维洛部落 - 狂野狩猎[NEWLINE]埃洛希姆守护者 - 庇护[NEWLINE]格利高里族 - 炽热[NEWLINE]希普斯佣兵国 - 战吼[NEWLINE]伊利安遗族 - 停滞[NEWLINE]地狱军团 - 地狱之火[NEWLINE]卡扎德王国 - 富矿脉[NEWLINE]库里奥塔特 - 传奇[NEWLINE]拉努恩海盗 - 怒海[NEWLINE]勒约沙尔法 - 林木进军[NEWLINE]鲁崔尔普矮人部族 - 南托苏尔塔的馈赠[NEWLINE]马拉基姆游牧民 - 宗教狂热[NEWLINE]天界军团 - 神罚[NEWLINE]塞安隐修会 - 碎世[NEWLINE]希达永生者 - 遁入迷雾[NEWLINE]斯瓦塔尔法 - 夜之帷幕[NEWLINE][NEWLINE][TAB]凯尔的笔记：我们加入这些有两个原因。当然，它们有助于我们区分每个文明。但我们也想加入一个战略选项，迫使玩家决定使用该能力的最佳时机。因此，所有世界法术总体上都会随时间变得更强大，奖励那些不急于早期使用而从中获利的玩家。"
T["TXT_KEY_DAWN_OF_MAN_LJOSALFAR"]="[NEWLINE][NEWLINE]策略：勒约沙尔法是一个防御型文明——毕竟，他们无法建造任何攻城武器。取而代之的是，光明精灵能够有效地打一场消耗战，利用他们的森林基础设施以单位的数量压垮对手，劫掠其土地，直到他把他打得形同死人。此外还有别的路数——从野性纽带科技那里获得男爵，放出一群狼人，是攻陷敌方城市的有效办法，而法师也总是存在的。凭借在森林中建造的能力，精灵与绿叶之友的森林加成有着良好的协同——但绿叶之友的路数并非严格必需，而追随暗流这类侵略性宗教，将以溺死的形式提供出色的早期进攻单位。"

# ============ 地狱地形 PEDIA（LINK 剥壳；含 \r\n 字面转义原样保留） ============
T["TXT_KEY_CONCEPT_HELL_TERRAIN_PEDIA"]="[H1]地狱地形[\\\\H1][PARAGRAPH:2]地狱地形代表着当厄瑞玻斯落入邪恶影响之下时，可蔓延于其上的腐蚀。它与末日审判计数器紧密相连，但其效果是局部的而非全局的。[NEWLINE][NEWLINE]无地狱地形游戏选项完全阻止地狱的蔓延。（圣化之地设施阻止地狱地形蔓延进该地块，但仅用于剧本。）除此之外，地狱地形总会迅速蔓延进地狱军团所据领土，并从天界军团所据领土消退。若一处相邻地块（或传送门另一侧的地块）已被腐蚀，则当计数器超过 10 时，地狱可蔓延进以混沌之灰烬为国教的所有者的土地；一旦计数器超过 25，蔓延进其他邪恶领袖所据的土地；超过 50，蔓延进中立领袖的土地；超过 90，蔓延进善良领袖的土地。它从善良土地消退得更快，从邪恶土地消退得更慢，而从混沌之灰烬所据土地根本不消退。[NEWLINE][NEWLINE]地块上出现地狱之火、死灵图腾或受折磨的灵魂，会立即将其变为地狱地形，并只要它们存在便使其保持如此。[NEWLINE][NEWLINE]熵变节点可能爆发，将周遭地块变为地狱。[NEWLINE][NEWLINE]带有邪秽、恶魔、恶魔附身或卡娜之鞭晋升的单位，无论相邻地块多么纯净或污秽，都可将其蔓延至它们所占据的地块。[NEWLINE][NEWLINE][NEWLINE]带有天使、受福或辉光之冠晋升的单位，可帮助减缓或逆转地狱的蔓延。[NEWLINE][NEWLINE]净化法术与守护者祭室建筑可立即治愈地狱地形。[PARAGRAPH:2]当地狱蔓延时，会发生以下变化：[NEWLINE]冰原变为幽暗冰川 [NEWLINE]苔原变为荒原 [NEWLINE]平原变为堕落之野 [NEWLINE]草原变为破碎之地 [NEWLINE]沙漠变为燃烧之沙 [NEWLINE]海岸变为悲痛之海 [NEWLINE]海洋变为绝望之洋 [NEWLINE][NEWLINE]葡萄酒 [NEWLINE]海洋变为愤怒之葡萄 [NEWLINE]绵羊与猪变为蟾蜍 [NEWLINE]马匹与牛变为梦魇兽 [NEWLINE]棉花与丝绸变为剃刀草 [NEWLINE]香蕉与甘蔗变为古拉加姆 [NEWLINE]大理石变为舍乌特石 [NEWLINE]玉米、小麦与稻米变为蛇柱 [NEWLINE][NEWLINE]灌丛与泛滥平原变为黑曜石平原\r\n[NEWLINE]森林、远古森林、新生森林与丛林，变为焦林 [NEWLINE][NEWLINE]当地狱地形消退时，这些变化会逆转。请注意，在多种普通资源可能变为同一地狱等价物的情况下，这样一种资源未必会还原为它原本的那一种。"
