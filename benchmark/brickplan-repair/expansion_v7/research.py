"""Human error evidence ledger: paraphrases, sources, and simulation boundaries.

No scraped personal profiles or whole copyrighted discussions are redistributed.
The unit is a source page, not a participant, accident, or prevalence estimate.
"""
from collections import Counter
from urllib.parse import urlparse
from expansion_v7 import OUT
from expansion_v7.build import write

# title, URL, relevant evidence paraphrase, source kind. Relevant passages were
# inspected via the web research tools on 2026-10-23; thread comments may change.
SOURCES = [
('S01','Lego Building Process and Feedback','https://www.eurobricks.com/forum/forums/topic/55387-lego-building-process-and-feedback/',
 '讨论者描述预判下一步而搭错镜像、难以区分说明书中的黑与深灰，以及装配次序造成难以加件。','community-self-report'),
('S02','Ever miss a piece?','https://www.eurobricks.com/forum/forums/topic/104424-ever-miss-a-piece/',
 '讨论区分真正缺货、使用错颜色和零件留在包装／附近；不能把所有找不到零件都视作装配错误。','community-discussion'),
('S03','What has been the biggest error you have made?','https://www.reddit.com/r/lego/comments/14i05s9/',
 '有人在很多步骤后发现齿轮尺寸错误、零件反装或漏件，需要部分拆解；评论另描述镜像错误。','community-self-report'),
('S04','Worst mistake while building a set','https://www.reddit.com/r/lego/comments/1hk7b08/',
 '评论自述内部组件上下反装，以及漏掉不再容易看到的半厚垫片，临近完成才发现。','community-self-report'),
('S05','Worst building experience','https://www.reddit.com/r/lego/comments/1flfqhw/',
 '评论提到重复劳动、近似蓝色混淆、移动／加灯时结构散开；体验评价不是错误发生率。','community-self-report'),
('S06','Anyone else get this mixup?','https://www.reddit.com/r/lego/comments/iolsoo/',
 '发帖者以为包装给错颜色，后来确认把蓝色和灰色1×4砖用在了错误位置。','community-confirmed-correction'),
('S07','Five-year-old built a mirrored model','https://www.reddit.com/r/lego/comments/z24fzw/',
 '展示与讨论左右镜像搭建，也包含主动镜像改造；只把非预期结果用于错误启发，不把所有镜像都判错。','community-observation'),
('S08','When you get a 2x','https://www.reddit.com/r/lego/comments/1nqi2b4/',
 '多位评论者描述做完一份才发现需要两份，或提前猜测镜像重复后才发现并不完全相同。','community-self-report'),
('S09','Lego mistake already done','https://www.reddit.com/r/lego/comments/15mxko1/',
 '作者提到方向可能装反、跳过说明页并多次回查，担心修正会损坏已完成部分。','community-self-report'),
('S10','Ford GT problems','https://www.reddit.com/r/legotechnic/comments/1dv9jg9/',
 '梁错开一颗凸点导致下一组件无法装入；发帖者确认位置建议解决了问题。','community-confirmed-correction'),
('S11','Diagnosing a mistake three bags ago','https://www.reddit.com/r/lego/comments/kdsy6a/',
 '家长描述孩子尝试修正一颗凸点的偏移，修正后盖板仍对不上，需要回溯此前结构。','community-observation'),
('S12','Camper roof installation','https://www.reddit.com/r/lego/comments/1bhnv08/',
 '发帖者多次重装仍无法滑入屋顶；检索到的相关评论建议检查一颗凸点的偏移，因部分回复折叠，诊断未独立确认。','community-unresolved'),
('S13','Helicopter hook holder installed backwards','https://bricks.stackexchange.com/questions/17783/mistake-with-hook-holder-steering-arm-with-round-socket-on-technic-helicopter',
 '步骤66的球窝方向错误到步骤744才暴露；答复建议局部拆解并记录拆解过程，作者认可建议。','community-self-report'),
('S14','Why LEGO still do this?','https://www.eurobricks.com/forum/forums/topic/196660-why-lego-still-do-this/',
 '讨论颜色编码与内外层颜色；评论包含相近颜色斜坡拿错的自述。','community-self-report'),
('S15','Two symmetrical parts together','https://www.reddit.com/r/lego/comments/1odk789/',
 '作者描述黑色与灰色连接器混用，需要拆掉绞盘和发动机才能取回正确零件；另讨论x2漏看。','community-self-report'),
('S16','Misprinted instructions','https://www.reddit.com/r/lego/comments/1i51ypz/',
 '作者报告纸质步骤跳页和重复，切换App继续；归为说明材料问题。','input-material-defect'),
('S17','The purest form of pain','https://www.reddit.com/r/legotechnic/comments/1kd77ck/',
 '很晚才发现变速组件方向问题；评论同时提及说明版本歧义及反复返修，不能全部归为用户失误。','community-mixed-cause'),
('S18','Errors in build instructions','https://bricks.stackexchange.com/questions/1363/have-any-lego-sets-been-released-with-errors-mistakes-in-the-build-instructions',
 '多个具体例子涉及说明零件清单漏项、步骤重复、标注长度错误；用于输入质量排查。','input-material-defect'),
('S19','Extra parts after a bag','https://www.reddit.com/r/lego/comments/11183xw/',
 '讨论多余零件可能来自漏装或包装数量问题，帖子未形成单一确定诊断。','community-unresolved'),
('S20','Three days to build, one mistake to unbuild','https://www.reddit.com/r/lego/comments/1pkivj9/',
 '作者说明搬动展示时未托住主体，碟形部分脱落；刚性任务只模拟脱落后的结构变化。','community-self-report'),
('S21','First time building Technic','https://www.reddit.com/r/lego/comments/1v9kf2o/',
 '建造建议指出近似销、轴、齿轮容易拿混；描述小错误在后续暴露且难以拆修。','community-advice'),
('S22','A supposedly missing piece after 27 years','https://www.reddit.com/r/lego/comments/1sc7j9a/',
 '多条自述在包装、轮胎或其他位置找到零件；也有真正缺件和左右件发错的报告，应区分来源。','community-discussion'),
('S23','Color Coding','https://www.eurobricks.com/forum/forums/topic/138030-color-coding/',
 '讨论利用颜色帮助区分轴长和零件，涉及选择错误与装配复杂度；不是受控人类实验。','community-discussion'),
('S24','Has this ever happened to you?','https://www.reddit.com/r/lego/comments/14m5lq2/',
 '大量评论自述把仍在包装或附近的零件误判成缺货，也提到之前用了错颜色或漏步骤。','community-self-report'),
('S25','Rivendell extra pieces','https://www.reddit.com/r/lego/comments/12mrdy3/',
 '作者有较大的剩余斜坡，评论定位到步骤61中独立的一块，作者确认此前漏看。','community-confirmed-correction'),
('S26','Wrong brick placed 800 steps ago','https://www.reddit.com/r/lego/comments/1ldwmq5/',
 '自述内部反装等错误很晚暴露；讨论分块拆解、录像辅助重装，也有人描述多次重建才修正。','community-self-report'),
('S27','Noob: missing a few pieces','https://www.reddit.com/r/lego/comments/foem8s/',
 '评论明确自述离开后回来重复铺了一层板，以及重复同一步导致感觉缺零件。','community-self-report'),
('S28','Problems building your set','https://www.lego.com/en-dk/service/help-topics/article/what-to-do-if-youre-having-problems-building-your-set',
 '官方建议回看说明、拆回最近几步再搭，并确认连接压紧；压紧程度需要真实接触物理，当前不模拟。','official-guidance'),
('S29','Testing for Trouble','https://education.lego.com/en-us/lessons/spike-python-u6-testing-for-bugs/spike-python-u6l4-testing-for-trouble/',
 '官方教学例子包含漏轮、上下部分未连接、齿轮反装和滑台未固定；功能错误要有功能测试才可计分。','official-teaching-example'),
('S30','Influences of AR assistance on assembly stages','https://pmc.ncbi.nlm.nih.gov/articles/PMC6668604/',
 '研究区分选件与连接过程，以及感知／反应选择与动作阶段，并比较不同复杂度任务；用于分层评价设计。','primary-research'),
]

