```json
{
  "document_type": "review",
  "test_stage_type": "retrieval",
  "chunk_method": "mark",
  "max_length": 200,
  "overlap": "mixed",
  "sim_operator": "na",
  "embed_model": "HuggingFace DPR",
  "llm_model": "na",
  "original_file": "/raw/retrieval_results.txt"
}
```

# review_retrieval_mark_200_mixed_dpr_na.md

## 配置参数

| key | value |
|---|---|
| document_type | review |
| test_stage_type | retrieval |
| chunk_method | mark |
| max_length | 200 |
| overlap | mixed |
| sim_operator | na |
| embed_model | HuggingFace DPR |
| llm_model | na |
| original_file | /raw/retrieval_results.txt |

---
title: Retrieval Experiment 4 Overlap Boundary Analysis
experiment_type: overlap
chunk_method: mark
max_length: 200
overlap: mixed
sim_operator: null
embed_model: null
llm_model: null
date: 20260408
original_file: retrieval_results.txt
original_path: \docs\retrieval_results.txt
normalized_from: "mixed_file_split"
---

# Retrieval Experiment 4 Overlap Boundary Analysis

## 配置参数

| key | value |
|---|---|
| experiment | 实验四 |
| compared_overlap | 0, 10, 50, 100 |
| focus | 边界敏感问题的 overlap 影响 |
| source | 原始实验四与边界优势量化总结部分 |

## 原始内容
====== 实验四：overlap 边界敏感实验 =====
--------------------------------------------------------------------------------
        "What are the deployment advantages and disadvantages of using HuggingFace local embeddings versus Cohere hosted embeddings?",
        "Why does the project recommend performing large-scale document chunking, bulk embedding generation, and batch insertion on a stronger machine rather than on the RK3568 edge device?",
        "According to the text, what are the four main forms of deliverables that the final project output should include?",
        "Why does the text suggest including both chunk size and overlap size in the metadata fields of the embedding table?",
        "In this project, why does BentoML serve as the application service layer rather than as an embedding model itself?",
        "What benefits does using OpenGauss provide by storing both the original text content and the embedding vectors in a RetrievalQA pipeline?"

