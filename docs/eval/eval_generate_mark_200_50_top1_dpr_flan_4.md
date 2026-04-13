```json
{
  "document_type": "eval",
  "test_stage_type": "generate",
  "chunk_method": "mark",
  "max_length": 200,
  "overlap": 50,
  "sim_operator": "l2_distance",
  "embed_model": "HuggingFace DPR",
  "llm_model": "flan",
  "original_file": "/raw/rag_results_-阶段一.csv"
}
```

# eval_generate_mark_200_50_top1_dpr_flan_4.md

## 配置参数

| key | value |
|---|---|
| document_type | eval |
| test_stage_type | generate |
| chunk_method | mark |
| max_length | 200 |
| overlap | 50 |
| sim_operator | l2_distance |
| embed_model | HuggingFace DPR |
| llm_model | flan |
| original_file | /raw/rag_results_-阶段一.csv |

### 原始评价

---
title: Top-5 Mark 200-50 L2 Distance DPR Flan-T5-Base Evaluation
experiment_type: eval
chunk_method: mark
max_length: 200
overlap: 50
sim_operator: l2_distance
embed_model: dpr-question_encoder-single-nq-base / dpr-ctx_encoder-single-nq-base
llm_model: flan-t5-base
date: 20260408
original_file: rag_results_-阶段一.csv
original_path: \docs\rag_results_-阶段一.csv
normalized_from: "mixed_file_split"
---

# Top-5 Mark 200-50 L2 Distance DPR Flan-T5-Base Evaluation

## 配置参数

| key | value |
|---|---|
| config | mark_200_50 |
| top_k | 5 |
| sim_operator | `<->` |
| embed_model | dpr-question_encoder-single-nq-base / dpr-ctx_encoder-single-nq-base |
| llm_model | flan-t5-base |
| source | 原始人工评分表部分 |

## 原始评价内容

| Query 序号 | Query 简写 | retrieval_top1_hit | retrieval_top3_hit | answer_correct | answer_grounded | answer_complete | hallucination | 备注（关键问题点） |
|---:|---|---:|---:|---:|---:|---:|---:|---|
| 1 | OpenGauss role in RetrievalQA | 1 | 1 | 1 | 2 | 1 | 0 | 答案截断，只提 storing，未覆盖完整定义 |
| 2 | Why divide long documents | 1 | 1 | 1 | 2 | 1 | 0 | 答案极简“To be embedded directly”，缺失原因解释 |
| 3 | Two embedding sources | 0 | 0 | 0 | 0 | 0 | 1 | 答案完全无关（说 document chunking...），有幻觉 |
| 4 | BentoML role | 1 | 1 | 1 | 2 | 1 | 0 | 答案完整但偏短，未提 package logic 全貌 |
| 5 | Why RK3568 resource-constrained | 1 | 1 | 0 | 1 | 0 | 0 | 答案错位，回答了 experiments 而非原因 |
| 6 | Tasks on stronger machine | 0 | 1 | 0 | 1 | 0 | 0 | 答案反向（说 edge 做什么），严重错位 |
| 7 | Differences HF vs Cohere | 0 | 1 | 2 | 2 | 2 | 0 | 检索 top-1 miss，但 top-3 覆盖核心，生成完美 |
| 8 | Why separate retrieval & generation eval | 1 | 1 | 0 | 1 | 0 | 0 | 答案“A practical RetrievalQA system”太泛，无 why |
| 9 | Dimensions for best-practice | 0 | 0 | 0 | 0 | 0 | 0 | 答案“top-1 hit rate...”完全无关 |
| 10 | Recommended minimal for RK3568 | 0 | 0 | 0 | 0 | 0 | 0 | 答案“stable”无意义 |
| 11 | Metadata fields recommended | 0 | 0 | 0 | 0 | 0 | 0 | 答案“structure of the source document...”完全错位 |
| 12 | Why similarity operator in best-practice | 1 | 1 | 0 | 1 | 0 | 0 | 答案“fixed too early”只截取后半句，无前因 |
| 13 | Deployment adv/disadv HF vs Cohere | 0 | 1 | 2 | 2 | 2 | 0 | top-1 miss，但 top-3 覆盖，生成完美 |
| 14 | Why large-scale on stronger machine | 0 | 0 | 0 | 0 | 0 | 0 | 答案“reduces local computation pressure”只截取后半句 |
| 15 | Four main deliverables | 0 | 0 | 0 | 0 | 0 | 0 | 答案“[iii]”无意义 |
| 16 | Why include chunk/overlap in metadata | 0 | 1 | 0 | 1 | 0 | 0 | 答案错位，回答了 experiments 而非 why |
| 17 | Why BentoML as service layer not embedding | 1 | 1 | 0 | 1 | 0 | 0 | 答案“both stages should be evaluated independently”无关 |
| 18 | Benefits of storing text + vectors in OpenGauss | 0 | 1 | 1 | 2 | 1 | 0 | 答案部分对，但不完整 |
