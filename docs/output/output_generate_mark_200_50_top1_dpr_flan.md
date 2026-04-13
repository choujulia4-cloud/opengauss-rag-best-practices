```json
{
  "document_type": "output",
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

# output_generate_mark_200_50_top1_dpr_flan.md

## 配置参数

| key | value |
|---|---|
| document_type | output |
| test_stage_type | generate |
| chunk_method | mark |
| max_length | 200 |
| overlap | 50 |
| sim_operator | cosine |
| embed_model | HuggingFace DPR |
| llm_model | flan |
| original_file | /raw/rag_results_=-阶段一.csv |

### 原始终端输出

```text
---
title: Top-5 Mark 200-50 Cosine DPR Flan-T5-Base Experiment Output
experiment_type: similarity
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

# Top-5 Mark 200-50 Cosine DPR Flan-T5-Base Experiment Output

## 配置参数

| key | value |
|---|---|
| config | mark_200_50 |
| top_k | 5 |
| sim_operator | `<=>` |
| embed_model | dpr-question_encoder-single-nq-base / dpr-ctx_encoder-single-nq-base |
| llm_model | flan-t5-base |
| source | 原始终端输出部分 |

## 原始终端输出
================= Retrival Logs =================
Config: mark_200_50
Query: What role does OpenGauss play in a RetrievalQA pipeline?
Operator: <=>
Retrieval Time: 9.6906 seconds
== Rand 1: Distance/Score = 0.329345327016081 | Text = In a RetrievalQA pipeline, the database is not only responsible for storing original text chunks, but also for storing the embedding vectors that represent the semantic meaning of those chunks. 
== Rand 2: Distance/Score = 0.365273214113402 | Text = A typical RetrievalQA workflow contains several stages. The first stage is raw document preparation. 
== Rand 3: Distance/Score = 0.384691611838669 | Text = OpenGauss is an enterprise-grade relational database that can also be used as a vector store for retrieval-augmented generation systems. 
== Rand 4: Distance/Score = 0.386323553860279 | Text = HuggingFace, Cohere, and BentoML each play different roles in the system. OpenGauss provides the persistent vector storage and retrieval backbone. 
== Rand 5: Distance/Score = 0.412585909679588 | Text = A practical RetrievalQA system should separate retrieval evaluation from generation evaluation. Retrieval evaluation asks whether the database returns the correct or at least useful chunks. 
-- Connection to OpenGauss established sucessfully --
-- Generate query embedding with shape: torch.Size([768]) --
Generate_Time: 3.9146742820739746 seconds
Answer [1]: storing original text chunks
============================================
-- Connection to OpenGauss established sucessfully --
-- Generate query embedding with shape: torch.Size([768]) --
================= Retrival Logs =================
Config: mark_200_50
Query: Why must long source documents be divided into smaller chunks?
Operator: <=>
Retrieval Time: 0.3558 seconds
== Rand 1: Distance/Score = 0.31923553415309 | Text = These documents are often too long to be embedded directly, so they must be divided into smaller chunks. Chunking strategy has a direct influence on retrieval quality. 
== Rand 2: Distance/Score = 0.414412343622839 | Text = The first stage is raw document preparation. Source documents may come from manuals, technical reports, markdown files, project notes, or deployment guides. 
== Rand 3: Distance/Score = 0.424544314562541 | Text = The first dimension is chunking strategy. Fixed-length chunking is simple and easy to reproduce, but sentence-based or punctuation-based chunking may better preserve semantic boundaries. 
== Rand 4: Distance/Score = 0.42684339615239 | Text = Large-scale document chunking, bulk embedding generation, and batch insertion can be completed on a development workstation or server. 
== Rand 5: Distance/Score = 0.431465820696155 | Text = If chunks are too short, important context may be lost. If chunks are too long, retrieval may become noisy because a returned chunk can contain both relevant and irrelevant content. 
Generate_Time: 0.3333766460418701 seconds
Answer [2]: To be embedded directly
============================================
-- Connection to OpenGauss established sucessfully --
-- Generate query embedding with shape: torch.Size([768]) --
================= Retrival Logs =================
Config: mark_200_50
Query: What are the two embedding sources mentioned in this project?
Operator: <=>
Retrieval Time: 0.3515 seconds
== Rand 1: Distance/Score = 0.322256521826108 | Text = The best configuration depends on the structure of the source document and the nature of the user queries. After chunking, the next stage is embedding generation. 
== Rand 2: Distance/Score = 0.331440335314995 | Text = However, model size, inference latency, and memory usage can become critical on resource-constrained devices. Cohere embeddings, in contrast, are generated by calling a remote API. 
== Rand 3: Distance/Score = 0.336013773412766 | Text = In the context of this project, BentoML serves as the application service layer rather than as an embedding model itself. 
== Rand 4: Distance/Score = 0.351933699380951 | Text = The first dimension is chunking strategy. Fixed-length chunking is simple and easy to reproduce, but sentence-based or punctuation-based chunking may better preserve semantic boundaries. 
== Rand 5: Distance/Score = 0.352243233211838 | Text = When storing embeddings in OpenGauss, the schema design should support not only vector search, but also experiment traceability. 
Generate_Time: 0.7013535499572754 seconds
Answer [3]: document chunking, embedding generation, vector retrieval, and end-to-end question answering
============================================
-- Connection to OpenGauss established sucessfully --
-- Generate query embedding with shape: torch.Size([768]) --
================= Retrival Logs =================
Config: mark_200_50
Query: What does BentoML do in this project?
Operator: <=>
Retrieval Time: 0.3553 seconds
== Rand 1: Distance/Score = 0.278420001304794 | Text = BentoML turns the pipeline into a reusable service. 
== Rand 2: Distance/Score = 0.280964292583572 | Text = In the context of this project, BentoML serves as the application service layer rather than as an embedding model itself. 
== Rand 3: Distance/Score = 0.313928333962795 | Text = Therefore, both stages should be evaluated independently. BentoML can be used to package the retrieval and question answering logic as a deployable service. 
== Rand 4: Distance/Score = 0.324980764817903 | Text = Instead of exposing raw Python scripts, the engineer can define a service interface such as ask(query: str) and let BentoML handle model packaging, dependency management, and API serving. 
== Rand 5: Distance/Score = 0.358545493817141 | Text = A practical RetrievalQA system should separate retrieval evaluation from generation evaluation. Retrieval evaluation asks whether the database returns the correct or at least useful chunks. 
Generate_Time: 0.4850938320159912 seconds
Answer [4]: turns the pipeline into a reusable service
============================================
-- Connection to OpenGauss established sucessfully --
-- Generate query embedding with shape: torch.Size([768]) --
================= Retrival Logs =================
Config: mark_200_50
Query: Why is RK3568 considered a resource-constrained edge device?
Operator: <=>
Retrieval Time: 0.3527 seconds
== Rand 1: Distance/Score = 0.354460285131168 | Text = The RK3568 platform is a typical resource-constrained edge device. 
== Rand 2: Distance/Score = 0.39892714158698 | Text = Finally, the RK3568 deployment target introduces real-world constraints that force the system toward a minimal, stable, and well-justified implementation. 
== Rand 3: Distance/Score = 0.414027906845924 | Text = However, model size, inference latency, and memory usage can become critical on resource-constrained devices. Cohere embeddings, in contrast, are generated by calling a remote API. 
== Rand 4: Distance/Score = 0.433207815364293 | Text = It is also important to test deployment paths in a realistic environment. Some components that work on a standard x86 server may require simplification on an AArch64 board. 
== Rand 5: Distance/Score = 0.443369539938868 | Text = The edge device then focuses on online query handling, vector retrieval, and lightweight response assembly. This division of labor reduces memory pressure and improves stability. 
Generate_Time: 0.40349626541137695 seconds
Answer [5]: real-world constraints
============================================
-- Connection to OpenGauss established sucessfully --
-- Generate query embedding with shape: torch.Size([768]) --
================= Retrival Logs =================
Config: mark_200_50
Query: What tasks should be completed on a stronger machine instead of the edge device?
Operator: <=>
Retrieval Time: 0.3576 seconds
== Rand 1: Distance/Score = 0.338183877639154 | Text = The edge device then focuses on online query handling, vector retrieval, and lightweight response assembly. This division of labor reduces memory pressure and improves stability. 
== Rand 2: Distance/Score = 0.358467277782339 | Text = Finally, the RK3568 deployment target introduces real-world constraints that force the system toward a minimal, stable, and well-justified implementation. 
== Rand 3: Distance/Score = 0.36534353876253 | Text = On RK3568, the recommended minimal solution may be to deploy OpenGauss and a lightweight service endpoint locally, while performing large-scale embedding generation on a separate machine. 
== Rand 4: Distance/Score = 0.398931459958913 | Text = It also matches realistic edge deployment patterns where the edge node provides fast local search while heavy model computation remains centralized. 
== Rand 5: Distance/Score = 0.427792217607238 | Text = Large-scale document chunking, bulk embedding generation, and batch insertion can be completed on a development workstation or server. 
Generate_Time: 0.8366992473602295 seconds
Answer [6]: online query handling, vector retrieval, and lightweight response assembly
============================================
-- Connection to OpenGauss established sucessfully --
-- Generate query embedding with shape: torch.Size([768]) --
================= Retrival Logs =================
Config: mark_200_50
Query: What are the main differences between HuggingFace embeddings and Cohere embeddings?
Operator: <=>
Retrieval Time: 0.3497 seconds
== Rand 1: Distance/Score = 0.275253399449024 | Text = Therefore, choosing between HuggingFace and Cohere is not only a question of retrieval accuracy, but also a question of deployment constraints, response latency, operating cost, and system autonomy. 
== Rand 2: Distance/Score = 0.28379876605143 | Text = HuggingFace models are suitable when local execution and offline control are important. 
== Rand 3: Distance/Score = 0.297774272541424 | Text = A local HuggingFace embedding model may be suitable for offline experimentation, while Cohere may be more practical for remote or hybrid deployments. 
== Rand 4: Distance/Score = 0.299802487220278 | Text = The second dimension is embedding backend. HuggingFace local embeddings provide more deployment autonomy, while Cohere embeddings may provide higher convenience or better hosted performance. 
== Rand 5: Distance/Score = 0.333676312644682 | Text = The third dimension is similarity calculation and retrieval configuration. Different vector distance operators may produce different nearest neighbors even when the same embeddings are used. 
Generate_Time: 0.7311892509460449 seconds
Answer [7]: HuggingFace local embeddings provide more deployment autonomy, while Cohere embeddings may provide higher convenience or better hosted performance
============================================
-- Connection to OpenGauss established sucessfully --
-- Generate query embedding with shape: torch.Size([768]) --
================= Retrival Logs =================
Config: mark_200_50
Query: Why should retrieval evaluation be separated from generation evaluation?
Operator: <=>
Retrieval Time: 0.3542 seconds
== Rand 1: Distance/Score = 0.412585909679588 | Text = A practical RetrievalQA system should separate retrieval evaluation from generation evaluation. Retrieval evaluation asks whether the database returns the correct or at least useful chunks. 
== Rand 2: Distance/Score = 0.418747271284912 | Text = Therefore, both stages should be evaluated independently. BentoML can be used to package the retrieval and question answering logic as a deployable service. 
== Rand 3: Distance/Score = 0.424263993573527 | Text = This separation helps engineers understand whether a wrong final answer comes from missing context, poor retrieval ranking, or weak answer synthesis. 
== Rand 4: Distance/Score = 0.433084813980637 | Text = Conversely, a strong language model may sometimes produce a plausible answer even when retrieval is poor, which can hide defects in the retrieval layer. 
== Rand 5: Distance/Score = 0.44329523178683 | Text = It is therefore important to test the same set of questions under different combinations of chunking strategy, embedding backend, retrieval settings, and generation model. 
Generate_Time: 0.5303854942321777 seconds
Answer [8]: Retrieval evaluation asks whether the database returns the correct or at least useful chunks
============================================
-- Connection to OpenGauss established sucessfully --
-- Generate query embedding with shape: torch.Size([768]) --
================= Retrival Logs =================
Config: mark_200_50
Query: What dimensions should be tested systematically for best-practice exploration?
Operator: <=>
Retrieval Time: 0.3571 seconds
== Rand 1: Distance/Score = 0.351944381586559 | Text = The third dimension is similarity calculation and retrieval configuration. Different vector distance operators may produce different nearest neighbors even when the same embeddings are used. 
== Rand 2: Distance/Score = 0.356697564621039 | Text = These dimensions together form the basis of a best-practice report rather than isolated coding experiments. A good test knowledge base should support multiple question types. 
== Rand 3: Distance/Score = 0.36053563588213 | Text = The first dimension is chunking strategy. Fixed-length chunking is simple and easy to reproduce, but sentence-based or punctuation-based chunking may better preserve semantic boundaries. 
== Rand 4: Distance/Score = 0.363724370630675 | Text = The fifth dimension is deployment target. A workflow that runs smoothly on a high-memory x86 server may not be practical on a low-memory AArch64 board. 
== Rand 5: Distance/Score = 0.365553463794209 | Text = The second dimension is embedding backend. HuggingFace local embeddings provide more deployment autonomy, while Cohere embeddings may provide higher convenience or better hosted performance. 
Generate_Time: 0.5389132499694824 seconds
Answer [9]: chunking strategy
============================================
-- Connection to OpenGauss established sucessfully --
-- Generate query embedding with shape: torch.Size([768]) --
================= Retrival Logs =================
Config: mark_200_50
Query: What is the recommended minimal solution for RK3568 according to the text?
Operator: <=>
Retrieval Time: 0.3646 seconds
== Rand 1: Distance/Score = 0.39892714158698 | Text = Finally, the RK3568 deployment target introduces real-world constraints that force the system toward a minimal, stable, and well-justified implementation. 
== Rand 2: Distance/Score = 0.405437045636871 | Text = On RK3568, the recommended minimal solution may be to deploy OpenGauss and a lightweight service endpoint locally, while performing large-scale embedding generation on a separate machine. 
== Rand 3: Distance/Score = 0.419769672063093 | Text = The fifth dimension is deployment target. A workflow that runs smoothly on a high-memory x86 server may not be practical on a low-memory AArch64 board. 
== Rand 4: Distance/Score = 0.429149733583596 | Text = Such conclusions are more valuable than raw benchmark tables because they can guide future engineering decisions. The final project output should include several forms of deliverables. 
== Rand 5: Distance/Score = 0.429327288423733 | Text = The fourth is a community contribution package, such as a pull request or technical write-up, that makes the results reproducible for other developers interested in OpenGauss-based retrieval systems. 
Generate_Time: 0.24820399284362793 seconds
Answer [10]: stable
============================================
-- Connection to OpenGauss established sucessfully --
-- Generate query embedding with shape: torch.Size([768]) --
================= Retrival Logs =================
Config: mark_200_50
Query: What metadata fields are recommended for the OpenGauss embedding table?
Operator: <=>
Retrieval Time: 0.3517 seconds
== Rand 1: Distance/Score = 0.277749399839632 | Text = OpenGauss is an enterprise-grade relational database that can also be used as a vector store for retrieval-augmented generation systems. 
== Rand 2: Distance/Score = 0.320400487651256 | Text = HuggingFace, Cohere, and BentoML each play different roles in the system. OpenGauss provides the persistent vector storage and retrieval backbone. 
== Rand 3: Distance/Score = 0.322256521826108 | Text = The best configuration depends on the structure of the source document and the nature of the user queries. After chunking, the next stage is embedding generation. 
== Rand 4: Distance/Score = 0.322471375088272 | Text = On RK3568, the recommended minimal solution may be to deploy OpenGauss and a lightweight service endpoint locally, while performing large-scale embedding generation on a separate machine. 
== Rand 5: Distance/Score = 0.331440335314995 | Text = However, model size, inference latency, and memory usage can become critical on resource-constrained devices. Cohere embeddings, in contrast, are generated by calling a remote API. 
Generate_Time: 0.7147719860076904 seconds
Answer [11]: HuggingFace, Cohere, and BentoML
============================================
-- Connection to OpenGauss established sucessfully --
-- Generate query embedding with shape: torch.Size([768]) --
================= Retrival Logs =================
Config: mark_200_50
Query: Why should similarity operator selection be included in best-practice exploration?
Operator: <=>
Retrieval Time: 0.3569 seconds
== Rand 1: Distance/Score = 0.228732924680018 | Text = For this reason, similarity operator selection should be part of the best-practice exploration rather than being fixed too early. 
== Rand 2: Distance/Score = 0.348511264964113 | Text = Typical indicators include top-1 hit rate, top-3 hit rate, mean reciprocal rank, and average retrieval latency. 
== Rand 3: Distance/Score = 0.351944381586559 | Text = Conversely, a strong language model may sometimes produce a plausible answer even when retrieval is poor, which can hide defects in the retrieval layer. 
== Rand 4: Distance/Score = 0.353083918728291 | Text = Therefore, choosing between HuggingFace and Cohere is not only a question of retrieval accuracy, but also a question of deployment constraints, response latency, operating cost, and system autonomy. 
== Rand 5: Distance/Score = 0.356697564621039 | Text = These dimensions together form the basis of a best-practice report rather than isolated coding experiments. A good test knowledge base should support multiple question types. 
Generate_Time: 0.3626070022583008 seconds
Answer [12]: being fixed too early
============================================
-- Connection to OpenGauss established sucessfully --
-- Generate query embedding with shape: torch.Size([768]) --
================= Retrival Logs =================
Config: mark_200_50
Query: What are the deployment advantages and disadvantages of using HuggingFace local embeddings versus Cohere hosted embeddings?
Operator: <=>
Retrieval Time: 0.3539 seconds
== Rand 1: Distance/Score = 0.263588779808512 | Text = A local HuggingFace embedding model may be suitable for offline experimentation, while Cohere may be more practical for remote or hybrid deployments. 
== Rand 2: Distance/Score = 0.272397803159744 | Text = The second dimension is embedding backend. HuggingFace local embeddings provide more deployment autonomy, while Cohere embeddings may provide higher convenience or better hosted performance. 
== Rand 3: Distance/Score = 0.275253399449024 | Text = Therefore, choosing between HuggingFace and Cohere is not only a question of retrieval accuracy, but also a question of deployment constraints, response latency, operating cost, and system autonomy. 
== Rand 4: Distance/Score = 0.28379876605143 | Text = HuggingFace models are suitable when local execution and offline control are important. 
== Rand 5: Distance/Score = 0.298955241218754 | Text = HuggingFace, Cohere, and BentoML each play different roles in the system. OpenGauss provides the persistent vector storage and retrieval backbone. 
Generate_Time: 1.3590073585510254 seconds
Answer [13]: HuggingFace local embeddings provide more deployment autonomy, while Cohere embeddings may provide higher convenience or better hosted performance
============================================
-- Connection to OpenGauss established sucessfully --
-- Generate query embedding with shape: torch.Size([768]) --
================= Retrival Logs =================
Config: mark_200_50
Query: Why does the project recommend performing large-scale document chunking, bulk embedding generation, and batch insertion on a stronger machine rather than on the RK3568 edge device?
Operator: <=>
Retrieval Time: 0.4188 seconds
== Rand 1: Distance/Score = 0.30945282860264 | Text = Finally, the RK3568 deployment target introduces real-world constraints that force the system toward a minimal, stable, and well-justified implementation. 
== Rand 2: Distance/Score = 0.316800565462866 | Text = This reduces local computation pressure and can simplify deployment on lightweight edge devices, but it requires network access and external service credentials. 
== Rand 3: Distance/Score = 0.31690674986074 | Text = The edge device then focuses on online query handling, vector retrieval, and lightweight response assembly. This division of labor reduces memory pressure and improves stability. 
== Rand 4: Distance/Score = 0.318790730963182 | Text = It also makes it easier to run controlled experiments because the retrieval result can be linked back to the exact preprocessing configuration used when the chunk was inserted into the database. 
== Rand 5: Distance/Score = 0.321855576251688 | Text = For deployment on AArch64 platforms, such as RK3568 boards, containerization becomes even more important because it reduces manual configuration drift across devices. 
Generate_Time: 0.5229840278625488 seconds
Answer [14]: reduces manual configuration drift across devices
============================================
-- Connection to OpenGauss established sucessfully --
-- Generate query embedding with shape: torch.Size([768]) --
================= Retrival Logs =================
Config: mark_200_50
Query: According to the text, what are the four main forms of deliverables that the final project output should include?
Operator: <=>
Retrieval Time: 0.3576 seconds
== Rand 1: Distance/Score = 0.293955901255181 | Text = Such conclusions are more valuable than raw benchmark tables because they can guide future engineering decisions. The final project output should include several forms of deliverables. 
== Rand 2: Distance/Score = 0.357443001895657 | Text = Therefore, the final deployment plan should distinguish between what is validated in a development environment and what is realistic on the target board. 
== Rand 3: Distance/Score = 0.36193799533498 | Text = Even in a prototype stage, a clean project structure with separate modules for chunking, embedding, database access, retrieval, and service packaging greatly improves maintainability. 
== Rand 4: Distance/Score = 0.372873741424701 | Text = The first stage is raw document preparation. Source documents may come from manuals, technical reports, markdown files, project notes, or deployment guides. 
== Rand 5: Distance/Score = 0.384473781153584 | Text = Finally, the RK3568 deployment target introduces real-world constraints that force the system toward a minimal, stable, and well-justified implementation. 
Generate_Time: 0.3353428840637207 seconds
Answer [15]: raw document preparation
============================================
-- Connection to OpenGauss established sucessfully --
-- Generate query embedding with shape: torch.Size([768]) --
================= Retrival Logs =================
Config: mark_200_50
Query: Why does the text suggest including both chunk size and overlap size in the metadata fields of the embedding table?
Operator: <=>
Retrieval Time: 0.3566 seconds
== Rand 1: Distance/Score = 0.295612563208219 | Text = For example, a certain chunk size may work best for technical manuals, while a different overlap may help with fragmented deployment notes. 
== Rand 2: Distance/Score = 0.29768022639858 | Text = Common choices include chunk sizes of one hundred, three hundred, or five hundred words or tokens, with overlaps ranging from zero to one hundred. 
== Rand 3: Distance/Score = 0.329962900697347 | Text = In practice, chunk size and chunk overlap should be treated as tunable parameters. 
== Rand 4: Distance/Score = 0.333579808183217 | Text = The first dimension is chunking strategy. Fixed-length chunking is simple and easy to reproduce, but sentence-based or punctuation-based chunking may better preserve semantic boundaries. 
== Rand 5: Distance/Score = 0.347590361846582 | Text = A practical table may include the original text content, the embedding vector, document identifier, chunk identifier, source file name, embedding model name, chunk size, overlap size, and creation 
Generate_Time: 0.7079646587371826 seconds
Answer [16]: chunk size and overlap should be treated as tunable parameters
============================================
```
