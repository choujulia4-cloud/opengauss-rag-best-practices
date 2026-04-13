```json
{
  "document_type": "eval",
  "test_stage_type": "generate",
  "chunk_method": "mark",
  "max_length": 200,
  "overlap": 50,
  "sim_operator": "cosine",
  "embed_model": "HuggingFace DPR",
  "llm_model": "flan",
  "original_file": "/raw/rag_results_=-阶段一.csv"
}
```

# eval_generate_mark_200_50_top1_dpr_flan.md

## 配置参数

| key | value |
|---|---|
| document_type | eval |
| test_stage_type | generate |
| chunk_method | mark |
| max_length | 200 |
| overlap | 50 |
| sim_operator | cosine |
| embed_model | HuggingFace DPR |
| llm_model | flan |
| original_file | /raw/rag_results_=-阶段一.csv |

### 原始评价

---
title: Top-5 Mark 200-50 Cosine DPR Flan-T5-Base Evaluation
experiment_type: eval
chunk_method: mark
max_length: 200
overlap: 50
sim_operator: cosine
embed_model: dpr-question_encoder-single-nq-base / dpr-ctx_encoder-single-nq-base
llm_model: flan-t5-base
date: 20260408
original_file: rag_results_=-阶段一.csv
original_path: \docs\rag_results_=-阶段一.csv
normalized_from: "mixed_file_split"
---

# Top-5 Mark 200-50 Cosine DPR Flan-T5-Base Evaluation

## 配置参数

| key | value |
|---|---|
| config | mark_200_50 |
| top_k | 5 |
| sim_operator | `<=>` |
| embed_model | dpr-question_encoder-single-nq-base / dpr-ctx_encoder-single-nq-base |
| llm_model | flan-t5-base |
| source | 原始人工评分表部分 |

## 原始评价内容

| Query 序号 | Query 简写 | retrieval_top1_hit | retrieval_top3_hit | answer_correct | answer_grounded | answer_complete | hallucination | 备注（关键问题点） |
|---:|---|---:|---:|---:|---:|---:|---:|---|
| 1 | OpenGauss role in RetrievalQA | 1 | 1 | 1 | 2 | 1 | 0 | 答案截断，只提 storing，未覆盖完整定义 |
| 2 | Why divide long documents | 1 | 1 | 1 | 2 | 1 | 0 | 答案极简“To be embedded directly”，缺失原因 |
| 3 | Two embedding sources | 0 | 0 | 0 | 0 | 0 | 1 | 答案无关（document chunking...），有幻觉 |
| 4 | BentoML role | 1 | 1 | 1 | 2 | 1 | 0 | 答案偏短，未提 package logic 全貌 |
| 5 | Why RK3568 resource-constrained | 1 | 1 | 0 | 1 | 0 | 0 | 答案错位，只说 real-world constraints |
| 6 | Tasks on stronger machine | 0 | 1 | 0 | 1 | 0 | 0 | 答案反向（说 edge 做什么），严重错位 |
| 7 | Differences HF vs Cohere | 1 | 1 | 2 | 2 | 2 | 0 | 检索+生成完美，直接命中核心对比 |
| 8 | Why separate retrieval & generation eval | 1 | 1 | 1 | 2 | 1 | 0 | 答案只提 retrieval eval，未解释 why |
| 9 | Dimensions for best-practice | 0 | 1 | 0 | 1 | 0 | 0 | 答案“chunking strategy”太泛，无实质 |
| 10 | Recommended minimal for RK3568 | 0 | 0 | 0 | 0 | 0 | 0 | 答案“stable”无意义 |
| 11 | Metadata fields recommended | 0 | 0 | 0 | 0 | 0 | 0 | 答案“HuggingFace, Cohere, and BentoML”完全无关 |
| 12 | Why similarity operator in best-practice | 1 | 1 | 0 | 1 | 0 | 0 | 答案“being fixed too early”只截取后半句 |
| 13 | Deployment adv/disadv HF vs Cohere | 1 | 1 | 2 | 2 | 2 | 0 | 完美，直接命中 autonomy vs convenience |
| 14 | Why large-scale on stronger machine | 0 | 1 | 0 | 1 | 0 | 0 | 答案“reduces manual configuration drift”错位 |
| 15 | Four main deliverables | 0 | 0 | 0 | 0 | 0 | 0 | 答案“raw document preparation”完全错位 |
| 16 | Why include chunk/overlap in metadata | 0 | 1 | 1 | 2 | 1 | 0 | 答案部分对，但不完整 |
| 17 | Why BentoML as service layer not embedding | 1 | 1 | 1 | 2 | 1 | 0 | 答案较完整，但未全覆盖说明 |
| 18 | Benefits of storing text + vectors in OpenGauss | 1 | 1 | 1 | 2 | 1 | 0 | 答案部分对，但不完整 |
