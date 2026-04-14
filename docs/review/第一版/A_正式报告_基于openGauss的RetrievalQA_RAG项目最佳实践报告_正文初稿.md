# 基于 openGauss 的 RetrievalQA / RAG 项目最佳实践报告

**项目负责人：朱玲**

---

## 摘要

本项目围绕 openGauss 向量数据库、HuggingFace / DPR embedding、外部检索式 RetrievalQA 与普通生成模型的组合路线展开，目标不是仅验证系统“能否跑通”，而是沉淀一套适用于标准 Linux 开发环境与 AArch64 / RK3568 边缘场景的工程化最佳实践。项目原计划覆盖 openGauss、HuggingFace、Cohere、BentoML、AArch64 容器化部署、检索参数优化与社区输出；而当前阶段已经形成较稳定证据的主线，主要集中在 chunking 收敛、检索算子对比、生成器更换、检索/生成分离评测，以及“开发机完成重处理、边缘端保留最小闭环”的部署判断。fileciteturn7file3 fileciteturn7file10

当前阶段的核心结论如下。第一，chunking 层面，`mark_200_50` 是当前默认主配置，`mark_200_100` 可作为边界增强候选，`mark_150_10` 适合作为小 chunk 对照组；`length` 系列与 `mark_100_10` 则不适合作为主路线。第二，retrieval 层面，在当前 DPR embedding 路线下，`<#>` 是综合最优的相似度算子，`<=>` 居中，`<->` 明显偏弱；定义类、作用类、直接原因类问题检索已较稳定，列表/枚举类、元数据类仍是薄弱环节。第三，端到端 RAG 层面，`flan-t5-base` 已完成闭环验证，但主要短板是答案完整性不足；切换到 `Phi-3.5-mini-instruct` 后，在 correctness、groundedness、completeness 上均有显著提升，但生成耗时从约 1 秒级上升到 20 秒级以上。第四，gold context 上限测试出现了“完美上下文下仍高拒答、局部幻觉与完整性不足”的异常现象，提示当前系统瓶颈已明显转向生成模型本身，同时也可能受到 prompt 形式、chat template 用法与输入组织方式的影响。fileciteturn7file9 fileciteturn7file7

基于当前证据，项目的阶段性推荐配置为：`mark_200_50 + DPR + <#> + Phi-3.5-mini-instruct`，并采用“开发机完成文档切分、embedding 生成与批量入库，边缘端负责在线 query、向量检索与轻量响应组装”的部署思路。需要强调的是，这一结论属于当前阶段的工程收敛结果，而不是对原始申请书所有目标均已完全落地的宣告。fileciteturn7file11 fileciteturn7file13

**关键词：** openGauss；RetrievalQA；RAG；HuggingFace；DPR；Phi-3.5-mini-instruct；AArch64；RK3568

---

## 1. 项目背景与目标

### 1.1 项目背景

随着 LLM 应用逐渐进入企业级知识问答、技术检索与边缘部署场景，向量数据库、embedding 模型、RAG 管线与服务封装的协同设计变得越来越重要。本项目的意义不在于单独验证某一个组件，而在于总结一条可复用的工程路线：在 openGauss 提供的向量存储与检索能力之上，完成文档切分、embedding 生成、向量写库、query 检索、context 构造与生成回答的端到端闭环，并在此基础上给出配置建议与部署判断。知识库文本本身也明确将 openGauss 定位为 RetrievalQA 管线中的持久化向量存储与检索骨架，而非普通的辅助数据库。fileciteturn7file3

### 1.2 原始项目目标