| 问题序号 | 问题简写（英文） | mark_200_100 top-1 Text 开头 | Hit (100) | mark_200_50 top-1 Text 开头 | Hit (50) | mark_200_10 top-1 Text 开头 | Hit (10) | mark_200_0 top-1 Text 开头 | Hit (0) | 边界覆盖情况总结 |  |  |  |  |  |  |  |  |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Deployment adv/disadv HF vs Cohere | A local HuggingFace embedding model may be suitable... while Cohere may be more practical... | 1 | A local HuggingFace embedding model may be suitable... while Cohere may be more practical... | 1 | "HuggingFace local embeddings provide more deployment autonomy | while Cohere..." | 1 | "HuggingFace local embeddings provide more deployment autonomy | while Cohere..." | 1 | 全配置 top-1 都完整覆盖前后两句，overlap 无明显差异 |  |  |  |  |  |  |
| 2 | Why large-scale chunking/embedding on stronger machine | The RK3568 platform is a typical resource-constrained... not ideal for large embedding models... | 0.5 | The edge device then focuses on... This division of labor reduces memory pressure... | 0.5 | The edge device then focuses on... This division of labor reduces memory pressure... | 0.5 | The edge device then focuses on... This division of labor reduces memory pressure... | 0.5 | 全配置 top-1 均为后半句（division of labor），前半句（push offline to stronger）在 100/50 中 top-3 才出现 → overlap 帮助有限 |  |  |  |  |  |  |  |  |
| 3 | Four main forms of deliverables | The final project output should include several forms of deliverables. The first is a markdown deployment guide... | 1 | Such conclusions are more valuable... The final project output should include several forms of deliverables. | 0.5 | Such conclusions are more valuable... The final project output should include several forms of deliverables. | 0.5 | Such conclusions are more valuable... The final project output should include several forms of deliverables. | 0.5 | 只有 100 overlap top-1 完整列出第一项，其他配置 top-1 只提到“several forms”而未展开 → overlap 100 边界优势明显 |  |  |  |  |  |  |  |  |
| 4 | Why include chunk size & overlap size in metadata | "In practice | chunk size and chunk overlap should be treated as tunable parameters..." | 0.5 | Common choices include chunk sizes... with overlaps ranging from zero to one hundred. | 0.5 | Common choices include chunk sizes... with overlaps ranging from zero to one hundred. | 0.5 | Common choices include chunk sizes... with overlaps ranging from zero to one hundred. | 0.5 | 全配置 top-1 均为“tunable parameters”或“common choices”，但未覆盖“why”（好处句在原文更后） → overlap 帮助不大 |  |  |  |  |  |  |  |
| 5 | Why BentoML as service layer not embedding model | "This is especially useful... In the context of this project | BentoML serves as the application service layer rather than as an embedding model itself." | 1 | "In the context of this project | BentoML serves as the application service layer rather than as an embedding model itself." | 1 | "In the context of this project | BentoML serves as the application service layer rather than as an embedding model itself." | 1 | "In the context of this project | BentoML serves as the application service layer rather than as an embedding model itself." | 1 | 全配置 top-1 都直接命中核心定义句 + 上下文，overlap 无差异 |  |  |  |  |
| 6 | Benefits of storing text + vectors in OpenGauss | "In a RetrievalQA pipeline | the database is not only responsible for storing original text chunks | but also for storing the embedding vectors..." | 1 | "In a RetrievalQA pipeline | the database is not only responsible for storing original text chunks | but also for storing the embedding vectors..." | 1 | "In a RetrievalQA pipeline | the database is not only responsible for storing original text chunks | but also for storing the embedding vectors..." | 1 | "In a RetrievalQA pipeline | the database is not only responsible for storing original text chunks | but also for storing the embedding vectors..." | 1 | 全配置 top-1 完全相同且完美，overlap 无影响 |

==== 键观察与边界优势量化总结 ====
== 整体 Boundary Hit Rate（top-1 完整覆盖边界两侧的比率）：
- mark_200_100：4/6 = 66.7%（问题 1、3、5、6 满分）
- mark_200_50：3/6 = 50%
- mark_200_10：3/6 = 50%
- mark_200_0：3/6 = 50%

== overlap 带来的明显提升点（只在 overlap=100 时出现）：
- 问题 3（four deliverables）：只有 100 overlap 的 top-1 直接展开了“the first is a markdown deployment guide”，其他配置停留在“several forms”泛化句 → 边界跨段落列表类问题，大 overlap 成功救回完整信息。
- 问题 2（stronger machine 原因）：100 overlap 让 top-1 至少提到“not ideal for large embedding models”，更接近前半句，但仍未完整覆盖“push offline” → 提升有限。

== overlap 无效或差异小的点：
- 问题 1、5、6：核心句本身较独立，overlap 大小不影响 top-1。
- 问题 4：原因解释句在原文位置较分散，即使 100 overlap 也只召回“tunable parameters”而非完整好处。

== 结论性洞察（可直接用于报告）：
* 当答案信息天然跨自然段或列表边界时（如 deliverables 列表），overlap=100 能显著提升 top-1 完整率（从 50% → 66.7%），尤其在“列出多项”或“前后因果紧邻”场景。
* 对于半句前后依赖的问题（如 stronger machine 的“push offline + division of labor”），overlap 增加只能让 top-1 更接近前半句，但无法完全覆盖两句 → 需要结合 Parent-Child 或更大 chunk。
* overlap=50 vs 10 vs 0 在这些边界问题上差异很小（几乎持平），说明在 200 token 规模下，50 已接近饱和，100 才有额外收益。
* 推荐结论：在资源允许时，优先使用 overlap ≥ 50–100 处理技术文档/部署指南类知识库（边界敏感高）；若计算成本敏感，可保持 overlap=50 作为折中。
