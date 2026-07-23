# -*- coding: utf-8 -*-
import io,re,importlib.util
spec=importlib.util.spec_from_file_location("d","_trans_b10_data.py"); d=importlib.util.module_from_spec(spec); spec.loader.exec_module(d)
GL=dict(d.GL)
GL.update({"Ember Legion":"余烬军团","Eternal Cabal":"永恒结社","Brotherhood":"守望者兄弟会",
 "Runes of Kilmoprh":"基鲁莫夫之痕","Letum Frigus":"莱图姆·弗里古斯","Hills":"丘陵","Rivers":"河流",
 "rivers":"河流","water":"水域","flatlands":"平坦地","Water Terrain":"水域地形","Peaks":"山峰",
 "Fields of Perdition":"堕落之野","Burning Sands":"燃烧之沙","Jungles":"丛林","Smoke":"烟雾","Flames":"火焰",
 "Wastelands":"荒原","Field of Perdition":"堕落之野"})
PHRASE={"every sort of explorable lair":"各类可探索的巢穴","Cages":"囚笼",
 "by having fortified too long in one place":"在一处驻防过久","Wastelands":"荒原",
 "Fields of Perdition":"堕落之野","Wode's Oak":"沃德橡树","Meta Magic Mana":"元魔法能量",
 "Water Mana":"水流能量","Sun Mana":"太阳能量","Spirit Mana":"精魂能量","Creation Mana":"创造能量",
 "Enchantment Mana":"附魔能量","Law Mana":"律法能量","Death Mana or Ice Mana":"死亡能量或寒冰能量",
 "Grigi Abattoir":"格里吉屠场","Pyre of the Seraphic":"炽天焚坛","Tapestry House":"织锦之屋",
 "Grave of Asmoday":"阿斯莫代之墓","Rings of Warding":"守护之环","City Ruins":"城市废墟",
 "Burnt Forests":"焦林","Burning Sands":"燃烧之沙","Tundra":"苔原","Whaling Boats":"捕鲸船",
 "Desert":"沙漠","Felllowship of the Leaves":"绿叶之友","Fellowship of the Leaves":"绿叶之友",
 "Runes of Kilmorph":"基鲁莫夫之痕","Hallowed Ground":"圣化之地","Water":"水域"}
def term(x):
    x=x.strip().rstrip('.').strip()
    x=re.sub(r'^(?:or|and)\s+','',x,flags=re.I)
    if x in PHRASE: return PHRASE[x]
    x=re.sub(r'^(the|a|an)\s+','',x,flags=re.I)
    x=re.sub(r'\s+terrain$','',x,flags=re.I)
    if x in PHRASE: return PHRASE[x]
    for k in (x,'The '+x,x.replace('The ','').strip(),x.strip()):
        if k in GL: return GL[k]
    return "«"+x+"»"  # marker for unmapped, to catch leaks
def tlist(s):
    s=re.sub(r'\s+(?:and|amd)\s+',',',s.strip().rstrip('.'))
    s=re.sub(r'\bor\s+',' ',s)
    s=s.replace(' terrain','')
    out=[]; seen=set()
    for t in s.split(','):
        t=t.strip()
        if not t or t.lower() in ('flatlands','rivers','water'):
            special={'flatlands':'平坦地','rivers':'河流','water':'水域'}
            if t.lower() in special:
                v=special[t.lower()]
                if v not in seen: seen.add(v); out.append(v)
            continue
        v=term(t)
        if v not in seen: seen.add(v); out.append(v)
    return '、'.join(out)
raw=io.open("_b10_frag/r97_arda.txt",encoding="utf-8").read().rstrip("\n")
raw=re.sub(r'^\d+\t','',raw)
en=re.sub(r'\[LINK=[^\]]*\]([^\[]*)\[\\\\LINK\]', lambda m:m.group(1).strip(), raw)
# fix a stray leftover in Laeran: "Mind Mana[\\LINK]"
en=en.replace('Mind Mana[\\\\LINK]','Mind Mana').replace('Mind Mana[\\LINK]','Mind Mana')
segs=en.split('[PARAGRAPH][ICON_BULLET]')
intro_en=segs[0]; bullets=segs[1:]

