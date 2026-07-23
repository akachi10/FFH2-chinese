#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Build s07.out.tsv for batch-17: 3 religion pedia rows.
# Markers preserved byte-exact; only display text translated.
# On-disk forms: LINK close = [\\LINK] (two backslashes); literal \r \n \t kept literal.

B = "[\\\\LINK]"   # on-disk close marker = [\LINK]... wait: in python source, "[\\\\LINK]" -> [\\LINK] (2 backslashes). Correct.
# Actually we want the on-disk bytes to be:  [ \ \ L I N K ]  = "[\\LINK]" as bytes.
# In a python str literal, "[\\LINK]" == [\LINK] (1 backslash). "[\\\\LINK]" == [\\LINK] (2 backslashes). We need 2 -> use 4 backslashes.
CL = "[\\\\LINK]"   # -> [\\LINK] on disk (two backslashes)
CR = "\\r"           # literal backslash-r on disk
NL = "\\n"           # literal backslash-n on disk
TB = "\\t"           # literal backslash-t on disk

def L(target, disp):
    return f"[LINK={target}]{disp}{CL}"

rows = {}

# ---- 1. THE_EMPYREAN_PEDIA ----
empyrean = (
    "[TAB]绝对秩序崇尚律法，而天空的教诲崇尚智慧。其裁断源自卢古斯的教诲，惩罚并非依据一部繁复如迷宫的法典，"
    "而是就每一桩案件的是非曲直直接商议而定。无论是政府与其公民之间，还是帝国与帝国之间，社会平等与不偏不倚都是其典范。"
    "因此，天空的教诲赋予小帝国与那些称霸埃雷布斯的强权同等的话语权。 "
    "[PARAGRAPH:2]将其定为国教可获得以下事物："
    "[PARAGRAPH:1][TAB]光辉守卫（单位）"
    "[PARAGRAPH:1][TAB]光辉战车（单位）"
    "[PARAGRAPH:1][TAB]喻所祭司（单位）"
    "[PARAGRAPH:1][TAB]曙光战士卡利德·阿斯特拉肯（世界单位）"
    "[PARAGRAPH:1][TAB]" + L("IMPROVEMENT_CITADEL_OF_LIGHT", "光之要塞") + "（改良设施）"
    "[PARAGRAPH:2]天空的教诲与混沌之灰烬、杰斯议会均存在重大冲突。一者可阻止另一者传入某城，或将其逐出。 "
    "[PARAGRAPH:2]天空的教诲是上位议会得以创立的推动力量。在此宗教创立之前，任何玩家都无法采纳上位议会政策。 "
    "[PARAGRAPH:3]" + L("RELIGION_THE_EMPYREAN", "天空的教诲") + "的祭司与天使，其灵力（arda）受"
    + L("RELIGION_THE_EMPYREAN", "天空的教诲") + "的影响而最为强化，同时也在较小程度上受"
    + L("RELIGION_BROTHERHOOD_OF_WARDENS", "守望者兄弟会") + "、"
    + L("RELIGION_RINGGIVER", "赐环者") + "、"
    + L("RELIGION_UNBLEMISHED", "无瑕者") + "、"
    + L("RELIGION_HOUSE_OF_PLENTY", "丰饶之家") + "、"
    + L("RELIGION_THE_EMPYREAN", "绝对秩序") + "、"
    + L("RELIGION_RUNES_OF_KILMORPH", "基鲁莫夫之痕") + "，以及"
    + L("RELIGION_LAERAN_CORD", "莱兰之绳") + "的强化。其灵力将受"
    + L("RELIGION_CHILDREN_OF_THE_ONE", "太一之子") + "、"
    + L("RELIGION_MATRONAE", "母神教") + "、"
    + L("RELIGION_COUNCIL_OF_ESUS", "杰斯议会") + "、"
    + L("RELIGION_GREY_COUNCIL", "灰色议会") + "、"
    + L("RELIGION_COVEN", "夹缝之间") + "、"
    + L("RELIGION_THE_ASHEN_VEIL", "混沌之灰烬") + "、"
    + L("RELIGION_ANOINTED", "受膏者") + "、"
    + L("RELIGION_SONS_OF_DISCORD", "纷争之子") + "、"
    + L("RELIGION_STEWARDS_OF_INEQUITY", "不义之管家") + "、"
    + L("RELIGION_WHITE_HAND", "雪之手") + "、"
    + L("RELIGION_EMBER_LEGION", "余烬军团") + "、"
    + L("RELIGION_OCTOPUS_OVERLORDS", "深渊霸主") + "，以及"
    + L("RELIGION_CULT_OF_THE_DRAGON", "巨龙崇拜") + "的削弱。它在善良之地会得到强化，在邪恶之地会被削弱。它会因临近"
    + L("BONUS_MANA_SUN", "太阳能量") + "、"
    + L("IMPROVEMENT_MIRROR_OF_HEAVEN", "天堂之镜") + "、"
    + L("IMPROVEMENT_SPIRE_OF_THE_SUN", "太阳尖塔") + "、"
    + L("IMPROVEMENT_CITADEL_OF_LIGHT", "光之要塞") + "、"
    + L("IMPROVEMENT_TOWER", "塔楼") + "、"
    + L("FEATURE_HALLOWED_GROUND", "圣化之地") + "，或"
    + L("TERRAIN_DESERT", "沙漠") + "地形而得到强化。它会被"
    + L("BONUS_MANA_SHADOW", "暗影能量") + "、"
    + L("IMPROVEMENT_WHISPERING_WOOD", "低语森林") + "，或"
    + L("IMPROVEMENT_WODES_OAK", "沃德橡树") + "所削弱。 " + CR + NL + CR + NL
)

