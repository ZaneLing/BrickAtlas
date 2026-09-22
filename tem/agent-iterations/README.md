# 双 agent 研究迭代

用户要求以两个独立角色反复审稿、实质修订、验证和同步，直到达到内部 accept 标准。
这是内部模拟审稿，不代表 CVPR 官方接收。

- **CVPR 审核 agent**：[角色](../../.trae/skills/cvpr-reviewer/SKILL.md)，独立评判，不修改研究文件。
- **研究精进 agent**：[角色](../../.trae/skills/research-refiner/SKILL.md)，实现数据、评估和论文修订，不改审稿结论。
- 主 agent 负责逐轮报告、文件验证和 Git 同步。

完整规则见 [PROTOCOL.md](PROTOCOL.md)，当前状态见 [state.json](state.json)。
审稿按“实验已完成”的假设进行，但不假定结果有利，也不将假设写成实测数据。
所有实测待填单元格继续保持空白。

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
