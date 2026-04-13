```json
{
  "document_type": "review",
  "test_stage_type": "retrieval",
  "chunk_method": "mixed",
  "max_length": "mixed",
  "overlap": 10,
  "sim_operator": "na",
  "embed_model": "HuggingFace DPR",
  "llm_model": "na",
  "original_file": "/raw/retrieval_results.txt"
}
```

# review_retrieval_mixed_dpr_na.md

## 配置参数

| key | value |
|---|---|
| document_type | review |
| test_stage_type | retrieval |
| chunk_method | mixed |
| max_length | mixed |
| overlap | 10 |
| sim_operator | na |
| embed_model | HuggingFace DPR |
| llm_model | na |
| original_file | /raw/retrieval_results.txt |

---
title: Retrieval Experiment 1 Chunk Comparison
experiment_type: mixed
chunk_method: mixed
max_length: mixed
overlap: 10
sim_operator: null
embed_model: null
llm_model: null
date: 20260408
original_file: retrieval_results.txt
original_path: \docs\retrieval_results.txt
normalized_from: "mixed_file_split"
---

# Retrieval Experiment 1 Chunk Comparison

## 配置参数

| key | value |
|---|---|
| experiment | 实验一 |
| compared_configs | mark_150_10, mark_200_10, mark_200_50 |
| focus | max_chunk_size / overlap 对 retrieval 的影响 |
| source | 原始实验一部分 |

## 原始内容
====== 实验一：三种 max_chunk_size & overlap 组合的 retrieval 效果 =====

