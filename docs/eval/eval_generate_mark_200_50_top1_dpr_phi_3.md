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

# eval_generate_mark_200_50_top1_dpr_phi_3.md

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
title: Top-3 Comparison Summary
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

# Top-3 Comparison Summary

## 配置参数

| key | value |
|---|---|
| config | mark_200_50 |
| compared_top_k | Top-5 vs Top-3 |
| sim_operator | `<#>` |
| llm_model | phi-3.5-mini-instruct |

## 原始内容
终端原始输出：rag_results_#-phi-top3.txt
终端输出评分：rag_results_#-phi-top3.CSV
| 指标 | Top-5 (之前) | Top-3 (本次) | 变化 |
|---|---|---|---|
| retrieval_top1_hit | 66.7% | 61.1% | 轻微下降 |
| retrieval_top3_hit | 88.9% | 72.2% | 明显下降 |
| answer_correct (平均分) | 1.61 / 2 (80.5%) | 1.50 / 2 (75%) | 轻微下降 |
| answer_grounded | 1.94 / 2 (97%) | 1.78 / 2 (89%) | 轻微下降 |
| answer_complete | 1.67 / 2 (83.5%) | 1.56 / 2 (78%) | 轻微下降 |
| hallucination rate | 0% | 0% | 持平 |

检索-生成分离分析（Top-3）
纯 Retrieval fault：约 5 条（27.8%）——主要集中在列表/枚举类（two sources、metadata fields、four deliverables、dimensions、large-scale on stronger）
纯 Generation fault：约 2 条（11.1%）
混合 fault：约 3 条
完全成功：约 8 条（44.4%）
核心结论：
将检索从 Top-5 → Top-3 后，检索质量明显下降（top-3 hit 从 88.9% 掉到 72.2%），导致整体 answer_correct 和 complete 都有小幅回落。但生成模型（Phi-3.5-mini）本身依然表现良好，大部分 query 仍能输出完整、自然的答案。
优点：
生成质量依然远强于 flan-t5-base
幻觉率为 0%，答案逻辑清晰
部分 query（如推荐方案、为什么分离评估、chunk/overlap 原因）回答非常完整且专业
缺点：
Top-3 导致信息覆盖不足，尤其在列表类和跨段落问题上，生成模型开始出现“信息不够”的情况（Query 3、11、15 等）
整体正确率和完整性比 Top-5 低约 5 个百分点

==== 总体评价总结 ==
更换为 Top-3 后，整体效果有小幅退化，但仍在可接受范围内。
积极方面：Phi-3.5-mini-instruct 的生成能力依然优秀，答案长度和逻辑性明显优于 flan-t5-base。即使检索信息减少，它仍然能尽量产出完整句子，而不是关键词。
负面方面：Top-3 导致检索召回的上下文变少，直接影响了列表类、比较类和推荐类问题的表现。检索瓶颈再次凸显。
当前最优配置建议：mark_200_50 + <#> + Top-4 或 Top-5 + Phi-3.5-mini-instruct 是目前平衡质量与速度的最佳组合。
