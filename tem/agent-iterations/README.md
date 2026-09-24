# 双 agent 研究迭代

用户要求以两个独立角色反复审稿、实质修订、验证和同步，直到达到内部 accept 标准。
这是内部模拟审稿，不代表 CVPR 官方接收。

- **CVPR 审核 agent**：[角色](../../.trae/skills/cvpr-reviewer/SKILL.md)，独立评判，不修改研究文件。
- **研究精进 agent**：[角色](../../.trae/skills/research-refiner/SKILL.md)，实现数据、评估和论文修订，不改审稿结论。
- 主 agent 负责逐轮报告、文件验证和 Git 同步。

完整规则见 [PROTOCOL.md](PROTOCOL.md)，当前状态见 [state.json](state.json)。
审稿按“实验已完成”的假设进行，但不假定结果有利，也不将假设写成实测数据。
所有实测待填单元格继续保持空白。

| 轮次 | 独立结论 | 修订与复审 |
|---|---|---|
| [第 1 轮](round-01/report.md) | Reject，3/10；5 个 major | 建立 84 个构造、1,008 条观察的视觉绑定与最小修复任务，补齐对照、语义评分及论文 |
| [第 2 轮](round-02/report.md) | Weak Reject，5/10；1 个 major、1 个 minor | 实现同题联合统计、配对差值、共同资格子集和失败诊断；56 项测试通过 |
| [第 3 轮](round-03/report.md) | Accept，7/10；0 个未解决问题 | 六个历史问题全部独立关闭；接受范围和非阻塞限制见 [终审](round-03/review.md) |

接受的研究版本为 `39e92789f2b64f34dbcfc118a2feb9e4439c951b`，
研究快照为 `6a52785ffaaae16e4e14b249289759a36243c15b94f2aa23a1b481230dc355e7`。
第三轮不再修改研究内容；最终提交只归档评审、答复和验证记录。

每个 `round-NN/` 保存评审所针对的文件哈希、独立审稿、逐条答辩、修改清单、
验证结果和中文轮次报告。成功结束需要至少 7/10、无关键/主要遗留问题，
并通过最后一个研究快照的一致性核验。

```sh
python3 tem/agent-iterations/snapshot.py N
python3 tem/agent-iterations/audit.py
python3 tem/agent-iterations/snapshot.py N --verify
python3 tem/agent-iterations/audit.py --require-accept
```

`snapshot.py` 拒绝覆盖旧轮次快照；每次重新评审都创建新轮次。
旧评审不可回写为接受，新修订必须接受独立复审。

最终 `audit.py --require-accept` 会重新计算整份研究快照，并逐文件核对
当前 Git HEAD 中的内容；未提交或审稿后发生变化的研究文件不能通过验收。

目录整理后，旧快照继续绑定当时的提交，不把移动后的工作区视为重新通过审稿。
使用以下命令检查封存接受记录和该提交内的全部原始字节：

```sh
python3 tem/agent-iterations/audit.py --require-accept --archived-commit 39e92789f2b64f34dbcfc118a2feb9e4439c951b
```

当前目录完整性由 [迁移验证](../repository-layout-20260924/README.md) 单独检查。