根据申请书，项目原始目标包含四个层面：一是在 AArch64 架构下完成 openGauss、HuggingFace、Cohere、BentoML 的容器化部署与指导文档输出；二是编写 Python 应用代码，实现多种 embedding 路线向 openGauss 写入与检索；三是基于 openGauss 向量存储完成 RetrievalQA 流程的端到端验证；四是形成部署文档、示例代码、最佳实践报告与社区贡献材料。申请书中还提出了诸如 ONNX 轻量化、Optuna 自动调优、Redis 缓存、多平台构建等扩展性目标。当前正式报告会如实承认：这些目标中，已有些形成了明确设计方向，但并非所有项都在本阶段形成了同等强度的实验闭环。fileciteturn5file7

### 1.3 本报告的评测范围

本报告只将“已形成较稳定证据”的内容作为主结论来源，主要覆盖以下五类：其一，chunking 配置的统计与收敛；其二，不同相似度算子与 chunk 配置的 retrieval-only 对比；其三，`flan-t5-base` 与 `Phi-3.5-mini-instruct` 的端到端生成对比；其四，gold context 条件下的生成器上限观察；其五，开发机与 RK3568 边缘端职责划分的工程判断。至于 Cohere 的完整实证、BentoML 的完整服务交付、ONNX / Optuna / Redis 等内容，本报告会在“原计划与实际收敛差异说明”及“后续工作”中保留，但不会将其写成已经完成的主结论。fileciteturn7file12

---

## 2. 系统架构与工程实现

### 2.1 总体架构

当前项目的主链路可以概括为：原始知识文本 → 文档切分 → chunk dataset → DPR context encoder 生成 embedding → openGauss 写库 → DPR question encoder 生成 query embedding → 相似度检索 → 上下文拼接 → 生成模型输出答案。`TextChunker` 在本项目中不仅是一个工具类，也承担了构造实验知识库文本与保存 chunk dataset 的角色；`HFEmbedder` 负责对 chunk dataset 批量生成 embedding；`OPController` 负责连接 openGauss、插入向量与执行 query 检索；`RagPipeline` 将上述链路组装成一个可复用的端到端流程；`test_rag.py` 则充当实验脚本，用于切换 chunk 参数、检索算子、top-k 与生成器配置。fileciteturn7file3 fileciteturn7file11

### 2.2 关键模块说明

`TextChunker` 当前支持 `mark` 与 `length` 两类切分思路，并通过 `max_chunk_size`、`overlap` 和 `cutting_type` 生成对应的 dataset 路径。其内置知识库文本明确包含了本项目想要评测的核心概念：openGauss 的角色、chunking 的作用、HuggingFace 与 Cohere 的差异、embedding 表元数据设计、相似度算子、retrieval / generation 分离、BentoML 的角色、AArch64 / RK3568 的部署约束以及最终交付物形式等，这也是后续 query 设计能够与最佳实践目标紧密对应的原因。fileciteturn7file3

`HFEmbedder` 使用 `facebook/dpr-ctx_encoder-single-nq-base` 及其 tokenizer 对 chunk dataset 执行批量编码，并将带 embedding 的数据集保存到磁盘。`OPController` 负责数据库连接、批量写库与检索。其 query 侧使用 `facebook/dpr-question_encoder-single-nq-base` 生成问题向量，并依据不同 operator 拼装检索 SQL；这意味着当前结论严格绑定于 DPR 这条 embedding 路线，而不应被过度外推为“所有 embedding 模型下都成立”。fileciteturn7file4

`RagPipeline` 将 retrieval operator、top-k 与 generation model_name 暴露为可切换参数，构成了后续实验设计的基础。值得注意的是，`load_generator` 中已经体现出从 seq2seq 模型切到 causal LM / chat 模型的代码演进痕迹：flan 的旧路径被保留为注释，而当前加载逻辑已转向本地的 `Phi-3.5-mini-instruct`。`generate_answer` 也同时保留了多种 prompt 版本，反映出项目在“prompt 微调 vs 更强生成器”之间进行过系统探索。fileciteturn7file11

### 2.3 当前实际主线路线

