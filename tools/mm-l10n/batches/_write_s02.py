# -*- coding: utf-8 -*-
import json
tr = {
"TXT_KEY_UNIT_LOSHA_PEDIA": "三位将领坐在前厅,等候被召入王座厅。其中一人是身经百战的老兵,冷峻沉着地坐着;第二人较为年轻、初任其职,紧张地坐立不安。那女人打了个呵欠,望向窗外。不久大门开启,他们被引入厅内,列于双王座之前。卫兵退下,只留三人与艾莉柯西丝和弗劳诺斯独处。[PARAGRAPH:1]艾莉柯西丝立刻起身,快步走向他们。&#147;你们三人受命守住我们的新殖民地帕武纳尔!可你们还没回来向我复命,像挨了打的狗一样,我的斥候就已告知我——我们的城市已成废墟!告诉我发生了什么,以及我为何不该把你们吞——为何不该处死你们。\" [PARAGRAPH:1]\"谢欧尔,先说你的汇报,\"弗劳诺斯插话道。他仍瘫坐在王座上,目光却锐利地盯住那年轻人。[PARAGRAPH:1]\"是,主人,女主人。我们……奉佩迪安之命,抵达城镇后将部队分为三部。我统领猎手。我们前往丘陵与森林,远在敌军逼近帕武纳尔之前便已发现他们。我,呃,我把手下分成小队,在敌军行军途中袭扰他们,并派斥候把敌军数量与编成的情报送回洛莎和佩迪安处。整整一个月,敌军围攻城镇,我持续伏击消耗他们。然后,城镇的大门开了!我兵力不足以击败敌军,主人们……我必须禀报,是洛莎和佩迪安辜负了你们。\"[PARAGRAPH:1]\"你们全都失败了,蠢货,\"艾莉柯西丝咆哮道。她跺着脚回到王座坐下,用凌厉的目光刺向谢欧尔。[PARAGRAPH:1]\"佩迪安,请继续说下去,\"弗劳诺斯道。[PARAGRAPH:1]\"正如谢欧尔所言,主人们,不过我必须把责任明明白白地归到洛莎肩上。我带走了突击部队,把弓箭手和移民留给她去部署城镇的防御。她本该轻而易举地守住整个季度,尽管敌军数量比我们预想的要多。我返回附近的阿凯亚去召集更多兵力,正在回程途中,便收到殖民地已被夷平的消息。我把手下留驻在那里,受召便回来了。所以显然是洛莎害我们输掉了这场仗,\"将军说完,退后一步,低下头。[PARAGRAPH:1]弗劳诺斯微微一笑。&#147;洛莎,看来正如我常对妹妹所说:柔弱的性别既缺乏力量,也缺乏判断力。不过,还是说说你的故事吧,我们且看看。\"[PARAGRAPH:1]洛莎从容地开口。&#147;正如他们所说,我的王子与公主,只是他们低估了你们敌人的数量。敌军数倍于我们出征时的兵力。若是硬拼,我们或许能拿下他们,但我军的伤亡将是重大的损失。因此我判定,失去那些移民好过一场血战。\" [PARAGRAPH:1]\"你好大的胆子!你受命是守住殖民地!\" [PARAGRAPH:1]\"我的女主人,命令就在我手上。上面写着:&#145;当入侵之军抵达我们的帕武纳尔城镇时阻止他们。'我正是这么做的。\" [PARAGRAPH:1]\"洛莎,你刚才说你丢了那些移民。\" [PARAGRAPH:1]\"哦,我是不是忘了提?在我把城镇——连同那些讨厌的居民——弃给敌军之前,我在粮仓里下了毒,酒里、水里也下了毒。\" [PARAGRAPH:1]艾莉柯西丝眨了眨眼;弗劳诺斯在王座上坐直了身子。&#147;谢欧尔,佩迪安,你们可以退下了,你们的命令稍后就到。洛莎,留下。\"年轻人溜了出去,年长者随后跟上,临走前却给了洛莎一个残忍的微笑。[PARAGRAPH:1]\"这么说,我惹恼了我的主人们?\"洛莎问道。[PARAGRAPH:1]\"亲爱的洛莎,\"艾莉柯西丝含笑说道,&#147;你已彻底为自己正了名。来吧,我们有一份礼物要给你。\"",
"TXT_KEY_PEDIA_CATEGORY_EVENT": "事件",
"TXT_KEY_PEDIA_CATEGORY_EVENTAGE": "时代",
"TXT_KEY_PEDIA_CATEGORY_GREAT_PERSONS": "伟人",
"TXT_KEY_PEDIA_CATEGORY_CONCEPT_DCM": "DCM 概念",
"TXT_KEY_WB_PUSH_MISSION": "推入任务",
"TXT_KEY_WB_WAIT": "等待中",
"TXT_KEY_WB_MOVE_CITY": "移动城市",
"TXT_KEY_WB_SENSIBILITY": "检查多格模式的前置条件",
"TXT_KEY_WB_PLOT": "地块",
"TXT_KEY_WB_UNIT": "单位",
"TXT_KEY_WB_LANDMARKS": "地标",
"TXT_KEY_WB_COASTAL_TRADE": "沿海 [ICON_TRADE]:%d1",
"TXT_KEY_WB_BASE_RATE": "基础速率:%d1",
"TXT_KEY_WB_REPEATABLE": "可使用游戏中已有的文明与领袖",
"TXT_KEY_WB_ADD_UNITS": "添加单位",
"TXT_KEY_WB_DEFAULT": "默认",
"TXT_KEY_WB_SCRIPT_DATA": "脚本数据",
"TXT_KEY_WB_GAME_YEAR": "游戏年份:%s1",
"TXT_KEY_WB_GAME_TURN": "游戏回合:%d1",
"TXT_KEY_WB_TARGET_SCORE": "目标分数:%d1",
"TXT_KEY_WB_AREA_ID": "区域 ID",
"TXT_KEY_WB_SINGLE_PLOT": "单个地块",
"TXT_KEY_WB_UNIT_DATA": "单位数据",
"TXT_KEY_WB_IMMOBILE_TIMER": "无法移动计时",
"TXT_KEY_WB_MADE_INTERCEPT": "已进行拦截",
"TXT_KEY_WB_TEMP_HAPPY": "临时 [ICON_HAPPY]:%d1",
"TXT_KEY_WB_GRANT_AVAILABLE": "可授予",
"TXT_KEY_WB_FREE_SPECIALISTS": "免费专家",
"TXT_KEY_WB_STATE_RELIGION_UNIT": "[ICON_RELIGION] 单位 [ICON_PRODUCTION]:%d1%%",
"TXT_KEY_WB_TECH_TRADING": "科技交易",
"TXT_KEY_WB_VASSAL_TRADING": "附庸交易",
"TXT_KEY_WB_IGNORE_IRRIGATION": "忽略灌溉",
"TXT_KEY_WB_ENEMY_WAR_WEARINESS": "敌方厌战度:%d1",
"TXT_KEY_WB_UPGRADE_PROGRESS": "升级回合:%d1",
"TXT_KEY_WB_CVASSAL": "已投降",
"TXT_KEY_WB_KILL": "消灭",
"TXT_KEY_WB_STRENGTH_DEFENSE": "基础防御力:",
"TXT_KEY_WB_MOVE_DISABLED_AI": "已对 AI 禁用移动",
"TXT_KEY_WB_FOUND_DISABLED": "已禁用建城",
"TXT_KEY_WB_PLOT_MIN_LEVEL": "最低等级:",
"TXT_KEY_WB_SCENARIO_COUNTER": "剧本计数器:",
"TXT_KEY_WB_COMMERCE_SLIDERS": "商业滑块:",
"TXT_KEY_WB_REV_INDEX": "革命指数 [ICON_UNHAPPY]:%d1",
"TXT_KEY_WB_CURRENT_UNIT": "当前单位:",
"TXT_KEY_WB_REASSIGN_PLAYER": "重新分配玩家",
"TXT_KEY_WB_IS_PERMANENT_SUMMON": "为永久召唤物",
"TXT_KEY_WB_SUMMON": "召唤物",
"TXT_KEY_WB_SUMMONER": "召唤者",
"TXT_KEY_WB_SWITCH_PLAYER": "切换玩家",
"TXT_KEY_WORLD_UNITS": "世界单位",
"TXT_KEY_UNLIMITED_UNITS": "无限单位",
"TXT_KEY_WB_LACKS_PROMOTIONS": "不具备晋升",
"TXT_KEY_WB_SPELL": "施放法术",
"TXT_KEY_SANCTUARY_TIMER": "庇护所计时:%d1",
"TXT_KEY_WB_FORTIFY_TURNS": "驻防回合",
"TXT_KEY_WB_UNIT_CLASS": "单位类别类型",
"TXT_KEY_RESOLUTIONS": "议案",
"TXT_KEY_WB_BLOCKADING": "封锁中",
}
data=json.load(open('_b24_in/s02.json',encoding='utf-8'))
assert len(data)==59, len(data)
lines=[]
for it in data:
    k=it['key']
    assert k in tr, "missing "+k
    v=tr[k]
    assert '\n' not in v and '\t' not in v and '\r' not in v, k
    lines.append(k+'\t'+v)
open('_b24_out/s02.out.tsv','w',encoding='utf-8').write('\n'.join(lines)+'\n')
print("wrote",len(lines),"rows")
