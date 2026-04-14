# 基于 openGauss 的 RetrievalQA / RAG 项目工程总结

**项目负责人：朱玲**

---

## 1. 项目目标

本项目围绕 openGauss 向量数据库、DPR embedding、外部检索式 RetrievalQA 与生成模型对比展开，目标是完成从文档切分、embedding 生成、向量检索到端到端问答的可运行闭环，并在实验基础上沉淀一套可复述、可迁移的阶段性最佳实践。当前总结只保留“已经做完并有证据”的部分，不把尚未完全落地的设想写成既成事实。fileciteturn7file3

## 2. 系统实现

当前主链路由五个核心模块组成：`TextChunker` 负责分块并生成 chunk dataset；`HFEmbedder` 用 DPR context encoder 批量生成 embedding；`OPController` 负责连接 openGauss、写入 embedding 与执行相似度检索；`RagPipeline` 串联 chunk → embedding → 写库 → 检索 → 生成；`test_rag.py` 用于切换 chunk 配置、算子、top-k 与生成器配置进行实验。当前实际形成主结论的路线是：`mark` 系列切块 + DPR + openGauss + `<#>` 检索 + 生成器对比。fileciteturn7file4 fileciteturn7file11

## 3. 已完成的关键实验

### 3.1 Chunk 收敛

分块统计与检索对比表明，`length` 系列不适合作为当前主路线，`mark_100_10` 过碎；`mark_150_10` 适合作为小 chunk 对照组，`mark_200_10` 较稳，而 `mark_200_50` 是当前综合表现最均衡的默认主配置。对边界敏感问题的补测还显示，`mark_200_100` 在少数跨边界问题上可能更有优势，但不足以替代 `mark_200_50` 成为默认配置。fileciteturn4file24 fileciteturn7file4

### 3.2 Retrieval 收敛

在当前 DPR embedding 路线下，`<#>` 是综合最优的相似度算子，`<=>` 居中，`<->` 明显偏弱。定义类、作用类、直接原因类问题的 top-1 / top-3 检索已较稳，而列表/枚举类、元数据类问题仍然薄弱，主要原因不是算子本身，而是答案信息天然分散、跨 chunk 边界。这个结论来自 retrieval-only 对比，而不是只看端到端最终答案。fileciteturn4file25

### 3.3 生成器收敛

`flan-t5-base` 已经成功跑通端到端闭环，但主要问题是答案过短、完整性不足。更换到 `Phi-3.5-mini-instruct` 后，检索层指标不变，但 `answer_correct` 从 47% 提升到 80.5%，`answer_complete` 从 39% 提升到 83.5%，groundedness 也明显提升，hallucination 降为 0%；代价是生成时延从约 1 秒级上升到 20 秒级以上。这说明当前系统的主要瓶颈已经从检索层逐步转向生成层，同时也说明 Phi 可以被视为新的主生成器路线。fileciteturn7file9

### 3.4 Gold Context 异常

为了测试生成器上限，项目还做了 gold context 实验，直接向生成器提供人工构造的标准上下文。但结果并没有像预期那样“显著更好”，反而出现高拒答、局部幻觉与完整性不足。这说明“完美检索 ≠ 完美答案”，当前生成器对 context 的利用能力仍有限；同时，这组异常也可能受到 prompt 约束、chat template 与输入组织方式影响，因此更适合写成“高价值异常现象”，而不是直接下最终定论。fileciteturn7file7

## 4. 关键工程判断

第一，retrieval evaluation 与 generation evaluation 必须分离。否则很容易把生成模型能力误判成检索系统能力，或者反过来掩盖检索层缺陷。第二，chunk / operator / top-k / generator 必须解耦评测，否则无法知道主瓶颈到底在哪一层。第三，gold context 异常说明“给足上下文”并不自动等价于“生成器能用好上下文”，这一点直接影响后续优化方向。第四，RK3568 这类资源受限板端更适合承担“本地检索 + 轻量服务”角色，而不适合同时承担重 embedding 与重生成模型。fileciteturn7file10 fileciteturn7file13

## 5. 当前推荐配置

当前阶段的默认推荐配置为：

- chunk：`mark_200_50`
- retrieval operator：`<#>`
- embedding：DPR
- generator：`Phi-3.5-mini-instruct`

若问题更偏边界敏感或跨列表枚举，可考虑把 `mark_200_100` 作为增强候选；若只需要轻量 baseline 验证，则可以继续使用 `flan-t5-base`。这一定义是“当前最佳折中”，而不是永久不变的最终答案。fileciteturn7file9

## 6. 后续工作

后续工作主要分三类：一是检索侧补齐 top-k 收尾实验，并考虑最小版本 rerank / hybrid；二是生成侧继续复测 gold context，并尝试更稳的 prompt / chat template 组织方式；三是工程侧补齐 BentoML 完整交付、Cohere 路线证据与边缘端最小闭环验证。对面试或简历表达来说，当前已经可以清晰表述为：项目完成了检索主线收敛，并把系统瓶颈准确定位到了生成层。fileciteturn7file7