综合代码、评测文件与对应关系表，当前真正形成主结论的路线可以概括为：`mark` 系列 chunking → DPR embedding → openGauss 检索 → `<#>` 作为主算子 → `mark_200_50` 作为默认主配置 → `Phi-3.5-mini-instruct` 作为新的主生成器路线；而 `flan-t5-base` 则保留为 baseline generator。这条路线是项目在多轮实验后形成的收敛结果，而不是从一开始就预设好的单线方案。fileciteturn7file18

---

## 3. 评测设计与评价标准

### 3.1 评测分层原则

本项目最重要的方法论之一，是明确将 retrieval evaluation 与 generation evaluation 分离。知识库文本已清楚说明：retrieval evaluation 关注数据库是否返回正确或至少有用的 chunk，generation evaluation 关注最终答案是否正确、grounded 且完整；若两者不分离，就容易将生成模型的能力误判为检索系统的能力，或者反过来掩盖检索层缺陷。这个原则最终成为本报告所有主结论的前提。fileciteturn7file10

### 3.2 题集与问题类型

从 `query整合.txt` 与 `query -goldContext.txt` 可以看出，当前实验题集并不是随机提问，而是围绕 RetrievalQA 系统的关键能力设计的。问题大致可分为五类：定义/作用型，如 “OpenGauss 在 RetrievalQA 中扮演什么角色”；直接原因型，如 “为什么长文档必须切块”；对比型，如 “HuggingFace embeddings 与 Cohere embeddings 的差异”；列表/枚举型，如 “四种项目 deliverables”；部署/推荐方案型，如 “RK3568 的推荐最小方案是什么”。这种设计使得不同 chunk 配置、operator、top-k 与生成器配置都能在统一题集上被比较。fileciteturn7file16 fileciteturn7file1

### 3.3 指标定义

本报告沿用项目中已经明确的人工评分标准：`retrieval_top1_hit` 表示 top-1 chunk 是否直接包含核心答案句，`retrieval_top3_hit` 表示 top-3 是否覆盖完整答案；`answer_correct` 取值为 0/1/2，分别表示完全错误、部分正确、完全准确；`answer_grounded` / `faithfulness` 取值为 0/1/2，表示非 grounded、部分 grounded、完全基于检索内容；`answer_complete` 取值为 0/1/2，表示严重缺失、基本覆盖但不完整、完整无遗漏；`hallucination` 取值为 0/1，表示无明显幻觉与存在幻觉。这一评分体系使得 retrieval-only 对比、端到端 RAG 对比、gold context 对比之间具备统一的解释框架。fileciteturn4file4

### 3.4 评测配置说明

当前主要评测轴包括：chunk 配置（`mark_150_10`、`mark_200_10`、`mark_200_50`、边界补测中的 `mark_200_100`）、operator（`<#>`、`<=>`、`<->`）、top-k（至少比较过 top-1 / top-3 / top-5）、生成器（`flan-t5-base` vs `Phi-3.5-mini-instruct`）以及绕过 retrieval 的 gold context direct generation。对应关系表也说明，相关原始文件已被重命名并按 `chunk / mixed / rag / topk / eval / review` 等目录归档，这为正式报告的可追溯性提供了基础。fileciteturn7file18

---

## 4. Chunking 最佳实践

### 4.1 统计结果与总体判断

`split_chunk_results.txt` 已经提供了当前最核心的 chunking 统计依据。第一组对比表明，在当前英文技术知识库下，`length` 系列并不如 `mark` 系列稳定：例如 `length 150 10` 仍存在过短块与超长块，`mark 100 10` 则明显过碎，出现较多过短块与异常长度；而 `mark 200 10` 与 `mark 200 50` 在 `min / max / median / std` 等指标上更均衡。第二组 overlap 对比进一步说明：`mark_150` 在 overlap 增大时会引入更多超长块，而 `mark_200` 在 `0 / 10 / 20 / 50` 不同 overlap 下整体更稳定。基于这些现象，可以较有把握地说：当前最值得继续推进的是 `mark_150_10`、`mark_200_10`、`mark_200_50` 三组，而 `mark_200_50` 是综合表现最均衡的默认主配置。fileciteturn4file24

