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
  "original_file": "/raw/rag_results_#-phi-top1.csv"
}
```

# eval_generate_mark_200_50_top1_dpr_phi_2.md

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
| original_file | /raw/rag_results_#-phi-top1.csv |

### 原始评价

---
title: Top-1 Phi-3.5-Mini-Instruct Evaluation
experiment_type: eval
chunk_method: mark
max_length: 200
overlap: 50
sim_operator: inner_product
embed_model: dpr-question_encoder-single-nq-base / dpr-ctx_encoder-single-nq-base
llm_model: phi-3.5-mini-instruct
date: 20260408
original_file: rag_results_#-phi-top1.csv
original_path: \docs\rag_results_#-phi-top1.csv
normalized_from: "direct_standardization"
---

# Top-1 Phi-3.5-Mini-Instruct Evaluation

## 配置参数

| key | value |
|---|---|
| config | mark_200_50 |
| top_k | 1 |
| sim_operator | `<#>` |
| embed_model | dpr-question_encoder-single-nq-base / dpr-ctx_encoder-single-nq-base |
| llm_model | phi-3.5-mini-instruct |

## 原始评价内容

| Query 序号 | Query（简写） | retrieval_top1_hit | answer_correct | answer_grounded | answer_complete | hallucination | 与 Top-3 / Top-5 对比 |
|---|---|---|---|---|---|---|---|
| 1 | OpenGauss role | 1 | 0 | 0 | 0 | 0 | 大幅下降（之前 Top-5/3 均为 2） |
| 2 | Why divide long documents | 1 | 2 | 2 | 2 | 0 | 持平（优秀） |
| 3 | Two embedding sources | 0 | 0 | 0 | 0 | 0 | 持平（仍弱） |
| 4 | BentoML role | 1 | 2 | 2 | 2 | 0 | 持平（优秀） |
| 5 | Why RK3568 resource-constrained | 1 | 0 | 0 | 0 | 0 | 大幅下降 |
| 6 | Tasks on stronger machine | 0 | 1 | 1 | 1 | 0 | 持平 |
| 7 | Differences HF vs Cohere | 1 | 0 | 0 | 0 | 0 | 大幅下降 |
| 8 | Why separate retrieval & generation | 1 | 2 | 2 | 2 | 0 | 持平（优秀） |
| 9 | Dimensions for best-practice | 0 | 0 | 0 | 0 | 0 | 持平（弱） |
| 10 | Recommended minimal for RK3568 | 0 | 0 | 0 | 0 | 0 | 大幅下降 |
| 11 | Metadata fields | 0 | 0 | 0 | 0 | 0 | 持平（弱） |
| 12 | Why similarity operator | 1 | 1 | 2 | 1 | 0 | 轻微下降 |
| 13 | Deployment adv/disadv HF vs Cohere | 1 | 2 | 2 | 2 | 0 | 持平（优秀） |
| 14 | Why large-scale on stronger machine | 0 | 0 | 0 | 0 | 0 | 持平（弱） |
| 15 | Four main deliverables | 0 | 0 | 0 | 0 | 0 | 持平（弱） |
| 16 | Why include chunk/overlap in metadata | 1 | 2 | 2 | 2 | 0 | 持平（优秀） |
| 17 | Why BentoML as service layer | 1 | 0 | 0 | 0 | 0 | 大幅下降 |
| 18 | Benefits of storing text + vectors | 1 | 0 | 0 | 0 | 0 | 大幅下降 |
