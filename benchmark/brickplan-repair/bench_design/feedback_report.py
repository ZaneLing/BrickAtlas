"""Export the A-feedback repair report and actual rendered source examples."""
from pathlib import Path
import hashlib,shutil
from bench_design import ROOT
from bench_design.challenges import QUALITY
from bench_design.review_server import Server
from bench_design.source_expansion import OUT,index
from bench_design.quality_report import FAMILIES
from expansion_v7.build import read,write


def main():
    server=Server(('127.0.0.1',0),Path('/tmp/brick-gt-feedback-final'))
    evidence=read(QUALITY/'feedback-preview-validation.json')
    assert evidence['status']=='PASS' and evidence['version']==server.gt.version
    native=read(OUT/'native-replay-check.json');geometry=read(OUT/'independent-geometry-check.json')
    visibility=read(OUT/'visibility-check.json');provenance=read(OUT/'provenance-check.json')
    assert visibility['allVisible'] and geometry['allAgreed'] and provenance['status']=='PASS'
    assets=OUT/'examples';assets.mkdir(exist_ok=True)
    lines=['# A反馈后的修复：放大位置、三个角度、更多不同物件','',
        '更新：2026-10-27。**本轮没有调用付费模型，API费用为 $0。**','',
        '[打开A检查页](http://127.0.0.1:8808/A) · [直接看新增机器人](http://127.0.0.1:8808/A?task=N003) · [B入口](http://127.0.0.1:8808/B) · [C入口](http://127.0.0.1:8808/C)','',
        '## 1. A的反馈，以及本次改了什么','',
        'A共提交71题：50题选GT正确，20题选看不清，1题选GT有问题。原记录完整保留。新版默认列出这21道待复查题，加上20道新物件示例，共41题；原来的其他题仍在“全部题目”里。','',
        '| 问题 | 已做的修改 |','|---|---|',
        '| 大房子、大建筑看不清操作位置 | 默认放大本题修复位置；旁边给整件物品小图，用青框标出放大的区域；可随时点“看整体”。场景里的其他零件仍参与遮挡。 |',
        '| 一个角度被挡住 | 同时列出三个立体角度缩略图；初始选择更能看出变化的一侧；当前、GT结果、目标同步换角度和比例。 |',
        '| 拆完好像没拆，步骤看不明白 | 点任一步，直接并排看操作前和操作后；只在实际移动件所在的那一侧描边。每一步继续放大该操作件周围。 |',
        '| Q003书架的GT有异议 | 修复了阶段识别：这题只要求第7步的7块状态，不要求装成完整21块书架。10个参考拆装动作另做独立几何复核，均一致；仍保留A的异议，等待真人复查。 |',
        '| 反复审同一个物件 | 新增10个不同来源物件的收尾模块，每个只做5个case，审查页各展示1静态、1动态。 |',
        '| 程序说有错，图却一样 | 新增可见性筛查。狮子最初选到的转向错误三个角度都无变化，已换成另一处真正可见、可合法修回的转向错误。 |','',
        '**页面仍然只需要选一个：GT正确 / GT有问题 / 看不清或无法判断。无需拼装，也无需写文字。**','',
        '![白宫：放大修复位置与三个角度](feedback-interface-evidence/white-house-closeup.png)','',
        '![书架：操作前、操作后并排检查](feedback-interface-evidence/step-before-after.png)','',
        '### 21道待复查题','',
        '以下不是“自动判为修好了”。程序与画面已更新，是否足够清楚、GT是否可信，仍由新的真人提交确认。','',
        '| 题号 | 物件 | A上次判断 | 本次复查重点 |','|---|---|---|---|']
    feedback=read(QUALITY/'A-feedback-resolution.json')
    for row in feedback['rows']:
        if row['choice']=='correct':continue
        code=row['code'];bundle=server.gt.bundle(code)
        focus='第7步目标；拆上层、换内部件、装回' if code=='Q003' else '无错题允许不操作；看清当前阶段' if code=='Q014' else '放大的修复位置、三个角度及操作前后'
        lines.append(f'| [{code}](http://127.0.0.1:8808/A?task={code}) | {bundle["title"]} | {"GT有问题" if row["choice"]=="problem" else "看不清"} | {focus} |')
    lines+=['','## 2. 新增10个不同物件','',
        '这些物件来自[LDraw官方模型库](https://library.ldraw.org/omr)。完整原模型都保留在场景中；题目让模型完成明确的收尾部分，例如车顶、鹿角和驾驶舱。**这次新增的是10个有完整物件背景的收尾模块，不是10套从零搭完整套装的任务。**','',
        '其中6个源文件是本轮新下载，另4个来自此前已保存的社区源文件。这里的“新增”指新增可操作的模块；同一套装可能在旧静态库出现过，划分训练、调试、测试时继续按原套装合并分组。','',
        '| 物件／LDraw套装 | 完整源模型件数 | 本题操作件数 | 两种错误 | 真人示例 |','|---|---:|---:|---|---|']
    models=index()['models'];tasks=read(OUT/'review-tasks.json')['tasks'];byid={r['caseId']:r['code'] for r in tasks}
    for m in models:
        st=byid[f'QN:{m["id"]}::static::{m["preferredFamily"]}'];dy=byid[f'QN:{m["id"]}::dynamic::{m["preferredFamily"]}']
        lines.append(f'| [{m["title"]} · {m["sourceSetId"]}]({m["source"]["url"]}) | {m["sourceParts"]} | {m["activeParts"]} | 少件；{FAMILIES[m["preferredFamily"]]} | [静态{st}](http://127.0.0.1:8808/A?task={st}) / [动态{dy}](http://127.0.0.1:8808/A?task={dy}) |')
    lines+=['','每个物件只有5个case：1个正常拼装、2个静态修复、2个动态干扰修复。共50个case：20静态、30动态（其中10个无干扰对照）。各题每次只装或拆一块；GT只是一种合法修法，换合法顺序、同种零件换编号，不按中间顺序判错。','',
        '### 输入、输出和难度','',
        '| 项目 | 内容 |','|---|---|',
        '| 静态输入 | 已经出现错误的当前状态、本题阶段目标、可用零件；可按需看说明和位置预览。未来成品不是本题目标。 |',
        '| 动态输入 | 已搭好的主体、待完成模块目标、可用零件；逐件操作，每步能看实际状态，过程中发生一次未提示的变化。 |',
        '| 模型输出 | inspect查看，attach安装，detach拆下，finish结束。每次最多改变一块。 |',
        '| GT与评分 | 每次操作合法，结束状态与本题目标物理等价。没触发事故的运行单列，不算修复失败；修复主结论还需要正常分支成功。 |',
        '| 这批的级别 | 模块5–12块，参考局部修复1–2步，一次事故；属于短模块、短返修。补的是物件多样性，不能据此声称补足高难度。原有长过程、内部返修、多次事故仍保留。 |','',
        '**真人GT检查页额外展示答案、修复位置和更有帮助的初始角度。这些提示只用于检查题目，不会偷偷放入模型输入，也不能当作真人盲做成功率。**','',
        '## 3. 每个物件的实际图与case','',
        '图片直接由本题原始几何状态渲染。完整成品用于认识物件；静态题右图是当前阶段目标，可能还没有装完收尾部分。点击图片可查看原分辨率。']
    for i,m in enumerate(models,1):
        folder=OUT/'models'/m['id'];cases=read(folder/'cases.private.json.gz')
        st=byid[f'QN:{m["id"]}::static::{m["preferredFamily"]}'];dy=byid[f'QN:{m["id"]}::dynamic::{m["preferredFamily"]}']
        view=server.gt.default_view(st)
        for name,path in [('whole',server.gt.image(dy,'goal','isometric',scope='whole')),('current',server.gt.image(st,'current',view)),('target',server.gt.image(st,'goal',view))]:
            shutil.copyfile(path,assets/f'{m["id"]}-{name}.png')
        lines+=['',f'### {i}. {m["title"]}','',m['module']+'。','',
            '| 完整物件 | 本题当前状态（局部） | 本题阶段目标／GT结果（局部） |','|---|---|---|',
            '| '+' | '.join(f'![{name}](source-expansion/examples/{m["id"]}-{key}.png)' for name,key in [('完整物件','whole'),('当前状态','current'),('本题目标','target')])+' |','',
            '| case后缀 | 题型 | 开始状态／干扰位置 | GT参考动作数 |','|---|---|---|---:|']
        for c in cases:
            events=c.get('referenceEvents',[])
            detail=f'修到说明第{c["completedInstructionStep"]}步的目标' if c['mode']=='static' else f'正常参考路线装到{c["events"][0]["minimumInstalled"]}块后出现变化' if events else '主体预装好，从收尾模块起点完成'
            lines.append(f'| `{c["mode"]}::{c["family"]}` | {"静态修复" if c["mode"]=="static" else "动态修复" if events else "正常对照"} | {detail} | {len(c["referenceActions"])} |')
        lines+=['',f'完整case ID前缀：`QN:{m["id"]}::`。作者：{m["source"]["author"]}。原文件许可：{m["source"]["license"]}。']
    lines+=['','## 4. 已检查到哪一步，还有什么不能宣称','',
        f'- 新增50个case全部通过实际运行器回放；20次动态事故确实发生。没有付费模型成绩。',
        f'- 新增静态GT共{len(geometry["checks"])}个拆装动作，用另一套布尔几何算法复核，结论均与运行器一致。范围只含这些参考动作，不代表所有候选动作均被独立穷举验证，也不模拟摩擦、卡扣力度或真实手部操作。',
        '- 20个静态错误在三个审查角度中至少一面可见；普通模型输入的模块图也通过可见差异筛查。筛查只检查图像是否存在足够差异，不代替真人判断。',
        '- 新增动态题在实际发生事故时再次检查可见性，换合法顺序也适用；没有合适的可见错误时延后触发，最终未触发则保持单独统计。',
        '- 91个人工检查页面的GT均能正常回放，待复查项与新增示例的画面已逐项检查可见差异。原有正确对照允许图像一致。',
        '- 新增物件的源文件、模型清单和依赖零件哈希均核对一致；原作者和许可保留，源几何未修改。',
        '- A原来的71份GT提交仍然保留。新版本还没有真人重新确认，21道问题题和20道新增例子仍待检查。',
        '- 旧物理抽查P024（关联Q021熊猫）仍缺少可靠的背景碰撞信息，不能宣称已经解决。',
        '- 原正式目录仍为5,720题（5,452主任务、268诊断）。本轮50个新增case单独存放，等待真人检查后再决定纳入；不把扩充数字冒充已验证题数。','',
        '### 可追溯记录','',
        '[A逐题反馈](A-feedback-resolution.json) · [50题回放](source-expansion/native-replay-check.json) · [独立几何](source-expansion/independent-geometry-check.json) · [可见性](source-expansion/visibility-check.json) · [来源核验](source-expansion/provenance-check.json) · [91题预览核验](feedback-preview-validation.json) · [Q003复核](q003-feedback-audit.json)','']
    (QUALITY/'A-FEEDBACK-REPAIRS.zh-CN.md').write_text('\n'.join(lines))
    server.server_close()


if __name__=='__main__':main()
