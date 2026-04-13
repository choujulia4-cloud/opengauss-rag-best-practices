```json
{
  "document_type": "eval",
  "test_stage_type": "generate",
  "chunk_method": "mark",
  "max_length": 200,
  "overlap": 50,
  "sim_operator": "inner_product",
  "embed_model": "HuggingFace DPR",
  "llm_model": "phi",
  "original_file": "/raw/rag_results_top.txt"
}
```

# eval_generate_mark_200_50_top1_dpr_phi.md

## 配置参数

| key | value |
|---|---|
| document_type | eval |
| test_stage_type | generate |
| chunk_method | mark |
| max_length | 200 |
| overlap | 50 |
| sim_operator | inner_product |
| embed_model | HuggingFace DPR |
| llm_model | phi |
| original_file | /raw/rag_results_top.txt |

### 原始评价

---
title: Top-1 Comparison Summary
experiment_type: eval
chunk_method: mark
max_length: 200
overlap: 50
sim_operator: inner_product
embed_model: dpr-question_encoder-single-nq-base / dpr-ctx_encoder-single-nq-base
llm_model: phi-3.5-mini-instruct
date: 20260408
original_file: rag_results_top.txt
original_path: \docs\rag_results_top.txt
normalized_from: "mixed_file_split"
---

# Top-1 Comparison Summary

## 配置参数

| key | value |
|---|---|
| config | mark_200_50 |
| compared_top_k | Top-1 vs Top-3 vs Top-5 |
| sim_operator | `<#>` |
| llm_model | phi-3.5-mini-instruct |

## 原始内容
| 指标 | Top-1 (本次) | Top-3 (之前) | Top-5 (之前) | 趋势 |
|---|---|---|---|---|
| retrieval_top1_hit | 61.1% | 61.1% | 66.7% | 持平 |
| answer_correct (平均分) | 0.78 / 2 (39%) | 1.50 / 2 (75%) | 1.61 / 2 (80.5%) | 大幅下降 |
| answer_grounded | 0.83 / 2 (41.5%) | 1.78 / 2 (89%) | 1.94 / 2 (97%) | 大幅下降 |
| answer_complete | 0.78 / 2 (39%) | 1.56 / 2 (78%) | 1.67 / 2 (83.5%) | 大幅下降 |
| hallucination rate | 0% | 0% | 0% | 持平 |

检索-生成分离分析（Top-1）

纯 Retrieval fault：约 9 条（50%）——Top-1 信息量严重不足，导致大量 query 生成模型直接拒答（“does not contain enough information”）
纯 Generation fault：约 3 条（16.7%）
混合 fault：约 6 条
完全成功：约 5 条（27.8%）

核心结论：
使用 Top-1 后，系统表现大幅退化。虽然检索 Top-1 hit 率和 Top-3 差不多，但由于上下文信息严重减少，生成模型（即使是 Phi-3.5-mini-instruct）也无法产出高质量答案，大量出现“信息不足”拒答或极简回答。
4. 总体评价总结
Top-1 的效果明显不如 Top-3 和 Top-5，整体质量下降非常显著。

积极方面：
幻觉率依然为 0%，模型依然“老实”。
部分定义类和对比类问题（Query 2、4、8、13、16）在 Top-1 下仍能给出较好答案，说明 Phi-3.5-mini-instruct 的 instruction following 能力确实强。

主要问题：
检索信息量不足是致命伤：大量 query 的 Top-1 只包含一句话，导致生成模型频繁输出“information not enough”或非常简短的答案。
answer_correct 从 Top-5 的 80.5% 暴跌至 39%，answer_complete 也从 83.5% 跌至 39%。
这再次证明：在当前知识库下，Top-3 或 Top-5 是必要的，Top-1 过于激进。


最终推荐配置（目前最优）：

chunk：mark_200_50
算子：<#>
Top-k：Top-4 或 Top-5（平衡质量与速度）
生成模型：Phi-3.5-mini-instruct
prompt：你当前使用的优化版本
