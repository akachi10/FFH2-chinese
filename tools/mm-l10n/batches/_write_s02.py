# -*- coding: utf-8 -*-
import json,re
from collections import Counter
data=json.load(open('_b17_in/s02.json',encoding='utf-8'))
src={it['key']:it['en'] for it in data}

# Build translations. Use actual backslash sequences via raw notation carefully.
# In python source, to emit literal [\\LINK] (backslash-backslash) we write '[\\\\LINK]'.
BS2='[\\\\LINK]'  # -> literal [\\LINK]

esus = (
"[TAB]一个秘密议会,它散布谎言的本领高超到常常连自己故事的真伪都分辨不清。它在多数大城市都设有“王座”(秘密聚会之所),尤其擅长将货物与人员偷运进出各地。杰斯被称为盗贼之王、暗影杰克与月歌,尽管教内领袖也常喜欢将这些名号据为己有。"
"[PARAGRAPH:2]创立[PARAGRAPH]以下是关于本教创立流传最广的传说,无人知晓它是否属实。"
"[PARAGRAPH]在其他诸神不知情时,杰斯会时不时潜入造化之中。他最常化身为游方的吟游诗人(男女随他心意),偶尔也化作商人、乞丐、豺狼或乌鸦。"
"[PARAGRAPH]在一次这样的游历中,他遇见了奥里奥尔·佩雷格里努斯——一位多年来一直在偷盗自己神庙的基鲁莫夫祭司。就在他即将受审的前一夜,他坐在酒馆里喝闷酒,低声向任何愿意听他祷告的神明祈求,因为他自己所侍奉的神必定不会宽恕他的罪行。"
"[PARAGRAPH]正在酒馆献艺的杰斯听见了他的话,便上前宽慰这人。两人对饮,奥里奥尔终于道出了自己的遭遇。杰斯给了他一个可以向教会讲述的谎言,可奥里奥尔仍担心没人会相信他。于是杰斯递给他一枚蛋白石圣甲虫,说它能让任何人都相信他的谎言。"
"[PARAGRAPH]奥里奥尔带着圣甲虫去教会长老面前受审。令他惊讶的是,他们毫不怀疑地相信了他的谎言。指控他的人反遭惩处,而他在基鲁莫夫教会中的地位也随之提升。"
"[PARAGRAPH]一年后杰斯归来,又在那间酒馆里找到了奥里奥尔。这次他已经潦倒不堪,几乎付不起自己的酒钱,世上一切他所珍视的东西都已失去。杰斯问他出了什么事,他说如今没有人相信他所说的任何话。他以为圣甲虫受了诅咒,便把它扔了。"
"[PARAGRAPH]杰斯解释道,他确实让这人的谎言变得可信,但代价是:此后没有人会相信奥里奥尔说出的任何真话。倘若奥里奥尔对妻子说他爱她,她也不会相信。"
"[PARAGRAPH]奥里奥尔对着酒杯啜泣起来。"
"[PARAGRAPH]“你叫什么名字?”杰斯问。"
"[PARAGRAPH]“奥里奥尔。”奥里奥尔说,目光仍盯着自己的酒。"
"[PARAGRAPH]“我不信。”杰斯说,“我看你的名字该叫门达克斯·奥帕库斯。”"
"[PARAGRAPH]“我的名字叫门达克斯?”奥里奥尔问。"
"[PARAGRAPH]“这听着好多了。这是个人们会相信的名字。”杰斯说,“那你又侍奉哪位神?肯定不是基鲁莫夫,我看你侍奉的是杰斯,暗影之神。”"
"[PARAGRAPH]“我侍奉暗影之神?”奥里奥尔问。"
"[PARAGRAPH]“正是。看,这有多容易。”杰斯说,“还有记住:你可以对任何女人说你爱她,她都会相信你——只要那不是真的。倘若你当真爱她,你的话在她耳中便会发苦,你的深情会化作毒药,令她厌弃你。你可以去一座新城,开始新的生活,为杰斯兴建一座教会——只要你心里明白,这一切全是假戏。”"
"[PARAGRAPH]“你的诅咒已经夺走了我妻子的爱。”奥里奥尔说,“我已失去在教会中的地位,你还要我连信仰也一并抛弃?我若直接去找教会长老,把你对我的所作所为告诉他们又如何?”"
"[PARAGRAPH]“你尽可一试,可谁会信你呢?”杰斯笑着说。"
"[PARAGRAPH]如今改名门达克斯的奥里奥尔,依杰斯所言,在一座废弃的帕特里亚庄园里创立了第一座幽冥王座(要让人相信他才是真正的主人,实在轻而易举)。那座王座的种种传统大多由他一手杜撰,是他一时兴之所至、灵感交织而成的一团乱麻。据说他此生最大的秘密,是他直到死去那天都还私藏着一座小小的基鲁莫夫神龛。"
"[PARAGRAPH:3]教派[PARAGRAPH]每一座王座都可视为自成一派。它们之间没有共通的联络、规则或传统。有的残暴而好复仇,有的则轻松而自在。它们往往与自己所处的社群截然相反。有时它们是城邦政府背后的秘密力量,有时又不过是一群假扮秘密组织的少年冒险者。"
"[PARAGRAPH:3]作为诸教中的一个异数,杰斯议会没有神庙,也没有寻常的信徒。身为一个秘密社团,它无法向城市或周遭所有单位公开地[LINK=SPELL_EVANGELIZE]传道"+BS2+"。然而,任何身为成员的单位都可以付出代价,在任意城市中建立起当地的议会据点。没有其他国教前置要求、且领袖持有相应国教的单位,可以花费金钱,向同一格上的杰斯[LINK=PROMOTION_EVANGELIZE]传道者"+BS2+"购买一次入会仪式。为奇迹付费——这一主题在杰斯议会中屡见不鲜。"
"[PARAGRAPH]杰斯的祭司拥有间谍的种种能力,包括窃取情报、破坏城市生产,以及破坏包括独特地貌在内的各类设施。"
"[PARAGRAPH]国教开放[LINK=UNIT_SHADOWRIDER]暗影骑手"+BS2+"、[LINK=UNIT_DISCIPLE_ESUS]骗徒 "+BS2+"、[LINK=UNIT_PRIEST_ESUS]窃贼"+BS2+"与[LINK=UNIT_HIGH_PRIEST_ESUS]鼓吹者"+BS2+"等单位。"
"[PARAGRAPH]杰斯议会与天空的教诲有重大冲突。二者中的一方可以阻止另一方传入某城,或将另一方逐出。"
"[PARAGRAPH]杰斯议会是与上位议会相抗衡的下位议会得以创立的幕后推手。在本教创立之前,任何玩家都不得采用下位议会政策;而任何以本教为国教的玩家也不得加入上位议会。\\r\\n\\t\\t\\r\\n\\t\\t\\r\\n\\t\\t\\r\\n"
"[PARAGRAPH:3][LINK=RELIGION_COUNCIL_OF_ESUS]杰斯议会"+BS2+"的祭司与天使,其阿尔达会因[LINK=RELIGION_COUNCIL_OF_ESUS]杰斯议会"+BS2+"的影响而得到最大程度的强化,同时也会在较小程度上因[LINK=RELIGION_STEWARDS_OF_INEQUITY]不公之管家"+BS2+"、[LINK=RELIGION_ANOINTED]受膏者"+BS2+"、[LINK=RELIGION_COVEN]夹界"+BS2+"、[LINK=RELIGION_THE_ASHEN_VEIL]混沌之灰烬"+BS2+"、[LINK=RELIGION_SONS_OF_DISCORD]纷争之子"+BS2+"与[LINK=RELIGION_EMBER_LEGION]余烬军团"+BS2+"而增强。其阿尔达会因[LINK=RELIGION_CHILDREN_OF_THE_ONE]太一之子"+BS2+"、[LINK=RELIGION_MATRONAE]母神会"+BS2+"、[LINK=RELIGION_THE_EMPYREAN]天空的教诲"+BS2+"、[LINK=RELIGION_GREY_COUNCIL]灰议会"+BS2+"、[LINK=RELIGION_UNBLEMISHED]无瑕者"+BS2+"、[LINK=RELIGION_RINGGIVER]赐环者"+BS2+"、[LINK=RELIGION_THE_EMPYREAN]绝对秩序"+BS2+"、[LINK=RELIGION_RUNES_OF_KILMORPH]基鲁莫夫之痕"+BS2+"、[LINK=RELIGION_CULT_OF_THE_DRAGON]巨龙教团"+BS2+"、[LINK=RELIGION_HOUSE_OF_PLENTY]丰饶之家"+BS2+"、[LINK=RELIGION_BROTHERHOOD_OF_WARDENS]守护者兄弟会"+BS2+"与[LINK=RELIGION_FELLOWSHIP_OF_LEAVES]绿叶之友"+BS2+"而削弱。它在善良阵营的土地上会被削弱,在中立或邪恶阵营的土地上会被强化。靠近[LINK=BONUS_MANA_SHADOW]暗影能量"+BS2+"、[LINK=IMPROVEMENT_WODES_OAK]沃德橡树"+BS2+"与[LINK=IMPROVEMENT_WHISPERING_WOOD]低语森林"+BS2+"会使其增强;靠近[LINK=BONUS_MANA_SUN]太阳能量"+BS2+"、[LINK=IMPROVEMENT_MIRROR_OF_HEAVEN]天堂之镜"+BS2+"与[LINK=IMPROVEMENT_CITADEL_OF_LIGHT]光明堡垒"+BS2+"则会削弱它。"
)

