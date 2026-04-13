```json
{
  "document_type": "eval",
  "test_stage_type": "generate",
  "chunk_method": "mark",
  "max_length": 200,
  "overlap": 50,
  "sim_operator": "inner_product",
  "embed_model": "HuggingFace DPR",
  "llm_model": "flan vs phi",
  "original_file": "/raw/rag_results.txt"
}
```

# eval_generate_mark_200_50_dpr_flan_vs_phi.md

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
| llm_model | flan vs phi |
| original_file | /raw/rag_results.txt |

### 原始评价

---
title: RAG Stage 3 Generator Comparison Summary
experiment_type: eval
chunk_method: mark
max_length: 200
overlap: 50
sim_operator: inner_product
embed_model: HuggingFace DPR
llm_model: mixed
date: 20260408
original_file: rag_results.txt
original_path: \docs\rag_results.txt
normalized_from: "mixed_file_split"
---

# RAG Stage 3 Generator Comparison Summary

## 配置参数

| key | value |
|---|---|
| stage | 阶段三 |
| focus | flan-t5-base vs Phi-3.5-mini-instruct |
| source | 原始文件阶段三部分 |

## 原始内容
【阶段三】更换模型 Phi-3.5-mini-instruct
| 指标 | flan-t5-base (<#>) | Phi-3.5-mini (<#>) | 变化 |
|---|---|---|---|
| retrieval_top1_hit | 66.7% | 66.7% | 不变 |
| retrieval_top3_hit | 88.9% | 88.9% | 不变 |
| answer_correct (平均分) | 0.94 / 2 (47%) | 1.61 / 2 (80.5%) | 大幅提升 +33.5% |
| answer_grounded | 1.67 / 2 (83.3%) | 1.94 / 2 (97%) | 大幅提升 |
| answer_complete | 0.78 / 2 (39%) | 1.67 / 2 (83.5%) | 大幅提升 +44.5% |
| hallucination rate | 5.6% | 0% | 完全消除 |
| 平均 Generate_Time | ~1.0s | ~23–27s | 显著变慢 |

检索-生成分离分析
纯 Retrieval fault：约 3 条（16.7%）——主要是列表类和部分边界问题
纯 Generation fault：约 2 条（11.1%）——生成质量已大幅改善
混合 fault：约 2 条
完全成功率：约 11 条（61%）——相比 flan-t5-base 的 11% 有巨大进步

Phi-3.5-mini-instruct 在生成质量上提升非常明显，尤其是回答的完整性、细节丰富度和逻辑连贯性。从 flan-t5-base 的“关键词式回答”变成了“完整自然段回答”。大部分 query 的答案已经达到了可以直接使用的水平，hallucination 也彻底消失。
主要代价是生成速度大幅变慢（在你的 CPU 上从 1 秒级变成 20+ 秒级），这进一步验证了生成模型不适合直接放在 RK3588 上跑。
