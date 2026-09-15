# Mechanism-1 模型实测

- 状态：complete
- 错误：无
- 模型：openai/gpt-4.1-mini、google/gemini-2.5-flash
- 请求：96
- 本轮费用：$0.069427
- 累计费用：$3.759386 / $4.50

| 模型 | 任务 | 完成 | 格式正确 | Exact Success | 费用 |
|---|---|---:|---:|---:|---:|
| openai/gpt-4.1-mini | prefix-dynamics | 6 | 6 | 5 | $0.004782 |
| openai/gpt-4.1-mini | insertion-access | 6 | 6 | 3 | $0.005004 |
| openai/gpt-4.1-mini | fault-recovery | 6 | 6 | 0 | $0.004882 |
| openai/gpt-4.1-mini | inventory-substitution | 6 | 6 | 6 | $0.004916 |
| openai/gpt-4.1-mini | dynamic-robustness | 6 | 6 | 5 | $0.004645 |
| openai/gpt-4.1-mini | functional-kinematics | 6 | 6 | 3 | $0.004634 |
| openai/gpt-4.1-mini | active-inspection | 6 | 6 | 4 | $0.004857 |
| openai/gpt-4.1-mini | multiobjective-design | 6 | 6 | 2 | $0.004990 |
| google/gemini-2.5-flash | prefix-dynamics | 6 | 6 | 6 | $0.003810 |
| google/gemini-2.5-flash | insertion-access | 6 | 6 | 3 | $0.003926 |
| google/gemini-2.5-flash | fault-recovery | 6 | 6 | 3 | $0.004134 |
| google/gemini-2.5-flash | inventory-substitution | 6 | 6 | 6 | $0.003818 |
| google/gemini-2.5-flash | dynamic-robustness | 6 | 6 | 2 | $0.003665 |
| google/gemini-2.5-flash | functional-kinematics | 6 | 6 | 3 | $0.003675 |
| google/gemini-2.5-flash | active-inspection | 6 | 6 | 4 | $0.003778 |
| google/gemini-2.5-flash | multiobjective-design | 6 | 6 | 4 | $0.003912 |

结果是固定最小 Harness 下的描述性开发集表现。六个对象、每类六题，不支持显著性排名。
物理 Oracle、原始模型回答和评分结果分别保留在 `run.json`。
