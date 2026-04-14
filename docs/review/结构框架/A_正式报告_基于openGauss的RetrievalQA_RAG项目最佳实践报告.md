# 基于 openGauss 的 RetrievalQA / RAG 项目最佳实践报告

**项目负责人：朱玲**

---

## 使用说明
本文件为“面向社区 / 项目结项”的正式报告章节框架与写作草稿框架。
写作原则如下：

1. 如实呈现“原计划更大，实际先收敛到主线路线”的项目推进过程。
2. 正文以结论、核心表格、关键指标、代表性现象为主。
3. 原始实验输出、评分表、终端日志、拆分文件与阶段性材料统一放入附录与证据目录。
4. BentoML、Docker、compose 等材料可用于说明工程实现路径与部署尝试，但不直接作为“最终最佳实践参数配置”的证据。
5. “典型报错与修复经验”按项目阶段经验总结式组织，而不是简单流水账。

---

# 摘要（写作草稿）
本项目围绕 openGauss + HuggingFace / DPR + 外部检索 + 普通生成模型 的 RetrievalQA / RAG 路线展开，目标是沉淀一套兼顾开发机验证与 AArch64 / RK3568 边缘部署约束的阶段性最佳实践。项目最终形成的主结论不是“所有计划项全部完成”，而是围绕文本分块、向量检索、生成模型、部署分工四条主线完成收敛：在 chunking 层，当前默认推荐配置为 `mark_200_50`，`mark_200_100` 作为边界增强候选，`mark_150_10` 保留为小 chunk 对照；在 retrieval 层，HuggingFace / DPR 路线下 `<#>` 为当前综合最优主算子，而 `<->` 整体偏弱；在端到端层，系统已完成从检索到生成的完整闭环验证，瓶颈逐步由检索层转向生成层；在生成模型选择上，Phi-3.5-mini-instruct 相比 flan-t5-base 显著改善答案正确性、groundedness 与完整性，因此可视为当前新的主生成器路线；在部署侧，最终更现实的建议是开发机承担大规模 chunking、embedding 与批量写库，边缘设备承担本地检索与轻量服务，形成最小稳定闭环。

同时，本报告保留了对“原计划与实际收敛差异”的如实说明：包括 Cohere、BentoML、ONNX、自动调优、缓存、多平台部署等目标在内的原始项目范围更大，但当前阶段形成稳定实证的部分主要集中在 chunk / retrieval / generator 主线。对未完全落地但值得保留的方向，如 top-k 收尾实验、gold context 复测、rerank / hybrid 验证、BentoML 完整服务封装与边缘部署闭环增强，统一列入后续工作。

---

# 关键词
openGauss；RetrievalQA；RAG；HuggingFace；DPR；Phi-3.5-mini-instruct；AArch64；RK3568

---

# 目录（建议）
1. 项目背景与目标  
2. 系统架构与工程实现  
3. 评测设计与评价标准  
4. Chunking 最佳实践  
5. Retrieval 最佳实践  
6. End-to-End RAG 最佳实践  
7. Gold Context 上限测试与异常分析  
8. 部署与工程化最佳实践  
9. 原计划、实际收敛路线与差异说明  
10. 关键报错与修复经验  
11. 当前推荐配置  
12. 后续工作  
13. 结论  
附录

---

# 1. 项目背景与目标

## 1.1 项目背景（写作要点）
- 说明 openGauss 在 RetrievalQA / RAG 场景中的角色：不仅承担传统关系数据库能力，也承担向量存储与相似度检索骨架。
- 说明为什么该项目需要“最佳实践”，而不是只做单次演示。
- 说明项目与 AArch64 / RK3568 边缘部署场景的现实约束。

## 1.2 原始项目目标（写作要点）
- 部署文档：容器化部署与环境说明。
- 模型接入：Embedding 生成、向量写库、相似度检索。
- RetrievalQA 验证：从检索到生成的完整链路。
- 社区输出：最佳实践报告、代码示例、后续社区化整理。