# ---- 2. OVERLORDS_PEDIA ----
overlords = (
    "[TAB]爱琴海浪涛之下的力量据说比任何其他力量都更为强大，然而深渊霸主漫无焦点，追逐着千百种晦暗难明的图谋。"
    "深渊霸主的信徒不敢让自己直接暴露于其主宰们相互矛盾的号令之下，转而以贫苦之人充作中间人。这些人很快便在此过程中被逼疯，"
    "而信徒们反倒乐见如此，因为这能防止他们篡改所传的讯息。他们还共享一套将战士化为“溺者”——一种不死奴仆——的手段，"
    "自愿受此过程者寥寥无几。 "
    "[PARAGRAPH:2]将其定为国教可获得以下事物："
    "[PARAGRAPH:1][TAB]疯人院（建筑）"
    "[PARAGRAPH:1][TAB]无限制的狂热祭司（单位）"
    "[PARAGRAPH:1][TAB]冥河守卫（单位）"
    "[PARAGRAPH:1][TAB]溺者（单位）"
    "[PARAGRAPH:1][TAB]萨维罗斯（世界单位）"
    "[PARAGRAPH:1][TAB]大法师赫玛（世界单位）"
    "[PARAGRAPH:2]深渊霸主的邪教与绝对秩序存在重大冲突。一者可阻止另一者传入某城，或将其逐出。"
    + CR + NL + TB + TB + CR + NL + TB + TB + CR + NL +
    "[PARAGRAPH:3]" + L("RELIGION_OCTOPUS_OVERLORDS", "深渊霸主") + "的祭司与天使，其灵力（arda）受"
    + L("RELIGION_OCTOPUS_OVERLORDS", "深渊霸主") + "的影响而最为强化，同时也在较小程度上受"
    + L("RELIGION_STEWARDS_OF_INEQUITY", "不义之管家") + "、"
    + L("RELIGION_SONS_OF_DISCORD", "纷争之子") + "、"
    + L("RELIGION_ANOINTED", "受膏者") + "、"
    + L("RELIGION_FOXMEN", "狐人") + "、"
    + L("RELIGION_WHITE_HAND", "雪之手") + "、"
    + L("RELIGION_COUNCIL_OF_ESUS", "杰斯议会") + "、"
    + L("RELIGION_THE_ASHEN_VEIL", "混沌之灰烬") + "，以及"
    + L("RELIGION_COVEN", "夹缝之间") + "的强化。其灵力将受"
    + L("RELIGION_CHILDREN_OF_THE_ONE", "太一之子") + "、"
    + L("RELIGION_MATRONAE", "母神教") + "、"
    + L("RELIGION_EMBER_LEGION", "余烬军团") + "、"
    + L("RELIGION_THE_EMPYREAN", "绝对秩序") + "、"
    + L("RELIGION_GREY_COUNCIL", "灰色议会") + "、"
    + L("RELIGION_UNBLEMISHED", "无瑕者") + "、"
    + L("RELIGION_RINGGIVER", "赐环者") + "、"
    + L("RELIGION_BROTHERHOOD_OF_WARDENS", "守望者兄弟会") + "、"
    + L("RELIGION_THE_EMPYREAN", "天空的教诲") + "、"
    + L("RELIGION_LAERAN_CORD", "莱兰之绳") + "、"
    + L("RELIGION_RUNES_OF_KILMORPH", "基鲁莫夫之痕") + "、"
    + L("RELIGION_CULT_OF_THE_DRAGON", "巨龙崇拜") + "，以及"
    + L("RELIGION_ETERNAL_CABAL", "永恒密党") + "的削弱。它会因临近"
    + L("BONUS_MANA_WATER", "水之能量") + "、"
    + L("BONUS_MANA_MIND", "心灵能量") + "、"
    + L("BONUS_JETEYE", "喷眼兽") + "、水域地形、河流、泛滥平原、"
    + L("IMPROVEMENT_AIFON_ISLE", "艾冯岛") + "、"
    + L("IMPROVEMENT_FISHING_BOATS", "渔船") + "，或"
    + L("IMPROVEMENT_WHALING_BOATS", "捕鲸船") + "而得到强化。它会被"
    + L("BONUS_MANA_FIRE", "火之能量") + "、"
    + L("IMPROVEMENT_RING_OF_CARCER", "卡塞尔之环") + "、"
    + L("IMPROVEMENT_PYRE_OF_THE_SERAPHIC", "炽天者火葬堆") + "、山峰与丘陵所削弱。" + CR + NL
)