### 4.2 收敛结论表

| 配置 | 当前定位 | 建议 | 主要理由 |
|---|---|---|---|
| length 系列 | 非主路线 | 不推荐作为主配置 | 在当前知识库下整体不如 mark 稳定 |
| mark_100_10 | 过碎配置 | 排除 | 过短块多，信息容易被切碎 |
| mark_150_10 | 小 chunk 对照组 | 保留 | 某些比较类、部署任务类问题 top-1 更直接 |
| mark_200_10 | 200 系列基线 | 保留 | 统计稳定，适合作为对照基线 |
| mark_200_50 | 默认主配置 | 推荐 | 稳定性、上下文完整性与 retrieval 表现最均衡 |
| mark_200_100 | 边界增强候选 | 条件保留 | 对边界敏感问题更有优势，但不是默认配置 |

### 4.3 代表性现象

边界补测显示，当答案跨自然段或列表边界时，更大的 overlap 才开始体现明显收益。例如 deliverables 这类“列出多项”的问题，在 `overlap=100` 时 top-1 完整率出现提升，而 `50 / 10 / 0` 差异并不大。这说明：对当前 200 token 规模而言，`50` 已经接近普通技术文档的折中点，而 `100` 更适合作为专门处理边界敏感问题的增强候选，而不是直接全面替代 `50`。fileciteturn7file4

### 4.4 阶段性结论

综合统计与 retrieval 表现，当前最稳妥的 chunking 结论是：默认配置采用 `mark_200_50`，同时保留 `mark_150_10` 作为小 chunk 对照、`mark_200_100` 作为边界增强候选。这个结论是“当前阶段最佳折中”，并不排除未来针对不同知识库类型进一步细化条件化推荐。

---

## 5. Retrieval 最佳实践

### 5.1 retrieval-only 对比的总体发现

`retrieval_results.txt` 对当前 retrieval 层提供了比较清晰的证据。其一，在 “三种 max_chunk_size & overlap 组合” 实验中，`mark_200_10` 与 `mark_200_50` 明显优于 `mark_150_10`，尤其在定义类、作用类、直接原因类问题上 top-1 命中率更高；但小 chunk 在个别比较类、部署任务类问题上反而可能更直接，例如 “stronger machine tasks” 这种问法在 `mark_150_10 + <#>` 下 top-1 命中更精确。其二，在 “固定 200 token 规模、更改 overlap 与相似度算子” 实验中，`<#>` 在比较类、推荐/部署类问题上最不容易完全 miss，`<->` 则在多个问题上更偏向召回包装性总结句。其三，列表/枚举类、元数据类问题在三种算子下都偏弱，说明这类问题的主要瓶颈不是算子本身，而是信息分散与 chunk 边界。fileciteturn4file25

### 5.2 当前主算子结论

从当前证据看，`<#>` 是 DPR 路线下最值得继续推进的主算子。其优势体现在：top-1 与 top-3 命中总体最好，对比较类与推荐/部署类问题更稳，且在端到端 RAG 对比中对应的 answer_correct、groundedness 与 completeness 也是三种算子里最优。相比之下，`<=>` 居中，可作为参考对照；`<->` 则在本知识库下明显更弱，不适合作为主算子继续推进。fileciteturn4file26

### 5.3 算子对比表

| 维度 | `<#>` | `<=>` | `<->` | 当前结论 |
|---|---|---|---|---|
| retrieval_top1_hit | 最优 | 中等 | 最弱 | `<#>` 当前最佳 |
| retrieval_top3_hit | 最优 | 次之 | 最弱 | `<#>` 更适合作主算子 |
| 比较类问题 | 较强 | 中等 | 偏弱 | `<#>` 优势更明显 |
| 推荐/部署类问题 | 较强 | 中等 | 偏弱 | `<#>` 更不易完全 miss |
| 列表/元数据类 | 全弱 | 全弱 | 全弱 | 主要瓶颈不在算子本身 |

