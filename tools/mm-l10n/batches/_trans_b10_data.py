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
