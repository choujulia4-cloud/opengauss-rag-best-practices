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
  "original_file": "/raw/goldContext_results3.txt"
}
```

# eval_generate_mark_200_50_goldcontext_summary_dpr_phi.md

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
| original_file | /raw/goldContext_results3.txt |

### 原始评价

```text
即使给出完美的 Gold Context，Phi-3.5-mini-instruct 的表现也远没有达到上限，这说明模型本身能力是当前最大瓶颈：

拒答率极高：多个 query 直接输出 “The context provided does not contain enough information” 或 “the answer is no”，即使 gold context 里明明有答案。
幻觉出现：Query 7（RK3568 minimal solution）出现了明显幻觉（编造“16GB of RAM”）。
完整性依然不足：很多答案只覆盖部分内容，或回答得过于泛化（例如 Query 2 把原因说成“improve readability”）。
对比之前：Top-5 时的 80.5% correct 主要得益于 Top-5 提供了更多上下文“补偿”了模型的弱点；而当只给 Gold Context 时，模型反而暴露了指令跟随能力和上下文理解的局限性。

核心结论：

Phi-3.5-mini-instruct 在 RAG 场景下有明显进步（比 flan-t5-base 好很多），但尚未达到“强 instruct 模型”的水平。
当前系统瓶颈已经从“检索”转移到了生成模型本身（即使完美检索，也只能发挥约 45% 的潜力）。
这也解释了为什么 Top-3 / Top-5 效果差异不大——模型利用上下文的能力有限。
```