### 5.4 retrieval 层局限

需要特别强调的是：当前 retrieval 层并非“已经完美”。例如 “two embedding sources”“metadata fields”“four deliverables”“dimensions for best-practice exploration” 这类答案天然分散、需要整合多个片段的问题，即使更换算子或加大 top-k，也未必能在 top-1 直接命中完整答案。因此，正式报告不应把 `<#>` 解释为“万能算子”，而应写成“在当前 DPR + 当前知识库 + 当前 query 集合下的阶段性最优选择”。fileciteturn4file25

---

## 6. End-to-End RAG 最佳实践

### 6.1 flan-t5-base baseline 的作用与局限

`flan-t5-base` 的最大价值，在于帮助项目顺利跑通了从检索到生成的完整闭环。阶段性结果表明，在 `mark_200_50 + <#> + DPR + flan-t5-base` 这条主线上，系统已具备可用的 retrieval coverage，且 hallucination rate 很低，说明该模型总体保持“老实”与 grounded 的特性。但它的主要短板也非常明确：答案过于极简、只摘半句、缺少关键点，导致 `answer_complete` 明显偏低。换言之，`flan-t5-base` 更适合作为 baseline generator 和开发验证工具，而不是项目最终的质量目标。fileciteturn7file14

### 6.2 prompt 调整的收益与边界

阶段二结果显示，prompt 调整的确有正面作用：新的 prompt 让 `flan-t5-base` 略微更倾向于输出完整句子，`answer_complete` 从 39% 提升到 44.5%，`answer_correct` 从 47% 提升到 50%，幻觉率下降到 0%。但这一改善幅度有限，且生成耗时在某些 query 上明显增加。换言之，prompt 优化属于“值得做但不是决定性突破”的增强项，它能挤出 5–10% 的改进空间，却不能从根本上解决小模型的上下文整合能力不足。fileciteturn7file0

### 6.3 更换到 Phi-3.5-mini-instruct 的结果

阶段三的模型替换，是当前端到端层面最关键的证据。检索层指标几乎不变：`retrieval_top1_hit` 仍为 66.7%，`retrieval_top3_hit` 仍为 88.9%；但在生成层，`Phi-3.5-mini-instruct` 相比 flan 出现了明显提升：`answer_correct` 从 `0.94 / 2 (47%)` 提升到 `1.61 / 2 (80.5%)`，`answer_grounded` 从 `1.67 / 2 (83.3%)` 提升到 `1.94 / 2 (97%)`，`answer_complete` 从 `0.78 / 2 (39%)` 提升到 `1.67 / 2 (83.5%)`，hallucination rate 从 5.6% 降到 0%；代价是平均生成时间从约 1 秒级上升到 23–27 秒。fileciteturn7file9

### 6.4 生成器对比结论

这组结果支持两个重要结论。第一，当前系统瓶颈已经从“检索层是否完全失效”转向“生成模型能否充分利用 context”。因为检索层指标未变，而端到端回答质量显著上升，说明提升主要来自生成器本身。第二，新的主生成器路线应该是 `Phi-3.5-mini-instruct`，而不是继续把 flan 当作质量主线。flan 更适合作为轻量 baseline 和工程验证工具；Phi 则更适合承担“当前最优答案质量”的角色。唯一需要同时写清的是：其 CPU 上的生成时延很高，因此并不适合作为边缘板端的重生成模型。fileciteturn7file9

### 6.5 故障分类分析

按照检索-生成分离分析，旧的 flan 路线中仍存在较高比例的 pure generation fault，即 top-3 已经 hit 但答案依然答不好；而切换到 Phi 后，pure generation fault 显著下降，完全成功率提升到约 61%。这意味着当前 retrieval 主线已经足够支撑生成模型能力比较，后续优化的主战场将更多转向生成器与 prompt 的协同，而不是重新推翻 retrieval 整体路线。fileciteturn7file9