## 1.3 本报告的评测范围（阶段性）
- 本阶段重点覆盖：
  - chunking 配置收敛
  - retrieval operator 对比
  - flan 与 Phi 的端到端生成比较
  - top-k 比较
  - gold context 生成器上限观察
  - 开发机 / 边缘设备职责分工判断
- 本阶段未形成完整实证闭环的方向：
  - Cohere 路线
  - BentoML 完整交付
  - ONNX / Optuna / Redis 等扩展项
  - 社区 PR 提交闭环

---

# 2. 系统架构与工程实现

## 2.1 总体架构（建议配图）
建议配“原始文档 -> chunking -> embedding -> openGauss -> query embedding -> similarity retrieval -> context -> generator -> answer”的流程图。

## 2.2 关键模块说明
### 2.2.1 TextChunker
- 负责知识库文本的切分。
- 当前比较了 length / mark 两类切分思路。
- 实验重点收敛在 mark 路线。

### 2.2.2 HFEmbedder
- 使用 DPRContextEncoder 生成文本 chunk embedding。
- 当前主 embedding 路线为 DPR。

### 2.2.3 OPController
- 负责连接 openGauss。
- 负责 embedding 数据写入。
- 负责基于 `<#>` / `<=>` / `<->` 等算子的向量检索。

### 2.2.4 RagPipeline
- 串起 chunk -> embedding -> 写库 -> 检索 -> 上下文构造 -> 生成回答。
- 体现 RetrievalQA 的主执行链。

### 2.2.5 test_rag.py
- 用于单配置、多 query 的阶段性评测与对比。
- 支撑 top-k 比较、gold context 比较与生成器对比。

## 2.3 当前实际主线路线
- chunk：mark-based
- default chunk config：`mark_200_50`
- retrieval operator：`<#>`
- embedding：DPR
- generator baseline：flan-t5-base
- current main generator：Phi-3.5-mini-instruct

---

# 3. 评测设计与评价标准

## 3.1 评测分层原则
- retrieval evaluation 与 generation evaluation 分离。
- 原因：
  - 检索命中不等于最终答案好。
  - 生成模型可能掩盖检索缺陷，也可能浪费已命中的上下文。
- 该原则是本项目最重要的评测组织原则之一。

## 3.2 题集与问题类型
建议将问题分为：
- 事实定位型
- 原因解释型
- 对比型
- 列表 / 枚举型
- 部署 / 推荐方案型

## 3.3 指标定义
### 检索层
- `retrieval_top1_hit`
- `retrieval_top3_hit`

### 生成层
- `answer_correct`
- `answer_grounded / faithfulness`
- `answer_complete`
- `hallucination`

### 评分口径（可直接入正文）
- Hit = 1：top-1 直接包含或非常明确地回答了问题
- Hit = 0.5：top-1 部分相关、提到关键词但不够直接/完整
- Hit = 0：top-1 与问题明显不相关或只沾边

## 3.4 评测配置说明
- chunk 配置比较
- similarity operator 比较
- top-k 比较
- flan vs Phi 生成器比较
- gold context 对比实验

---

# 4. Chunking 最佳实践

## 4.1 总体结论（可直接作为正文初稿）
当前证据支持以下稳定结论：length 路线暂不适合作为主路线；`mark_100_10` 可基本排除；主候选已收敛到 `mark_150_10`、`mark_200_10`、`mark_200_50`；其中 `mark_200` 系列整体比 `mark_150` 更稳定，`mark_200_50` 是当前默认主配置，而 `mark_200_100` 更适合作为边界增强候选而不是直接替代默认配置。

## 4.2 建议表格：Chunk 配置收敛结论表
| 配置 | 统计特征 | 当前定位 | 是否推荐 | 说明 |
|---|---|---|---|---|
| length 系列 | 稳定性一般 | 非主路线 | 否 | 当前英文技术知识库下不如 mark 稳定 |
| mark_100_10 | 过短块多 | 排除 | 否 | 过碎，边界信息破碎 |
| mark_150_10 | 小 chunk 对照 | 对照保留 | 有条件 | 某些比较类问题 top-1 更直接 |
| mark_200_10 | 200 系列基线 | 保留 | 是 | 稳定，适合作为对照基线 |
| mark_200_50 | 默认主配置 | 主配置 | 是 | 综合表现最均衡 |
| mark_200_100 | 边界增强候选 | 条件保留 | 有条件 | 更适合边界敏感问题 |

