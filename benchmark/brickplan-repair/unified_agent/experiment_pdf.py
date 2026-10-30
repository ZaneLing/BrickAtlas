"""Render the archived report to a self-contained, mail-friendly Chinese PDF."""
import json,time
from pathlib import Path
from xml.sax.saxutils import escape
from PIL import Image as PILImage
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle,Image,PageBreak,KeepTogether
from unified_agent.experiment_batch import OUT


def main():
    data=json.loads((OUT/'metrics.json').read_text());plan=json.loads((OUT/'plan.json').read_text())
    font='/System/Library/Fonts/STHeiti Medium.ttc';pdfmetrics.registerFont(TTFont('CJK',font,subfontIndex=0))
    styles=getSampleStyleSheet()
    for key in ['Normal','Title','Heading1','Heading2']:
        styles[key].fontName='CJK';styles[key].wordWrap='CJK';styles[key].textColor=colors.HexColor('#213a46')
    styles['Normal'].fontSize=9;styles['Normal'].leading=14
    styles['Heading1'].fontSize=16;styles['Heading1'].leading=22
    styles['Heading2'].fontSize=12;styles['Heading2'].leading=18
    styles.add(ParagraphStyle('SmallCJK',parent=styles['Normal'],fontSize=7,leading=10))
    styles.add(ParagraphStyle('TableCJK',parent=styles['Normal'],fontSize=7,leading=10))
    story=[];width=A4[0]-76
    def para(text,style='Normal'):return Paragraph(escape(str(text)).replace('\n','<br/>'),styles[style])
    def add(text,style='Normal'):story.extend([para(text,style),Spacer(1,7)])
    def table(headers,rows,widths=None):
        cells=[[para(c,'TableCJK') for c in row] for row in [headers,*rows]]
        t=Table(cells,colWidths=widths or [width/len(headers)]*len(headers),repeatRows=1,hAlign='LEFT')
        t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#e8f2f2')),
            ('VALIGN',(0,0),(-1,-1),'TOP'),('BOTTOMPADDING',(0,0),(-1,-1),6),('TOPPADDING',(0,0),(-1,-1),6),
            ('LINEBELOW',(0,0),(-1,-1),.3,colors.HexColor('#d4e0e4'))]))
        story.extend([t,Spacer(1,12)])
    def picture(name,max_height=650):
        p=OUT/'plots'/(name+'.png')
        if not p.exists():return
        with PILImage.open(p) as im:w,h=im.size
        scale=min(width/w,max_height/h);story.extend([Image(str(p),width=w*scale,height=h*scale),Spacer(1,9)])
    def ratio(g):return f"{g['success']}/{g['denominator']}" if g['denominator'] else '不适用'
    add('BRICK ATLAS\n静态与动态扩展实验报告','Title')
    add(time.strftime('%Y-%m-%d %H:%M')+'  |  '+('最终报告' if data['complete'] else '进行中快照，尚非最终结果'))
    add('1. 实验安排','Heading1')
    add('四个模型使用同一视觉 Agent。每个模型50道静态阶段题、50道正常拼装题；正常成功后另跑同题事故分支。补测上一批 Sol 未运行和 Seed 中断的条件，单独保存。')
    add('主表采用统一v5输入。v4发现工具参数说明歧义，全部条件统一重跑；旧记录保留作接口排查，费用保留，不与v5成绩混合。','SmallCJK')
    add(f"50个物件，{plan['sourceGroups']}个来源组；长度分组{plan['selectedLengths']}。长度不是已经验证的人类难度。静态同样使用工具操作，不是一次性问答。")
    statuses={s['model']:s for s in data['apiStatus']}
    table(['模型','静态/50','正常/50','接口状态'],[[s['label'],s['newSampleCompleted']['static'],s['newSampleCompleted']['normal'],
        '多图与长历史通过' if statuses[s['model']]['passed'] else statuses[s['model']].get('error','未检查')] for s in data['summary']],[125,65,65,width-255])
    table(['模型','静态正常','静态故障','正常拼装','事故修复','技术中断'],[[s['label'],*[ratio(s[k]) for k in ['control','repair','normal','incident']],s['technical']] for s in data['summary']], [113,78,78,78,91,width-438])
    add('分数为成功数/有效分母。接口失败、截断、程序错误不当作能力失败。用完该题决策预算而没有完成，计为端到端未完成。正常前置未通过，事故修复记为不适用。','SmallCJK')
    picture('success-rates',220)
    story.append(PageBreak())
    add('2. 输入和程序修复','Heading1')
    changes=[('阶段目标','静态说明书只开放到本题目标阶段，已经相同就提交，允许库存剩余。'),
        ('看清位置','新增单候选全尺寸当前/预览对照，统一相机和画布。'),
        ('知道操作哪个件','新增当前图点选辨认，只返回可见件编号；说明书标出所示零件编号，不提供目标位置编号。'),
        ('输出适配','接受唯一完整JSON外的代码围栏或前置解释；不选择多个对象，不修补缺损JSON，不执行截断。'),
        ('接口负担','每轮最大输出预留从8192调整为2048；增加较大图片包和长历史的接口检查。'),
        ('限流与版本','只对未生成内容的429有限重试；保留所有请求和用量；核对实际返回模型版本。'),
        ('历史结果','旧分数不重写。新接口下的补测和新增样本分别报告。')]
    table(['问题','修复'],changes,[95,width-95])
    add('3. 指标怎么理解','Heading1')
    table(['指标','含义'],[
        ['提交完成率','合法最终结构达标，并主动调用finish。'],['结构达标率','停止时结构和约束达标，不要求主动finish。'],
        ['结构F1','同时匹配零件种类、颜色和姿态；固定背景不加分。'],['合法动作率','接受的拆装次数/格式完整的拆装尝试。'],
        ['错误减少/损坏','初始错误消除多少；起点正确的件有多少最后被弄错。'],['合格修复率','同题正常前置成功，且计划事故全部生效，才进入分母。'],
        ['接口与效率','格式、截断、服务错误分开；记录动作、观察、token、时间和费用。']],[95,width-95])
    add('尚未证明：真人盲操作可读性、独立物理验证、全库表现。本批静态与动态不保证目标和现场完全配对，不能作为纯动态困难的因果估计。','SmallCJK')
    story.append(PageBreak());add('4. 结构结果与错误家族','Heading1')
    picture('structure-satisfaction',240);picture('error-families',260)
    add('结构已经正确但没有主动提交，单独统计；不能与拼错结构混为一谈。家族样本较少，不给正式排名或显著性结论。')
    story.append(PageBreak());add('5. 请求用量与成本','Heading1')
    table(['模型','请求数','输入token','输出token','估算CNY','API拒绝'],[[s['label'],s['apiRequests'],s['inputTokens'],s['outputTokens'],f"{s['cny']:.4f}",s['rejectedAPI']] for s in data['summary']],[120,50,95,90,90,width-445])
    add('用量来自实际API返回，输出包含已报告推理token。费用包含预检和补测，为估算而非账单；Sol的Ark单价尚未核实，金额只作暂估。')
    picture('tokens-and-cost',230);picture('observation-actions',220)
    story.append(PageBreak());add('6. 长度、动作与接口问题','Heading1')
    picture('length-groups',230);picture('action-rejections',230)
    table(['模型','合法动作/尝试','格式/字段错','技术中断'],[[s['label'],str(s['actionSummary']['accepted'])+'/'+str(s['actionSummary']['attempts']),
        str(s['toolSummary']['formatErrors'])+'/'+str(s['toolSummary']['schemaErrors']),str(s['technicalCodes'])] for s in data['summary']],[120,100,95,width-315])
    add('动作反馈码描述环境拒绝原因，不足以确定是视觉、空间理解还是计划问题。长度分组不是经真人验证的难度。截断内容没有执行，不计为拼装失败，也没有自动重试到成功。','SmallCJK')
    for name,title in [('matrix-static','7. 静态逐题结构F1'),('matrix-normal','8. 正常拼装逐题结构F1'),('matrix-incident','9. 事故修复逐题结构F1')]:
        story.append(PageBreak());add(title,'Heading1');picture(name,690)
    if (OUT/'plots/actual-trajectories.png').exists():
        story.append(PageBreak());add('10. 模型真实动作过程','Heading1');picture('actual-trajectories',500)
        add('图取自实际模型日志。末列为目标。标题明确是否完成，不把参考程序的路径冒充模型结果。完整输入、输出、操作反馈和多角度图在本机回放页中。')
    for i in (1,2):
        if (OUT/f'plots/model-vs-reference-{i}.png').exists():
            story.append(PageBreak());add('模型过程与合法参考过程对照 '+str(i),'Heading1');picture('model-vs-reference-'+str(i),520)
            add('上行为真实API模型执行记录，下行为程序验证的一条合法路线。参考路线未提供给模型，不是最短路线证明，也不要求模型遵循相同顺序。')
    story.append(PageBreak());add('11. 逐题结果与补测明细','Heading1')
    add('新样本编号1-50；补测另外标明。S0=静态正常，S1=静态故障，D0=正常拼装，D1/D2=一次/两次事故。INT=技术中断。详尽字段在随附metrics.json中。','SmallCJK')
    rows=[]
    labels={'GPT-6.1 Sol':'Sol','Seed 2.1 Pro':'Seed','DeepSeek V4.1 Flash':'DS','Qwen3.8 Flash':'Qwen'}
    for r in data['rows']:
        if r['inputVersion']!=data['inputVersion']:continue
        rows.append([('补' if r['group']!='new-sample' else '')+str(r['sampleIndex']),r['object'],labels[r['label']],r['taskType'],
            '成功' if r['success'] else '未完成' if r['success'] is False else 'INT',f"{r['f1']:.2f}",
            f"{r['moves']}/{r['manipulations']}",r['calls'],f"{r['cny']:.3f}"])
    table(['编号','物件','模型','题型','结果','F1','动作/尝试','请求','CNY'],rows,[28,178,36,32,45,32,65,40,width-456])
    def footer(canvas,doc):
        canvas.setFont('CJK',8);canvas.setFillColor(colors.HexColor('#61767e'))
        canvas.drawString(38,22,'Brick Atlas | '+('最终报告' if data['complete'] else '进行中快照'))
        canvas.drawRightString(A4[0]-38,22,str(doc.page))
    path=OUT/'report.pdf'
    SimpleDocTemplate(str(path),pagesize=A4,leftMargin=38,rightMargin=38,topMargin=32,bottomMargin=38,
        title='Brick Atlas 静态与动态扩展实验',author='Brick Atlas').build(story,onFirstPage=footer,onLaterPages=footer)
    print('PDF',path,flush=True)


if __name__=='__main__':main()