grey = (
"被延请来在各方之间裁断是非的审判官。他们的信仰宣扬摒弃偏私,做出裁决时不受地方或私人影响。机制:灰议会是一个投票机构,玩家可在其中与其他玩家一同参与选举。常被称为“裁断者”。\\r\\n\\r\\n\\r\\n"
"[PARAGRAPH][ICON_BULLET][LINK=RELIGION_GREY_COUNCIL]灰议会"+BS2+"的祭司与天使,其阿尔达会因[LINK=RELIGION_GREY_COUNCIL]灰议会"+BS2+"的影响而增强。其阿尔达会因[LINK=RELIGION_CHILDREN_OF_THE_ONE]太一之子"+BS2+"、[LINK=RELIGION_MATRONAE]母神会"+BS2+"与[LINK=RELIGION_CULT_OF_THE_DRAGON]巨龙教团"+BS2+"而削弱。它在中立阵营的土地上会被强化,在善良或邪恶阵营的土地上会被削弱。靠近[LINK=BONUS_MANA_FORCE]力场能量"+BS2+"、[LINK=IMPROVEMENT_SEVEN_PINES]七松"+BS2+"或[LINK=IMPROVEMENT_RING_OF_WARDING]守护之环"+BS2+"会使其增强。\\r\\n\\r\\n\\t\\t"
)

