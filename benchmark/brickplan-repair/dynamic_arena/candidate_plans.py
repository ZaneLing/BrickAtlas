"""Explicit design queue. Planned conditions never enter the scored catalogue."""
from dynamic_arena import OUT
from expansion_v7.build import read,write
PLANS={
 '4490-1':('飞船两侧机翼收尾','机身预装；只操作两侧完整机翼连接处',['missing','offset'],'先核对铰接位置，转动视角后必须能看到两个连接口。'),
 '30277-1':('歼星舰上层舰桥','舰体预装；补顶部舰桥',['missing','wrong-part'],'灰色表面需局部放大并验证零件边界清楚。'),
 '8028-1':('TIE 飞船侧翼','驾驶舱预装；补两侧翼板',['missing','rotated'],'必须检查侧向连接；对称旋转不能算错。'),
 '20014-1':('越野车车顶','底盘、车轮预装；完成车顶',['missing','offset'],'先验证车顶支撑与返修路径。'),
 '7210-1':('恐龙头颈收尾','身体和四肢预装；完成头颈',['missing','wrong-color'],'原文件有近似旋转矩阵，当前不能当成已验证的刚体姿态。'),
 '20006-1':('履带车顶部炮塔','车体预装；补顶部炮塔',['missing','wrong-part'],'先确认炮塔作为完整可辨认模块且不会遮住修复部位。'),
 '310-3':('拖船驾驶舱顶部','船体预装；完成驾驶舱顶部与仪器',['missing','wrong-color'],'顶部仪器存在倾斜姿态，不能忽略它对拆屋顶的影响。'),
 '42116-1':('装载机驾驶室顶部','底盘与机械臂预装；完成驾驶室顶部',['missing','offset'],'固定机械臂姿态；不声称测试关节连续运动。'),
 '40148-1':('小羊头部收尾','底座与身体预装；完成头部',['missing','wrong-part'],'倾斜姿态与眼睛印刷件必须先通过几何检查。'),
 '5866-1':('救援直升机驾驶舱顶部','机身预装；完成驾驶舱顶部',['missing','wrong-color'],'应放大驾驶舱，排除旋翼遮挡后再确定题目。'),
 '30283-1':('越野车引擎盖','底盘和轮子预装；补引擎盖',['missing','offset'],'固定部分仍参与碰撞检查，不得删除不支持的轮子。'),
}
def main():
 rows=[]
 for m in read(OUT/'source-library.json')['models']:
  if m['setNumber'] not in PLANS:continue
  title,scope,families,blocker=PLANS[m['setNumber']]
  rows.append(dict(setNumber=m['setNumber'],title=title,scope=scope,conditions=['normal-build']+[mode+':'+f for f in families for mode in ['static','dynamic']],status='design-only-not-an-evaluable-case',gt=None,requiredBeforeAdmission=['explicit source indices','legal normal witness','legal repair witness','visible error at input resolution','human review'],openIssue=blocker))
 write(OUT/'candidate-question-designs.json',dict(models=rows,notIncludedInQuestionCounts=True,apiCalls=0))
 p=OUT/'NO-FIGURES-AND-NEW-CASES.zh-CN.md';s=p.read_text();s+='\n## 其余 11 个新来源：已设计方向，尚未作为题目发布\n\n这些只是设计，不含已验证 GT，不算题量。每个物件计划 1 个正常拼装、2 个静态修复、2 个动态修复条件；无法合法构造的条件会放弃。\n\n|来源|要完成的部分|初始状态|先要解决什么|\n|---|---|---|---|\n'
 for r in rows:s+=f"|{r['setNumber']}|{r['title']}|{r['scope']}|{r['openIssue']}|\n"
 p.write_text(s)
if __name__=='__main__':main()
