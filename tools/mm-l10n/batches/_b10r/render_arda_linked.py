# -*- coding: utf-8 -*-
# 新口径 ARDA 渲染：保留每个 [LINK=T]显示[\\LINK] 结构（显示文字译中文），
# 连接词按固定套路译中文。标记 [PARAGRAPH]/[ICON_BULLET]/[H1] 与 \r\n\t 保真。
import io,re,sys
sys.path.insert(0,"_b10r"); import gl

en=io.open("_b10r/arda_en.txt",encoding="utf-8").read()

def L(target,disp):
    zh=gl.disp(disp)
    if zh is None: return "«"+disp+"»"
    return f"[LINK={target}]{zh}[\\\\LINK]"

# 1) translate all LINK display in place -> keep wrappers
def linksub(s):
    return re.sub(r'\[LINK=([^\]]*)\]([^\[]*)\[\\\\LINK\]', lambda m:L(m.group(1),m.group(2)), s)

# 2) split into intro + 21 bullets
segs=en.split('[PARAGRAPH][ICON_BULLET]')
intro_en=segs[0]; bullets=segs[1:]

# ---- intro: hand translation, but LINK-translate first (intro has no LINK actually) ----
INTRO=("[H1]神赐之力[\\\\H1][PARAGRAPH:2]“神赐之力”一词指的是神祇能够授予其祭司与天使的神圣力量。"
"[PARAGRAPH]在巨龙纪元，诸神可以将全强度的神赐之力授予他们所愿的任何人，即便是那些深入敌方领土作战者。盟约改变了这一切。如今，诸神只被允许依据其附近凡间崇拜者所彰显的信仰之力，将神赐之力延展给他们在厄瑞玻斯的仆从。"
"[PARAGRAPH]诸神之间的结盟与仇怨，意味着对施法者自身宗教的信仰并非唯一相关因素，因为友善的神祇可能允许施法者的神祇分得一些力量，而崇奉该神之敌者也可能庇护其邻人抵御他的攻击。\\r\\n\\r\\n"
"[PARAGRAPH] 在本 modmod 中，神赐之力的强度由一系列晋升来表示，这些晋升主要影响法术失误施放的几率。带有某种宗教及神圣晋升的单位，会依据若干因素自动替换这些神赐之力等级的晋升。这些因素包括：施法者所有者的国教，控制该单位所在领土的玩家的国教，该玩家 AI 对每种宗教的偏好，最近城市中存在的宗教，最近城市中的宗教建筑，距各座圣城的距离，以及施法者所在地块或相邻地块上存在的能量或独特景观。\\r\\n\\r\\n\\r\\n"
"[PARAGRAPH]世上存在独一之子或圣母会，尤其在附近城市中，会削弱所有祭司的神赐之力。一旦圣母会的影响足够强大，圣母会城市或叛教者附近的祭司便会背弃他们的领袖，自身也沦为叛教者。一旦独一之子拥有足够的影响，祭司便可能背弃其信仰、变得反叛，甚至可能自行解散或叛投格利高里。\\r\\n\\r\\n")

def tlist_linked(s):
    """输入含 LINK 的英文列表串（可能夹杂 'and'/'or'/'the' 及裸词如 Hills/rivers），
    先把 LINK 换成中文链接，裸词用 disp 映射，用、连接。"""
    # first sub links
    s=linksub(s)
    # split on commas / and / or that are OUTSIDE [LINK...] — links have no comma inside
    s=re.sub(r'\s+(?:and|amd|or)\s+',',',s)
    parts=[p.strip().rstrip('.') for p in s.split(',') if p.strip()]
    BARE={'Hills':'丘陵','Peaks':'山峰','rivers':'河流','flatlands':'平坦地','water':'水域',
          'Water Terrain':'水域地形','Rivers':'河流','Wastelands':'荒原','Fields of Perdition':'堕落之野',
          'Smoke':'烟雾','Flames':'火焰','Jungles':'丛林','Burning Sands':'燃烧之沙','Blizzards':'暴风雪',
          'Letum Frigus':'莱图姆·弗里古斯'}
    out=[];seen=set()
    for p in parts:
        p=re.sub(r'\s+terrain$','',p)
        if p.startswith('[LINK='):
            v=p
        elif p in BARE: v=BARE[p]
        else:
            z=gl.disp(p); v=z if z else '«'+p+'»'
        if v not in seen: seen.add(v); out.append(v)
    return '、'.join(out)