TAXONOMY = [
('H01','看漏一步或一块','missing',['S25','S09','S03'],'simulate'),
('H02','漏看重复次数，只做一份','repeat-omission',['S08','S15'],'simulate-proxy'),
('H03','中断回来重复一步或多铺一层','repeated-step',['S27'],'simulate'),
('H04','相近颜色或颜色位置拿错','wrong-color',['S06','S14','S15'],'simulate'),
('H05','相似零件、长度或类型拿错','wrong-part',['S03','S21','S23'],'simulate-proxy'),
('H06','朝向装反','rotated',['S04','S13','S09'],'simulate'),
('H07','数凸点数错，位置偏一格','offset',['S10','S11'],'simulate'),
('H08','左右或镜像关系弄反','left-right-swap',['S07','S08'],'simulate-bounded-proxy'),
('H09','顺序不当，提前封住安装通路','early-cover',['S01'],'simulate'),
('H10','早期内部错误，后期需要拆开返修','buried-repair',['S13','S15','S26'],'simulate'),
('H11','多一层导致高度不一致','extra-layer',['S27'],'simulate'),
('H12','搬动时局部散开、连带掉件','cascade-removal',['S20','S05'],'simulate-state-only'),
('H13','修复后又遇到或造成其他错误','multi-event',['S11','S17','S26'],'temporal-stress-proxy'),
('H14','没有压紧、松动或受力变形',None,['S28','S20'],'excluded-contact-physics'),
('H15','齿轮能动但传动功能不对',None,['S03','S29'],'excluded-functional-test-missing'),
('H16','说明书印错、跳页、标注错误',None,['S16','S18'],'excluded-input-defect'),
('H17','真正缺货、包装发错、零件损坏',None,['S02','S19','S22'],'excluded-unsolvable-or-inventory-task'),
('H18','看到库存剩余件就误以为结构有错','normal-control',['S19','S24','S25'],'normal-control'),
]