---

## 7. Gold Context 上限测试与异常分析

### 7.1 实验目的

gold context 实验的目的，是绕过 retrieval，将人工构造的标准上下文直接输入生成器，从而观察生成器在“完美上下文条件”下的理论上限。按常理，若生成器有足够能力，则在 gold context 条件下应至少不差于 top-3 / top-5 retrieval 结果。

### 7.2 实际异常现象

实际结果却出现明显异常：即使给出完整的 gold context，`Phi-3.5-mini-instruct` 仍频繁出现拒答，直接输出 “The context provided does not contain enough information” 或 “the answer is no”；在 Query 7（RK3568 minimal solution）上甚至出现了明显幻觉，编造出并不存在于上下文中的 “16GB of RAM”；另外，许多答案依旧只覆盖部分信息，或回答得过于泛化。总结文件甚至指出：Top-5 时的 80.5% correct 主要得益于更多上下文对模型弱点的“补偿”，而 gold context 反而暴露了模型在指令跟随与上下文理解上的局限。fileciteturn7file7

### 7.3 可能影响因素

这一异常不能简单解释为“完美上下文无用”，更合理的写法是保留为阶段性异常，并给出可能影响因素。第一，当前用于 Phi 的 prompt 中包含较强的“只基于 context，信息不足就说 no”的约束，容易诱发保守拒答。第二，Phi 采用了 messages/chat 风格输入，而 flan 采用普通 seq2seq prompt，输入范式的变化本身就可能影响模型对 context 的利用方式。第三，gold context 的组织方式与 top-k 拼接后的检索上下文并不完全一致，可能改变了模型的读取偏好。第四，当前 gold context 对比样本量有限，尚不足以将这组异常解释为最终定论。fileciteturn4file4 fileciteturn7file17

### 7.4 阶段性结论

因此，本报告对 gold context 的结论保持谨慎：它确实提示当前瓶颈已明显转向生成模型本身，即使在高质量上下文下，生成器也未达到理想上限；但同时也应承认，gold context 实验设置中的 prompt 形式、chat template 使用方式和输入组织方式，很可能共同影响了这组结果。更稳妥的做法，是将其写成“当前阶段出现的高价值异常现象”，并作为后续实验优先复测项，而不是直接下结论说“完美上下文反而更差”。fileciteturn7file7

---

## 8. 部署与工程化最佳实践

### 8.1 开发机与边缘端职责分工

知识库文本与 gold context 题集都明确给出了一条现实的工程路径：RK3568 属于典型的资源受限边缘设备，适合轻量服务、数据库与受控实验，但不适合同时承担大型 embedding 模型与重型生成模型。因此，更合理的部署策略是：开发机或工作站完成大规模文档切分、批量 embedding 生成与批量入库；边缘设备仅负责在线 query 处理、向量检索与轻量响应组装。这一判断在项目中不仅是理论性结论，也与 `Phi-3.5-mini-instruct` 在 CPU 上 20 秒级生成时延的实测结果高度一致。fileciteturn7file10 fileciteturn7file13 fileciteturn7file9

### 8.2 OpenGauss 的系统角色

OpenGauss 在本项目中的定位，不是单纯存文本，而是同时承担“原始 chunk + embedding vector”的存储角色，并为 query 向量提供相似度检索基础。其价值在于将 RetrievalQA 的数据库层与向量检索层整合到同一系统中，使得文档 traceability、配置追踪与检索实验可以在数据库内部被统一管理。`TextChunker` 的知识库文本中甚至直接建议在表结构中包含原文、向量、文档 ID、chunk ID、文件名、模型名、chunk size、overlap 与创建时间等字段，以支持后续实验追踪与优化。fileciteturn7file3

### 8.3 BentoML 的角色