## 4.3 代表性现象
- overlap 对普通定义类问题影响不大。
- overlap 对跨列表、跨句边界问题更有价值。
- 小 chunk 可能在少数比较类 / 部署类问题上更直接，但整体稳定性不如 200 系列。

## 4.4 阶段性推荐
当前默认 chunk 配置推荐为 `mark_200_50`。

---

# 5. Retrieval 最佳实践

## 5.1 总体结论（正文草稿）
在当前 HuggingFace / DPR 路线下，`<#>` 是最值得继续推进的相似度算子；`<->` 明显弱于 `<#>`，不建议作为主算子继续推进；`<=>` 介于两者之间，但整体不如 `<#>`。定义类、作用类、直接原因类问题的 retrieval 已较稳定，而列表 / 枚举类、元数据字段类、推荐方案类问题的主要瓶颈并不只是算子，而在于答案信息天然分散、跨 chunk 边界。

## 5.2 建议表格：算子比较结论表
| 维度 | `<#>` | `<=>` | `<->` | 结论 |
|---|---|---|---|---|
| top-1 命中 | 最优 | 中等 | 最弱 | `<#>` 当前最佳 |
| top-3 覆盖 | 最优 | 次之 | 最弱 | `<#>` 最适合作为主算子 |
| 比较类问题 | 较强 | 中等 | 偏弱 | `<#>` 优势更明显 |
| 列表 / 枚举类问题 | 全部偏弱 | 全部偏弱 | 全部偏弱 | 主要瓶颈不只是算子 |

## 5.3 检索层局限
- 当前列表 / 元数据类问题仍易 miss。
- 不应把所有 retrieval 弱点归因于相似度公式。
- 更大的 chunk、合适 overlap、后续 rerank / hybrid 可能才是更有效补强方向。

---

# 6. End-to-End RAG 最佳实践

## 6.1 flan-t5-base baseline 观察
- 已成功跑通完整链路。
- groundedness 尚可，幻觉率低。
- 主要短板是完整性不足、容易极简回答。

## 6.2 Phi-3.5-mini-instruct 作为新主生成器路线
- 相比 flan-t5-base，在 correctness、faithfulness、completeness 上明显提升。
- 代价是生成时间增加。
- 当前可作为新的主生成器路线。

## 6.3 建议表格：flan vs Phi 对比表
| 模型 | correctness | groundedness | completeness | latency | 结论 |
|---|---|---|---|---|---|
| flan-t5-base | baseline | 较稳 | 偏弱 | 较快 | 适合开发验证 |
| Phi-3.5-mini-instruct | 更高 | 更高 | 更高 | 更慢 | 当前更优主路线 |

## 6.4 故障分类分析
建议按以下三类整理：
- pure retrieval fault
- pure generation fault
- mixed fault

写作重点：
- 当前“纯 generation fault”占比偏高，是判断主瓶颈已逐步转向生成层的重要依据。
- 幻觉率不高，主要问题不是乱编，而是答不全、拒答和保守输出。

---

# 7. Gold Context 上限测试与异常分析

## 7.1 实验目的
绕过 retrieval，直接给人工构造 gold context，观察生成器能力上限。

## 7.2 实际观察（正文草稿）
gold context 并未带来预期中的显著上限提升，反而暴露出较高拒答率、局部幻觉以及完整性仍不足的问题。这说明当前系统瓶颈已明显转向生成模型本身。

## 7.3 异常现象的可能影响因素
注意写成“可能”而不是“确定”：
- prompt 约束过强，诱发保守拒答
- chat template 与直接文本 prompt 的差异
- Phi 对“只基于 context”类指令的跟随方式偏保守
- gold context 组织方式、长度与答案结构要求影响了模型利用效果

## 7.4 阶段性结论
gold context 结果不能简单解释为“完美上下文无效”；更合理的解读是：生成模型本身已成为主要瓶颈，同时 gold context 评测设置仍可能影响模型真实上限的显现。

