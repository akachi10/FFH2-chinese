# -*- coding: utf-8 -*-
"""Generate g1.out.tsv (linenum<TAB>chinese) for 19 mana-PEDIA rows.
Marker-safe: emit bracket groups [...] verbatim; translate plain-text runs via TX.
Fails loudly if any plain-text run is left untranslated (nothing silently English)."""
import re, os, sys
BASE=os.path.dirname(os.path.abspath(__file__))
rows={}
for line in open(os.path.join(BASE,"g1.tsv"),encoding='utf-8'):
    c=line.rstrip("\n").split("\t")
    rows[int(c[0])]=(c[2],c[3])   # linenum -> (key, english)

BR=re.compile(r'(\[[^\]]*\])')

# ---------- token dictionary for plain-text runs (exact-run match after strip) ----------
TX={}
def D(en,zh): TX[en.strip()]=zh
# connectors / scaffold
D("with","，需"); D("or","或"); D("and","加"); D("are to be gifted with","获赠")
D("civilization.","文明。"); D(".","。")
D("Arcane units","秘法单位"); D("Adepts","术士"); D("Affinity for this sphere","对该领域的亲和")
for n in ["I","II","III","IV"]: D(f"Channeling {n}",f"引导 {n}")
# sphere access headers
for s,z in [("Death","死亡"),("Undeath","不死"),("Dimensional","次元"),("Earth","大地"),
            ("Enchantment","附魔"),("Entropy","衰退"),("Fire","炎之"),("Force","力场"),
            ("Ice","冰之"),("Law","法则"),("Life","生命"),("Meta Magic","超魔"),("Mind","精神"),
            ("Nature","自然"),("Shadow","阴影"),("Spirit","心灵"),("Sun","太阳"),("Water","水之")]:
    D(f"Allows access to the {s} sphere spells:",f"开放{z}领域法术：")
    D(f"{s} Affinity",f"{z}亲和")
    for n in ["I","II","III"]: D(f"{s} {n}",f"{z} {n}")
# spell visible names (link text)
SPELL={
 "Hallow Grave":"祝圣坟场","Destroy Undead":"摧毁不死","Summon Angel of Death":"召唤死亡天使",
 "Make Mortal":"化为凡躯","Raise Skeleton":"唤起骷髅","Summon Spectre":"召唤幽灵",
 "Summon Wraith":"召唤厉鬼","Call of the Grave":"坟墓的召唤","Chaos Affinity":"混乱亲和",
 "Escape":"遁走","Planar Binding":"位面束缚","Door of Ether":"以太之门","Summon Warp Bubble":"召唤扭曲气泡",
 "Diligence":"勤勉","Stoneskin":"石肤","Summon Earth Elemental":"召唤地元素","Earthquake":"地震",
 "Enchanted Blade":"附魔之刃","Empower Engine":"强化机械","Craft Artifact":"打造神器","Craft Automaton":"打造自动机偶",
 "Rust":"锈蚀","Wither":"枯萎","Summon Balor":"召唤巨角炎魔","Defile":"亵渎",
 "Blaze":"烈焰","Fireball":"火球术","Summon Fire Elemental":"召唤火元素","Pillar of Fire":"火柱",
 "Temperance":"节制","Ring of Warding":"守护法环","Summon Runewyn":"召唤符文守卫","Purge Magic":"清除魔法",
 "Slow":"缓速","Summon Ice Elemental":"召唤冰元素","Snowfall":"降雪","Stagnation":"停滞",
 "Loyalty":"忠诚","Summon Host of Einjerhar":"召唤英灵之军","Unyielding Order":"不屈秩序","Cosmic Order":"宇宙秩序",
 "Sanctify":"净化","Fertility":"丰饶","Resurrection":"复活","Grant Immortality":"授予不朽",
 "Floating Eye":"飘浮之眼","Dispel Magic":"驱散魔法","Summon Djinn":"召唤灯神","Awaken Magic":"唤醒魔法",
 "Inspiration":"启迪","Charm":"魅惑","Domination":"支配","Hastur's Razor":"哈斯塔之刃",
 "Poison Blade":"淬毒之刃","Bloom":"绽放","Summon Treant":"召唤树人","Overgrowth":"疯长",
 "Blur":"虚影","Shadowwalk":"暗影行走","Summon Mistform":"召唤雾影","Replace with Changeling":"替换为易形怪",
 "Courage":"勇气","Hope":"希望","Assuage":"抚慰","Peace":"和平",
 "Scorch":"灼烧","Blinding Light":"致盲之光","Summon Aurealis":"召唤烈焰巨人","Epiphany":"顿悟",
 "Spring":"涌泉","Water Walking":"水面行走","Summon Water Elemental":"召唤水元素","Inundation":"淹没",
}
TX.update({k:v for k,v in SPELL.items()})
# civ / religion / misc link texts appearing in spell-list & short supply lines
MISC={
 "Undeath":"不死","Death":"死亡",
 "Eternal Cabal":"永恒秘党","Tomb of Arawn":"阿劳恩之墓","Shades":"暗影","Reliquary":"圣物阁",
 "Ghosts":"幽灵","Soul Forge":"灵魂熔炉","Soul Shroud":"灵魂裹尸布","Undead":"不死者",
 "the first human":"第一个人类","Cassiel":"卡西尔","Sheaim":"塞安","The Between":"界间之众",
 "sorceresses":"女巫","Astral Project":"星界投射","Emrys":"埃姆里斯众","The Chainbreakers":"断链者",
 "Khazad":"卡扎德","The Runes of Kilmorph":"基尔莫芙符文","The Foxmen":"狐人众",
 "Luchuirp":"鲁崔尔普","The Ringgivers":"授环者","The Coven":"女巫会",
 "Infernal":"地狱军团","The Ashen Veil":"灰烬之幕","The House of Plenty":"丰饶之家",
 "Clan of Embers":"余灰部落","The Undertow":"暗流","Brigit":"女神布里吉特","Ring of Carcer":"卡瑟囚环",
 "Grigori":"格利高里","Illian":"伊利安","The White Hand":"白之手","The Fellowship of the Leaves":"绿叶同盟",
 "Auric Ulvin":"奥里克·尤尔文","God of Winter":"寒冬之神",
 "Bannor":"班诺尔","The Order":"秩序圣教","The Sons of Discord":"纷争之子",
 "Mercurian":"天界军团","Amurite":"阿姆莱特","Balseraph":"巴尔塞拉弗",
 "Ljosalfar":"勒约沙尔法","Svartalfar":"斯瓦塔尔法","The Council of Esus":"艾苏斯议会",
 "The Empyrean":"天空的教诲","Malakim":"马拉基姆","Lanun":"拉努恩",
 "Unholy Taint":"邪秽污染","Os-Gabella":"奥斯·加贝拉",
}
TX.update({k:v for k,v in MISC.items()})