从知识库文本与 `service.py`、`bentofile.yaml` 的代码看，BentoML 在本项目中被明确定位为应用服务封装层，而不是 embedding 模型本身。它的作用是把 chunker、embedder、database client、retriever 与 generator 的调用逻辑包裹为统一 API 服务。需要如实说明的是：当前关于 BentoML 的证据更适合支撑“架构定位”和“工程实现尝试”，而不足以支撑“已经形成最终部署最佳实践参数配置”。因此，本报告会将 BentoML 写为已明确定位的重要组件，而不是本阶段最佳实践主结论的中心证据。fileciteturn7file10 fileciteturn6file1 fileciteturn6file4

### 8.4 Docker / compose 的写法边界

你特别指出，当前上传的 Docker / compose / BentoML 文件并非最终测得最佳实践参数对应的配置。因此，本报告只将这些文件用于说明工程实现路径、阶段性部署尝试与多架构部署思路，而不会把其中的具体镜像名、端口、命令行与挂载路径写成“当前最终推荐配置”。这一区分非常重要，因为正式报告的可信度，正建立在“证据强弱与表述强弱一致”的前提上。fileciteturn6file2 fileciteturn6file3

### 8.5 当前最小可行部署建议

综合当前主线，最合理的阶段性部署建议为：在开发机完成完整实验、embedding 生成与主生成器比较，在边缘端仅保留 `OpenGauss + 本地轻量服务端点 + 外部机器完成大规模 embedding 生成` 的最小闭环。这既符合知识库文本中的工程判断，也与项目实际实验收敛路径一致。fileciteturn7file12

---

## 9. 原计划、实际收敛路线与差异说明

### 9.1 原计划中的扩展目标

申请书中的项目计划明显比当前已验证主线更大：包括 HuggingFace / Cohere / BentoML 三种 embedding / 服务路线、AArch64 容器化、ONNX 轻量化、混合检索与自动调优、缓存机制以及社区贡献。正式报告有必要保留这些目标，因为它们体现了项目原本的设计视野。fileciteturn5file7

### 9.2 当前已形成稳定证据的主线

当前真正形成稳定证据的，是 `mark_200_50` 为默认 chunk、`<#>` 为主算子、DPR 为 embedding 主路线、`Phi-3.5-mini-instruct` 为新主生成器，以及开发机/边缘端职责分工。这条主线已经足以支撑一份“阶段性最佳实践报告”，也足以支撑简历/面试中的工程总结，但它并不意味着所有申请书目标都已完整闭环。fileciteturn7file9

### 9.3 暂未完全落地或证据不足的部分

当前尚未形成同等强度证据的部分主要包括：Cohere 的完整实证路线、BentoML 的完整部署交付、ONNX / Optuna / Redis 等申请书扩展项、以及社区 PR 的正式提交与合入。对这些内容，最稳妥的写法是保留为“原计划重要组成部分与后续工作方向”，而非写成已完成主结论。这种写法虽然更克制，但更符合正式结项报告的可信度要求。

---

## 10. 关键报错与修复经验

### 10.1 筛选原则

`典型报错与修复经验（raw）.txt` 并不是可直接照搬的正式报告章节，而更像是候选素材池。正式报告在筛选时遵循两个原则：一是只保留那些具有普遍工程意义、且与当前主结论密切相关的问题；二是避免把“一次性现象”或尚未稳定复现的问题写成核心经验。fileciteturn6file0

### 10.2 当前值得写入正式报告的经验

第一，HuggingFace 模型下载失败、SSL / 网络不稳定与离线缓存准备问题，提示 AI/RAG 项目不能把“在线拉模型”当作唯一运行前提；稳定复现实验时，本地缓存和离线模型准备是必要工程能力。第二，从 flan 切换到 Phi 时，错误并不只是版本问题，还涉及模型架构类型变化、`AutoModelForCausalLM` 的导入与 chat / causal LM 的输入范式适配，这一问题直接影响了生成器路线切换。第三，openGauss 向量类型与 SQL 层的对接，需要显式区分 Python 侧的 numpy / list 与数据库侧的 vector literal，否则容易出现类型转换与检索结果异常。第四，相似度算子不应早早固定死，而必须结合 embedding 路线与问题类型实测。第五，端到端效果差时，应该优先做 retrieval / generation 分离诊断，而不是本能地把所有责任归因于数据库或 prompt。fileciteturn6file0