out={'TXT_KEY_RELIGION_COUNCIL_OF_ESUS_PEDIA':esus,'TXT_KEY_RELIGION_GREY_COUNCIL_PEDIA':grey}

# ---- parity verify vs source ----
def inv(s):
    return {
      'PARA': Counter(re.findall(r'\[PARAGRAPH(?::\d)?\]',s)),
      'TAB': s.count('[TAB]'),
      'NEWLINE': s.count('[NEWLINE]'),
      'ICON_BULLET': s.count('[ICON_BULLET]'),
      'LINKopen': s.count('[LINK='),
      'LINKclose': s.count('[\\\\LINK]'),
      'lit_r': s.count('\\r'),'lit_n': s.count('\\n'),'lit_t': s.count('\\t'),
      'realNL': s.count(chr(10)),'realTAB': s.count(chr(9)),
      'entity': '&#x' in s,
    }
def linkset(s): return Counter(re.findall(r'\[LINK=[^\]]*\]',s))
ok=True
for k in out:
    a,b=inv(src[k]),inv(out[k])
    for f in a:
        if a[f]!=b[f]:
            ok=False; print(f"MISMATCH {k} {f}: src={a[f]} cn={b[f]}")
    if linkset(src[k])!=linkset(out[k]):
        ok=False
        d1=linkset(src[k]); d2=linkset(out[k])
        print(f"LINK TARGET set mismatch {k}:")
        for t in set(d1)|set(d2):
            if d1[t]!=d2[t]: print("   ",t,"src",d1[t],"cn",d2[t])
    if chr(9) in out[k] or chr(10) in out[k]:
        ok=False; print(f"{k}: real TAB/NL in translation!")
print("PARITY OK" if ok else "PARITY FAILED")
if ok:
    with open('_b17_out/s02.out.tsv','w',encoding='utf-8') as f:
        f.write('TXT_KEY_RELIGION_COUNCIL_OF_ESUS_PEDIA\t'+esus+'\n')
        f.write('TXT_KEY_RELIGION_GREY_COUNCIL_PEDIA\t'+grey+'\n')
    print("WROTE _b17_out/s02.out.tsv")