# ---------- shared connective clauses (exact runs, dedup, count>=2) ----------
CONN={
 "The more sources of this Mana you control, the more likely your":"你所控制的此种能量来源越多，你的",
 "civilization. It is increased for those following":"文明。对跟随",
 ", either as a State Religion or as the caster's personal faith.":"（无论作为国教还是施法者个人信仰）者而言则增加。",
 "either as a State Religion or as the caster's personal faith.":"（无论作为国教还是施法者个人信仰）者而言则如此。",
 "and reduced for those following":"者增加，而对跟随",
 ". That not only increases the unit's strength based on how much mana you control, but lets it learn more powerful versions of the spells in this sphere for free, without spending any xp to level up, so long as it has the proper Channeling promotions.":"的几率就越高。此亲和不仅会依据你控制的能量多寡提升该单位的力量，还能让它免费习得该领域更强大的法术版本，无需花费经验值升级——只要它具备相应的引导晋升即可。",
}
TX.update(CONN)

# import per-row prose + one-off connectors (LORE runs) from data module
from _lore_g1 import LORE as LORE

# ---------- effective-supply lead-ins per sphere ----------
for s,z in [("Dimensional","次元"),("Earth","大地"),("Enchantment","附魔"),("Entropy","衰退"),
            ("Fire","炎之"),("Force","力场"),("Ice","冰之"),("Law","法则"),("Life","生命"),
            ("Meta Magic","超魔"),("Mind","精神"),("Nature","自然"),("Shadow","阴影"),
            ("Sun","太阳"),("Water","水之")]:
    TX[f"The effective supply of {s} Mana is greater for the"]=f"{z}能量的有效供给，对"
TX["The effective supply of Shadow Mana is greater for the"]="阴影能量的有效供给，对"
TX["The effective supply of Sun is greater for the"]="太阳能量的有效供给，对"
TX["The effective supply of Water is greater for the"]="水之能量的有效供给，对"

# ---------- short (non-PEDIA) rows: whole-value CN ----------
SHORT={
 3:"次元能量",
 9:"力场能量",
}

# ---------- per-row LORE: exact English plain-run -> CN ----------
# Populated iteratively; the completeness gate below prints any run still missing.
LORE={}

def translate(en):
    parts=BR.split(en)   # keeps bracket groups as separate items
    missing=[]
    o=[]
    for seg in parts:
        if seg=="":
            continue
        if seg.startswith("[") and seg.endswith("]"):
            o.append(seg); continue   # marker verbatim
        raw=seg
        key=seg.strip()
        if key=="":
            o.append(seg); continue   # whitespace-only run: keep as-is (spacing)
        if key in TX:
            # preserve leading/trailing spaces around the run
            lead=raw[:len(raw)-len(raw.lstrip())]
            trail=raw[len(raw.rstrip()):]
            o.append(lead+TX[key]+trail)
        elif key in LORE:
            lead=raw[:len(raw)-len(raw.lstrip())]
            trail=raw[len(raw.rstrip()):]
            o.append(lead+LORE[key]+trail)
        else:
            missing.append(key)
            o.append(raw)   # leave English for now
    return "".join(o), missing

if __name__=="__main__":
    allmiss={}
    result={}
    for ln,(key,en) in rows.items():
        if ln in SHORT:
            result[ln]=SHORT[ln]; continue
        cn,miss=translate(en)
        result[ln]=cn
        if miss: allmiss[ln]=miss
    # report missing runs
    if "--emit" not in sys.argv:
        tot=0
        for ln in sorted(allmiss):
            print(f"--- L{ln} {rows[ln][0]}: {len(allmiss[ln])} missing runs ---")
            for m in allmiss[ln]:
                tot+=1
                print(repr(m))
        print(f"TOTAL missing runs: {tot}")
    else:
        if allmiss:
            sys.exit(f"REFUSE emit: {sum(len(v) for v in allmiss.values())} untranslated runs")
        # marker parity check per row
        CL="["+chr(92)+chr(92)+"LINK]"
        for ln,(key,en) in rows.items():
            cn=result[ln]
            assert en.count("[LINK=")==cn.count("[LINK="), f"L{ln} LINK open"
            assert en.count(CL)==cn.count(CL), f"L{ln} LINK close"
            assert "\t" not in cn and "\n" not in cn, f"L{ln} real tab/nl"
        with open("g1.out.tsv","w",encoding='utf-8') as f:
            for ln in sorted(result):
                f.write(f"{ln}\t{result[ln]}\n")
        print("WROTE g1.out.tsv", len(result), "rows")