| Query (问题) | Config | Top-1 Text 开头关键词 | Manual Hit | 说明 |  |
|---|---|---|---|---|---|
| What role does OpenGauss play in a RetrievalQA pipeline? | mark_150_10 | "In a RetrievalQA pipeline | the database is not only..." | 1 | 非常直接，几乎是定义句 |
| What role does OpenGauss play in a RetrievalQA pipeline? | mark_200_10 | "In a RetrievalQA pipeline | the database is not only..." | 1 | 同上，更完整上下文 |
| What role does OpenGauss play in a RetrievalQA pipeline? | mark_200_50 | "In a RetrievalQA pipeline | the database is not only..." | 1 | 同上 |
| Why must long source documents be divided into smaller chunks? | mark_150_10 | These documents are often too long to be embedded directly | 1 | 精确命中原因句 |  |
| Why must long source documents be divided into smaller chunks? | mark_200_10 | These documents are often too long to be embedded directly | 1 | 更完整（包含“Chunking strategy has a direct influence...”） |  |
| Why must long source documents be divided into smaller chunks? | mark_200_50 | These documents are often too long to be embedded directly | 1 | 同上 |  |
| What are the two embedding sources mentioned in this project? | mark_150_10 | embedding generation on a separate machine. | 0 | 完全无关 |  |
| What are the two embedding sources mentioned in this project? | mark_200_10 | The best configuration depends on... After chunking... | 0 | 依然无关 |  |
| What are the two embedding sources mentioned in this project? | mark_200_50 | The best configuration depends on... After chunking... | 0 | 依然无关 |  |
| What does BentoML do in this project? | mark_150_10 | BentoML turns the pipeline into a reusable service. | 1 | 非常精准 |  |
| What does BentoML do in this project? | mark_200_10 | BentoML turns the pipeline into a reusable service. | 1 | 同上 |  |
| What does BentoML do in this project? | mark_200_50 | BentoML turns the pipeline into a reusable service. | 1 | 同上 |  |
| Why is RK3568 considered a resource-constrained edge device? | mark_150_10 | "Finally | the RK3568 deployment target introduces..." | 0.5 | 提到 RK3568 + constraints，但没直接说“resource-constrained”原因 |
| Why is RK3568 considered a resource-constrained edge device? | mark_200_10 | The RK3568 platform is a typical resource-constrained... | 1 | 直接命中定义句，非常好 |  |
| Why is RK3568 considered a resource-constrained edge device? | mark_200_50 | The RK3568 platform is a typical resource-constrained... | 1 | 同上 |  |
| What tasks should be completed on a stronger machine instead of the edge device? | mark_150_10 | This division of labor reduces memory pressure... | 0.5 | 提到 division of labor，但没明确说“stronger machine”完成什么 |  |
| What tasks should be completed on a stronger machine instead of the edge device? | mark_200_10 | The edge device then focuses on online query handling... | 0.5 | 反向描述 edge 做什么，需推导才能知道 preprocessing 放 stronger machine |  |
| What tasks should be completed on a stronger machine instead of the edge device? | mark_200_50 | The edge device then focuses on online query handling... | 0.5 | 同上 |  |
| What are the main differences between HuggingFace embeddings and Cohere embeddings? | mark_150_10 | "Therefore | choosing between HuggingFace and Cohere is..." | 0.5 | 提到 trade-off，但差异描述不完整（top-3 才出现更直接的对比句） |
| What are the main differences between HuggingFace embeddings and Cohere embeddings? | mark_200_10 | "Therefore | choosing between HuggingFace and Cohere is..." | 0.5 | 同上，top-3 和 top-4 才有更清晰差异描述 |
| What are the main differences between HuggingFace embeddings and Cohere embeddings? | mark_200_50 | "Therefore | choosing between HuggingFace and Cohere is..." | 0.5 | 同上 |
| Why should retrieval evaluation be separated from generation evaluation? | mark_150_10 | Retrieval evaluation asks whether the database returns... | 0.5 | 描述了 retrieval evaluation 做什么，但没直接解释“why separate” |  |
| Why should retrieval evaluation be separated from generation evaluation? | mark_200_10 | A practical RetrievalQA system should separate... | 1 | 直接命中“should separate”那句，且紧跟解释 |  |
| Why should retrieval evaluation be separated from generation evaluation? | mark_200_50 | A practical RetrievalQA system should separate... | 1 | 同上 |  |
| What dimensions should be tested systematically for best-practice exploration? | mark_150_10 | This combination of system design... meaningful. | 0 | 几乎无关 |  |
| What dimensions should be tested systematically for best-practice exploration? | mark_200_10 | These dimensions together form the basis... | 0.5 | 提到“these dimensions”，但没列出具体是哪些（需看上下文） |  |
| What dimensions should be tested systematically for best-practice exploration? | mark_200_50 | These dimensions together form the basis... | 0.5 | 同上 |  |
| What is the recommended minimal solution for RK3568 according to the text? | mark_150_10 | "Finally | the RK3568 deployment target introduces..." | 0.5 | 提到 minimal / stable，但真正的推荐句在 top-4 |
| What is the recommended minimal solution for RK3568 according to the text? | mark_200_10 | "Finally | the RK3568 deployment target introduces..." | 0 | top-4 才有推荐句，但 top-1 偏远 |
| What is the recommended minimal solution for RK3568 according to the text? | mark_200_50 | "Finally | the RK3568 deployment target introduces..." | 0 | 同上 |
| What metadata fields are recommended for the OpenGauss embedding table? | mark_150_10 | "When storing embeddings in OpenGauss | the schema design..." | 0.5 | 提到 schema design，但没列具体字段（真正的字段描述在原文更前面） |
| What metadata fields are recommended for the OpenGauss embedding table? | mark_200_10 | OpenGauss is an enterprise-grade relational database... | 0 | 完全无关 |  |
| What metadata fields are recommended for the OpenGauss embedding table? | mark_200_50 | OpenGauss is an enterprise-grade relational database... | 0 | 完全无关 |  |
| Why should similarity operator selection be included in best-practice exploration? | mark_150_10 | "For this reason | similarity operator selection should be..." | 1 | 精确命中 |
| Why should similarity operator selection be included in best-practice exploration? | mark_200_10 | "For this reason | similarity operator selection should be..." | 1 | 同上 |
| Why should similarity operator selection be included in best-practice exploration? | mark_200_50 | "For this reason | similarity operator selection should be..." | 1 | 同上 |

-----------------------------------------------------
== 总结：仅基于 top-1 hit 率
- mark_150_10：整体 hit 率偏低（很多 0 或 0.5），小 chunk 导致上下文丢失严重，尤其对需要比较、列表、原因解释的问题。
- mark_200_10 和 mark_200_50：明显更好，定义类、直接原因类、过程类问题 top-1 hit 率很高。
- overlap 50 vs 10：在这些问题上差异不大（top-1 经常相同或非常相似），说明在这个知识库中 10 token 已经能较好捕捉关键句，但 50 可能在边界情况更有优势（未在此体现）。
- 最弱的问题类型：列举类（two embedding sources、dimensions、metadata fields、recommended solution）→ 小 chunk 几乎全 miss，200 也经常 miss top-1。
- 最强的问题类型：定义/作用/为什么做某事（直接原因） → 几乎全 hit，尤其 200 系列。

-----------------------------------------------------

--------------------------------------------------------------------------------
--------------------------------------------------------------------------------