def main():
    directory=OUT/'human-error-research'
    sources=[dict(id=i,title=t,url=u,summaryZh=s,kind=k,accessed='2026-10-23',
        evidenceStatus='relevant-page-sections-read',locator='Thread body and relevant comments, or named article sections',
        populationEstimate=False) for i,t,u,s,k in SOURCES]
    taxonomy=[dict(id=i,title=t,simulationFamily=f,sourceIds=s,status=status) for i,t,f,s,status in TAXONOMY]
    write(directory/'sources.json',dict(sources=sources,sourceCount=len(sources),
        domains=dict(Counter(urlparse(s['url']).netloc for s in sources)),
        method='Purposive web search and relevant passage reading; not a systematic prevalence survey.',
        authorsIndependentlyVerified=False,datesAndVotesNotUsedAsFrequency=True,
        unsuccessfulBackgroundReads=[dict(url='https://papers.iafor.org/submission41389/',reason='403; not used as full-text evidence'),
            dict(url='https://escholarship.org/uc/item/1sf2c7jf',reason='Anti-bot page; not used as full-text evidence')]))
    write(directory/'taxonomy.json',dict(categories=taxonomy,sourceLevel='Community-informed synthetic state errors',
        realHumanTrajectoryDataset=False,oneToOneCauseInference=False))
    lines=['# 社区与网上的人类拼装错误：证据、取舍与题目对应', '',
        '核对日期：2026-10-23。共核对30个来源页面的相关正文／评论，包括社区、自述、官方指导及一篇原始研究。采用关键词和案例追踪，未随机抽样。', '',
        '**这些来源支持“这种错误确实有人遇到过”；不支持发生率、年龄差异或代表全体玩家。新题是受社区证据启发的合成状态，不是真人操作轨迹。**', '',
        '## 错误怎么纳入', '', '| 编号 | 人类错误／问题 | 题目机制 | 来源 | 处理 |', '|---|---|---|---|---|']
    by_id={s['id']:s for s in sources}
    for row in taxonomy:
        refs='、'.join(f'[{s}]({by_id[s]["url"]})' for s in row['sourceIds'])
        lines.append(f'| {row["id"]} | {row["title"]} | {row["simulationFamily"] or "暂不生成"} | {refs} | {row["status"]} |')
    lines += ['', '## 模拟边界', '',
        '- 漏看x2用相同类型／颜色的两个位置缺失来模拟，不声称读取了人类的注意过程。',
        '- 左右错误只使用合法刚体位姿、两个不同位置的实际零件。没有生成负行列式的镜像零件；普通左右位置互换也不冒充真实手性零件镜像。',
        '- 错轴长、错齿轮等社区例子只为相似零件选择提供依据；当前题目使用能验证几何的替代零件，不声称已测传动功能。',
        '- 多次事件测试连续恢复；第二次后台干扰不等于证明模型或人类在第一次修复时制造了该错误。',
        '- 所有模拟事件都检查合法改动及逆向恢复；低可见和完全遮挡另列，不能算普通看图漏检。',
        '- 说明书缺页、错误库存、压紧程度等保留在问题清单，分别需要信息鲁棒性、库存搜寻或接触物理任务。',
        '- 正常题也保留备用件，库存有剩余件不代表装配出错。', '', '## 逐项来源摘要', '']
    for s in sources:
        lines += [f'### {s["id"]} · [{s["title"]}]({s["url"]})', '',
            s['summaryZh'], '', f'证据类型：`{s["kind"]}`。按相关段落核对；未复制整帖，未按点赞数或自报次数加权。', '']
    (directory/'README.zh-CN.md').write_text('\n'.join(lines).rstrip()+'\n')
    print('RESEARCH',len(sources),'sources',len(taxonomy),'categories',flush=True)


if __name__=='__main__':main()
