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
  "original_file": "/raw/goldContest_results2.csv"
}
```

# eval_generate_mark_200_50_goldcontext_compare_dpr_phi.md

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
| original_file | /raw/goldContest_results2.csv |

### 原始评价

| 指标 | Gold Context (本次) | Top-5 (之前) | Top-3 (之前) | 对比结论 |
|---|---|---|---|---|
| answer_correct (平均分) | 0.89 / 2 (44.5%) | 1.61 / 2 (80.5%) | 1.50 / 2 (75%) | 大幅下降 |
| answer_grounded | 1.11 / 2 (55.5%) | 1.94 / 2 (97%) | 1.78 / 2 (89%) | 大幅下降 |
| answer_complete | 0.94 / 2 (47%) | 1.67 / 2 (83.5%) | 1.56 / 2 (78%) | 大幅下降 |
| hallucination rate | 11.1% | 0% | 0% | 明显上升 |