# ---- 3. SONS_OF_DISCORD_PEDIA ----
sons = (
    "卡穆洛斯的教会渴望天下万邦彼此征战。他被称为血泉与百臂之神。大战前夜，天空回荡着卡穆洛斯麾下众魔尖利的啼叫，"
    "它们满怀期待地窥伺着即将到来的战争。在不曾取缔它们的城市里，卡穆洛斯的神庙是残酷的角斗场——新杀之人的尸体堆积如山，"
    "凶蛮的野兽饱餐尸身，几乎每一块石头都染满血污。这是一个建立在仇恨之上的宗教。它在某些国度里鼓吹种族主义，"
    "在另一些国度里则煽动对某个文化族群的敌视。仇恨的对象对这个宗教而言无关紧要，重要的只是由此点燃的仇恨本身。 "
    + CR + NL + TB + TB + CR + NL + TB + TB + CR + NL + TB + TB + CR + NL +
    "[PARAGRAPH:3]" + L("RELIGION_SONS_OF_DISCORD", "纷争之子") + "的祭司与恶魔，其灵力（arda）受"
    + L("RELIGION_SONS_OF_DISCORD", "纷争之子") + "的影响而最为强化，同时也在较小程度上受"
    + L("RELIGION_EMBER_LEGION", "余烬军团") + "、"
    + L("RELIGION_FOXMEN", "狐人") + "、深渊霸主、"
    + L("RELIGION_ANOINTED", "受膏者") + "、"
    + L("RELIGION_COVEN", "夹缝之间") + "、"
    + L("RELIGION_STEWARDS_OF_INEQUITY", "不义之管家") + "、"
    + L("RELIGION_THE_ASHEN_VEIL", "混沌之灰烬") + "、"
    + L("RELIGION_COUNCIL_OF_ESUS", "杰斯议会") + "、"
    + L("RELIGION_WHITE_HAND", "雪之手") + "，以及"
    + L("RELIGION_FELLOWSHIP_OF_LEAVES", "绿叶之友") + "的强化。其灵力将受"
    + L("RELIGION_CHILDREN_OF_THE_ONE", "太一之子") + "、"
    + L("RELIGION_MATRONAE", "母神教") + "、"
    + L("RELIGION_THE_EMPYREAN", "绝对秩序") + "、"
    + L("RELIGION_GREY_COUNCIL", "灰色议会") + "、"
    + L("RELIGION_UNBLEMISHED", "无瑕者") + "、"
    + L("RELIGION_RINGGIVER", "赐环者") + "、"
    + L("RELIGION_BROTHERHOOD_OF_WARDENS", "守望者兄弟会") + "、"
    + L("RELIGION_THE_EMPYREAN", "天空的教诲") + "、"
    + L("RELIGION_RUNES_OF_KILMORPH", "基鲁莫夫之痕") + "、"
    + L("RELIGION_HOUSE_OF_PLENTY", "丰饶之家") + "、"
    + L("RELIGION_CULT_OF_THE_DRAGON", "巨龙崇拜") + "，以及"
    + L("RELIGION_LAERAN_CORD", "莱兰之绳") + "的削弱。它在善良或中立之地会被削弱，在邪恶之地会得到强化。它会因临近"
    + L("BONUS_MANA_CHAOS", "混沌能量") + "而得到强化，因"
    + L("BONUS_MANA_LAW", "秩序能量") + "而被削弱。它在荒原、灭亡之野、"
    + L("FEATURE_BLIZZARD", "暴风雪") + "、"
    + L("FEATURE_TORMENTED_SOULS", "受折磨的灵魂") + "之上会得到强化，在"
    + L("FEATURE_HALLOWED_GROUND", "圣化之地") + "之上则被削弱。 " + CR + NL + CR + NL
)

out = {
    "TXT_KEY_RELIGION_THE_EMPYREAN_PEDIA": empyrean,
    "TXT_KEY_RELIGION_OVERLORDS_PEDIA": overlords,
    "TXT_KEY_RELIGION_SONS_OF_DISCORD_PEDIA": sons,
}

import json, os
data = json.load(open(os.path.join(os.path.dirname(__file__), "..", "_b17_in", "s07.json"), encoding="utf-8"))
order = [d["key"] for d in data]
lines = []
for k in order:
    v = out[k]
    assert "\t" not in v and "\n" not in v and "\r" not in v, f"{k}: real whitespace!"
    lines.append(k + "\t" + v)
open(os.path.join(os.path.dirname(__file__), "s07.out.tsv"), "w", encoding="utf-8").write("\n".join(lines) + "\n")
print("wrote s07.out.tsv:", len(lines), "rows")