def render(b):
    b=re.sub(r'\\r\\n','',b).strip()
    kind='祭司与天使' if 'Angels' in b[:45] else ('祭司与恶魔' if 'Demons' in b[:45] else '祭司')
    m=re.search(r'of\s+(?:the\s+)?(.*?)\s+will have', b)
    rel=term(m.group(1))
    out=f"{kind}的神赐之力，受{rel}的影响强化最甚"
    m3=re.search(r'lesser degree by\s+(.*?)\.\s*Its?\s+arda', b, re.S)
    if m3: out+=f"，也在较小程度上受{tlist(m3.group(1))}强化"
    out+="。"
    m4=re.search(r'arda (?:will be|is) weakened by\s+(.*?)\.\s*It will', b, re.S)
    if not m4: m4=re.search(r'arda will be weakened by\s+(.*?)\.\s*It will', b, re.S)
    if m4: out+=f"其神赐之力会被{tlist(m4.group(1))}削弱。"
    # alignment clause
    ma=re.search(r'(It will be (?:strengthened|weakened) in [^.]*?lands[^.]*?\.)', b)
    if ma:
        al=ma.group(1)
        al=(al.replace('It will be strengthened in Good lands and weakened in Evil lands.','它在善良土地强化，在邪恶土地削弱。')
              .replace('It will be strengthened in Good or Neutral lands.','它在善良或中立土地强化。')
              .replace('It will be strengthened in Neutral lands and weakened in Good or Evil lands.','它在中立土地强化，在善良或邪恶土地削弱。')
              .replace('It will be strengthened in Neutral lands and slightly weakened in Good or Evil lands.','它在中立土地强化，在善良或邪恶土地略微削弱。')
              .replace('It will be strengthened in Neutral lands.','它在中立土地强化。')
              .replace('It will be weakened in Good or Evil lands.','它在善良或邪恶土地削弱。')
              .replace('It will be weakened in Good lands, strengthened in Neutral or Evil lands.','它在善良土地削弱，在中立或邪恶土地强化。')
              .replace('It will be weakened in Good and strengthened in Evil lands.','它在善良土地削弱，在邪恶土地强化。')
              .replace('It will be weakened in Good or Neutral and strengthened in Evil lands.','它在善良或中立土地削弱，在邪恶土地强化。')
              .replace('It will be weakened in Neutral and strengthened in Evil lands.','它在中立土地削弱，在邪恶土地强化。')
              .replace('It will be weakened in Good lands and strengthened in Evil lands.','它在善良土地削弱，在邪恶土地强化。'))
        out+=al
    # proximity strengthen + weakened
    mp=re.search(r'strengthened by proximity to\s+(.*?)(?:\.\s*It is weakened by\s+(.*?))?\.?\s*(?:It is str?en?thened|$)', b, re.S)
    # robust: cut everything from 'proximity to'
    idx=b.find('proximity to')
    if idx>=0:
        rest=b[idx+len('proximity to'):]
        parts=re.split(r'\.\s*It (?:is|was) weakened by\s+|\.\s*It weakened by\s+', rest, maxsplit=1)
        strong=parts[0]
        out+=f"它会因邻近{tlist(strong)}而强化。"
        if len(parts)>1:
            weak=parts[1]
            # weak may itself contain a trailing 'It is stronger the longer...' etc
            weak=re.split(r'\.\s*It is (?:stronger|strenthened)|\.\s*It is str', weak)[0]
            out+=f"它会被{tlist(weak)}削弱。"
    # special fortify tails
    if 'stronger the longer the unit has been fortifying' in b:
        out+="单位在原地驻防越久，其力量越强。"
    if 'having fortified too long' in b:
        out+="它也会因在一处驻防过久而被削弱。"
    return out

paras=[render(b) for b in bullets]
body='[PARAGRAPH][ICON_BULLET]'.join(['']+paras)  # rejoin with markers, leading marker before first
# intro (hand): translate separately - keep markers
INTRO=("[H1]神赐之力[\\\\H1][PARAGRAPH:2]“神赐之力”一词指的是神祇能够授予其祭司与天使的神圣力量。"
"[PARAGRAPH]在巨龙纪元，诸神可以将全强度的神赐之力授予他们所愿的任何人，即便是那些深入敌方领土作战者。盟约改变了这一切。如今，诸神只被允许依据其附近凡间崇拜者所彰显的信仰之力，将神赐之力延展给他们在厄瑞玻斯的仆从。"
"[PARAGRAPH]诸神之间的结盟与仇怨，意味着对施法者自身宗教的信仰并非唯一相关因素，因为友善的神祇可能允许施法者的神祇分得一些力量，而崇奉该神之敌者也可能庇护其邻人抵御他的攻击。\\r\\n\\r\\n"
"[PARAGRAPH] 在本 modmod 中，神赐之力的强度由一系列晋升来表示，这些晋升主要影响法术失误施放的几率。带有某种宗教及神圣晋升的单位，会依据若干因素自动替换这些神赐之力等级的晋升。这些因素包括：施法者所有者的国教，控制该单位所在领土的玩家的国教，该玩家 AI 对每种宗教的偏好，最近城市中存在的宗教，最近城市中的宗教建筑，距各座圣城的距离，以及施法者所在地块或相邻地块上存在的能量或独特景观。\\r\\n\\r\\n\\r\\n"
"[PARAGRAPH]世上存在独一之子或圣母会，尤其在附近城市中，会削弱所有祭司的神赐之力。一旦圣母会的影响足够强大，圣母会城市或叛教者附近的祭司便会背弃他们的领袖，自身也沦为叛教者。一旦独一之子拥有足够的影响，祭司便可能背弃其信仰、变得反叛，甚至可能自行解散或叛投格利高里。\\r\\n\\r\\n")
full=INTRO+body+"\\r\\n\\r\\n\\r\\n\t\t"
# check for unmapped term leaks
leaks=re.findall(r'«[^»]*»',full)
print("UNMAPPED LEAKS:",set(leaks))
io.open("_b10_frag/arda_zh.txt","w",encoding="utf-8").write(full)
print("wrote arda_zh.txt len",len(full))
print("=== sample bullet 0 ===")
print(paras[0])
print("=== sample bullet 6 (kilmorph, fortify) ===")
print(paras[6])
print("=== sample bullet 11 (foxmen) ===")
print(paras[11])
