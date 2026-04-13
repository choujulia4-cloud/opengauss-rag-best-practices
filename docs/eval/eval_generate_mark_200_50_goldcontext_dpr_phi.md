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
  "original_file": "/raw/goldContest_results1.csv"
}
```

# eval_generate_mark_200_50_goldcontext_dpr_phi.md

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
| original_file | /raw/goldContest_results1.csv |

### 原始评价

| Query 序号 | Query（简写） | answer_correct | answer_grounded | answer_complete | hallucination | 备注 |
|---|---|---|---|---|---|---|
| 1 | OpenGauss role | 1 | 2 | 1 | 0 | 答案只提 storage，未覆盖完整定义 |
| 2 | Why divide long documents | 1 | 2 | 1 | 0 | 答案泛化（readability），偏离原文核心原因 |
| 3 | Two embedding sources | 2 | 2 | 2 | 0 | 完美 |
| 4 | BentoML role | 2 | 2 | 2 | 0 | 较好，但略显啰嗦 |
| 5 | Why RK3568 resource-constrained | 0 | 0 | 0 | 0 | 完全拒答（“does not contain enough information”） |
| 6 | What dimensions for best-practice | 0 | 0 | 0 | 0 | 完全拒答 |
| 7 | Recommended minimal for RK3568 | 0 | 0 | 0 | 0 | 严重幻觉（回答“16GB of RAM”） |
| 8 | Metadata fields | 0 | 0 | 0 | 0 | 完全拒答 |
| 9 | Four main deliverables | 1 | 2 | 1 | 0 | 只列了一部分，且格式混乱 |
| ...（其余省略，趋势一致） | - | - | - | - | - | - |