### 10.3 经验总结式写法

从项目阶段经验的角度，更有价值的不是“记住某条报错字符串”，而是形成一套排查顺序：先区分环境问题与逻辑问题，再区分检索问题与生成问题，最后才进入模型与配置优化。正是由于建立了这种排查顺序，本项目才逐渐从“怀疑哪里都有问题”的状态，走到“知道当前主瓶颈在哪一层、该继续优化什么”的收敛阶段。fileciteturn6file0

---

## 11. 当前推荐配置

### 11.1 默认推荐配置

基于当前证据，本项目的阶段性默认推荐配置为：

- Chunk 配置：`mark_200_50`
- Retrieval operator：`<#>`
- Embedding 路线：DPR（context encoder / question encoder）
- Generator：`Phi-3.5-mini-instruct`
- Baseline generator：`flan-t5-base`
- 部署策略：开发机完成大规模 chunking、embedding 与生成器比较；边缘端保留 `OpenGauss + 轻量服务端点` 的最小闭环

### 11.2 条件化推荐

若知识库边界敏感问题占比更高，可考虑 `mark_200_100` 作为增强候选；若需要保留更细粒度的对照组，可继续使用 `mark_150_10`；若后续需要面向吞吐量而不是质量做折中，`flan-t5-base` 仍可作为轻量 baseline，而不是彻底被放弃。也就是说，当前推荐配置不是唯一解，而是目前证据最强的默认路径。

---

## 12. 后续工作

### 12.1 检索侧

当前仍建议完成 top-k 的更系统收尾实验，进一步验证 top-1 / top-3 / top-5 在不同问题类型上的收益；同时可在当前 retrieval 主线不推翻的前提下，补充最小版本 rerank 或 hybrid 验证。

### 12.2 生成侧

gold context 的异常值得优先复测，尤其需要在保持 query 与 context 不变的情况下，单独控制 prompt 形式、chat template 与 answer style 要求；此外，也可以继续比较更强 instruct generator，进一步确认“当前瓶颈在生成器”这一结论的上限位置。

### 12.3 工程侧

后续应补齐 Cohere 实证、BentoML 完整交付、AArch64 / RK3568 的最小闭环复测，以及社区 PR / 技术 write-up 的正式输出。只有这些环节补齐后，申请书中的“原计划全量交付”才能算真正收尾。

---

## 13. 结论

本项目的价值，不在于单独证明某个数据库、某个 embedding 模型或某个生成器能否工作，而在于逐步形成一套有证据支撑的工程判断。当前阶段已经可以得出较稳的结论：其一，chunking 层已收敛到 `mark_200_50` 为默认主配置，`mark_200_100` 为边界增强候选；其二，retrieval 层在 DPR 路线下已明确 `<#>` 为主算子；其三，端到端质量的主瓶颈已明显转向生成层，`Phi-3.5-mini-instruct` 相比 `flan-t5-base` 带来显著质量提升；其四，边缘部署的合理方向不是“把所有重组件都塞进 RK3568”，而是“开发机完成重处理，边缘端保留最小闭环”。这些结论使项目已经从“能跑通”阶段，进入“有条件化推荐与工程经验沉淀”的阶段。fileciteturn7file9 fileciteturn7file12

---

## 附录说明

本报告正文只保留结论性描述、核心表格、核心指标与少量代表性现象；原始日志、评分表、归档命名映射、代码文件与 raw output 压缩包均应与本报告配套存档，以支持后续复核与社区化整理。详见单独的附录文件。