---

# 8. 部署与工程化最佳实践

## 8.1 开发机与边缘端职责分工
建议写为阶段性最佳实践结论：
- 开发机负责：大规模 chunking、embedding、批量写库、模型实验
- 边缘设备负责：在线 query、向量检索、轻量响应组装

## 8.2 OpenGauss 的系统定位
- 向量存储与检索骨架
- 与 RetrievalQA 主流程深度耦合，而非外围组件

## 8.3 BentoML、Docker、compose 的写法边界
- 可作为工程实现路径、服务化方向、部署尝试材料写入
- 不作为当前“最终最佳实践参数配置”的直接证据
- 应与“当前主线实证结论”区分开

## 8.4 当前最小可行部署建议
`OpenGauss + 本地轻量服务端点 + 外部强机器完成大规模 embedding 生成`

---

# 9. 原计划、实际收敛路线与差异说明

## 9.1 原计划中的主要扩展目标
- HuggingFace / Cohere / BentoML 多路线
- ONNX / 轻量化
- 自动调优
- 缓存
- 多平台部署
- 社区 PR

## 9.2 当前已形成稳定证据的主线
- chunk 路线收敛
- operator 路线收敛
- 生成器路线收敛
- 开发机 / 边缘端职责分工收敛

## 9.3 暂未完全落地的方向
- Cohere 实证不足
- BentoML 完整交付证据不足
- ONNX / Optuna / Redis 未形成闭环
- 社区 PR 尚未完成

---

# 10. 关键报错与修复经验

## 写作原则
本章不是报错流水账，而是“项目阶段经验总结”。

## 10.1 推荐保留的问题类型
- HuggingFace 模型下载 / SSL / 网络链路问题
- 模型切换时的加载类 / 输入范式问题
- openGauss 向量类型转换与算子验证问题
- 相似度算子不能预设为固定常量
- retrieval / generation 不分离会导致误判
- Docker 镜像体积与 COPY 策略问题
- 板端目标不应等同于开发机全栈复制

## 10.2 建议写法
每条经验统一成：
- 现象
- 根因
- 修复方式
- 工程启示

---

# 11. 当前推荐配置

## 11.1 默认推荐配置
- chunk：`mark_200_50`
- retrieval operator：`<#>`
- embedding：DPR
- generator：Phi-3.5-mini-instruct
- baseline：flan-t5-base
- deployment：开发机完成重处理，边缘端保留最小闭环

## 11.2 条件化推荐
- 边界敏感问题较多时：`mark_200_100`
- 小 chunk 只建议保留作对照与局部实验
- top-k 作为后续继续精调的维度

---

# 12. 后续工作

## 12.1 检索侧
- top-k 收尾实验
- overlap 边界补测
- rerank / hybrid 最小验证

## 12.2 生成侧
- gold context 复测
- 更强 instruct generator 对比
- prompt 结构化改进

## 12.3 工程侧
- BentoML 完整服务封装
- Cohere 路线补证
- AArch64 / RK3568 最小部署闭环强化
- 社区 PR 输出

---

# 13. 结论（写作草稿）
本项目当前阶段已经从“能否跑通”转入“哪条路线更值得推荐”的工程收敛阶段。围绕 chunking、retrieval、generator 与部署分工四条主线，项目已形成较明确的阶段性最佳实践：`mark_200_50` 是当前默认 chunk 配置，`<#>` 是 HuggingFace / DPR 路线下的主检索算子，Phi-3.5-mini-instruct 是当前更值得继续推进的主生成器路线，而边缘端部署更适合以本地检索与轻量服务构成最小闭环。与此同时，本报告也如实保留了原计划与实际推进之间的差异，避免将阶段性路线收敛误写为全量目标已完成。相较于只给出零散实验记录，这些阶段性结论更接近可以指导后续工程决策的最佳实践。

---

# 附录（建议）
- 附录A：文件归档与命名规则
- 附录B：原始证据目录
- 附录C：题集与 gold context
- 附录D：核心代码文件说明