def render(b):
    b=re.sub(r'\\r|\\n|\\t','',b)  # drop the trailing \r\n for parsing; re-add later
    kind='祭司与天使' if 'Angels' in b[:60] else ('祭司与恶魔' if 'Demons' in b[:60] else '祭司')
    # religion name (with LINK) between 'of' and 'will have'
    m=re.search(r'of\s+(?:the\s+)?(\[LINK=[^\]]*\][^\[]*\[\\\\LINK\])\s+will have', b)
    rel=linksub(m.group(1)) if m else '?'
    out=f"{kind}的神赐之力，受{rel}的影响强化最甚"
    m3=re.search(r'lesser degree by\s+(.*?)\.\s*Its?\s+arda', b, re.S)
    if m3: out+="，也在较小程度上受"+tlist_linked(m3.group(1))+"强化"
    out+="。"
    m4=re.search(r'arda (?:will be|is) weakened by\s+(.*?)\.\s*It will', b, re.S)
    if m4: out+="其神赐之力会被"+tlist_linked(m4.group(1))+"削弱。"
    # alignment
    b2=b.replace('Good or neutral lands','Good or Neutral lands')
    ma=re.search(r'(It will be (?:strengthened|weakened) in [^.]*?lands[^.]*?\.)', b2)
    if ma:
        al=ma.group(1)
        R=[('It will be strengthened in Good lands and weakened in Evil lands.','它在善良土地强化，在邪恶土地削弱。'),
           ('It will be strengthened in Good or Neutral lands.','它在善良或中立土地强化。'),
           ('It will be strengthened in Neutral lands and weakened in Good or Evil lands.','它在中立土地强化，在善良或邪恶土地削弱。'),
           ('It will be strengthened in Neutral lands and slightly weakened in Good or Evil lands.','它在中立土地强化，在善良或邪恶土地略微削弱。'),
           ('It will be strengthened in Neutral lands.','它在中立土地强化。'),
           ('It will be weakened in Good or Evil lands.','它在善良或邪恶土地削弱。'),
           ('It will be weakened in Good lands, strengthened in Neutral or Evil lands.','它在善良土地削弱，在中立或邪恶土地强化。'),
           ('It will be weakened in Good and strengthened in Evil lands.','它在善良土地削弱，在邪恶土地强化。'),
           ('It will be weakened in Good or Neutral and strengthened in Evil lands.','它在善良或中立土地削弱，在邪恶土地强化。'),
           ('It will be weakened in Good or Neutral lands and strengthened in Evil lands.','它在善良或中立土地削弱，在邪恶土地强化。'),
           ('It will be weakened in Neutral and strengthened in Evil lands.','它在中立土地削弱，在邪恶土地强化。'),
           ('It will be weakened in Good lands and strengthened in Evil lands.','它在善良土地削弱，在邪恶土地强化。')]
        for a,z in R: al=al.replace(a,z)
        out+=al
    # proximity
    idx=b.find('proximity to')
    if idx>=0:
        rest=b[idx+len('proximity to'):]
        tail=""
        mt=re.search(r'\.\s*It is stren\w*\s+(?:near|on)\s+(.*)$', rest, re.S)
        if mt: tail=mt.group(1); rest=rest[:mt.start()]
        ms=re.split(r'[.,]\s*It (?:is |was )?weakened by\s+|\s+and weakened by\s+|\.\s*It weakened by\s+', rest, maxsplit=1)
        out+="它会因邻近"+tlist_linked(ms[0].strip().rstrip('.'))+"而强化。"
        if len(ms)>1:
            weak=re.split(r'\.\s*It ', ms[1])[0].strip().rstrip('.')
            out+="它会被"+tlist_linked(weak)+"削弱。"
        if tail:
            tp=re.split(r',?\s*and weakened on\s+', tail, maxsplit=1)
            out+="它在临近"+tlist_linked(tp[0].strip().rstrip('.'))+"时强化"
            if len(tp)>1:
                out+="，在"+tlist_linked(tp[1].strip().rstrip('.'))+"上削弱"
            out+="。"
    if 'stronger the longer the unit has been fortifying' in b:
        out+="单位在原地驻防越久，其力量越强。"
    if 'having fortified too long' in b:
        out+="它也会因在一处驻防过久而被削弱。"
    return out

paras=[render(b)+'\\r\\n\\r\\n' for b in bullets]
body='[PARAGRAPH][ICON_BULLET]'.join(['']+paras)
full=INTRO+body+"\\r\\n\\t\\t"
leaks=re.findall(r'«[^»]*»',full)
print("LEAKS:",set(leaks))
io.open("_b10r/arda_zh_linked.txt","w",encoding="utf-8").write(full)
print("wrote len",len(full))
print("bullet0:",paras[0][:400])
