# 最终保留版总表（仅保留 eval / output 体系）

> 说明：根据最新规则，`rag_results.txt` 拆分为：
> - `eval_generate_mark_200_50_dpr_flan_vs_phi.md`
> - `output_generate_mark_200_50_dpr_phi.md`

| 原文件名 | 处理方式 | 拆分后文件数量 | 最终保留的新文件名 |
|---|---|---:|---|
| rag_results.txt | 已拆分 | 2 | eval_generate_mark_200_50_dpr_flan_vs_phi.md；output_generate_mark_200_50_dpr_phi.md |
| rag_results_top.txt | 已拆分 | 2 | eval_generate_mark_200_50_top1_dpr_phi.md；eval_generate_mark_200_50_top1_dpr_phi_3.md |
| rag_results_#-phi-top1.csv | 未拆分 | 1 | eval_generate_mark_200_50_top1_dpr_phi_2.md |
| rag_results_=-阶段一.csv | 已拆分 | 2 | eval_generate_mark_200_50_top1_dpr_flan.md；output_generate_mark_200_50_top1_dpr_flan.md |
| rag_results_阶段一.csv | 已拆分 | 2 | eval_generate_mark_200_50_top1_dpr_flan_2.md；output_generate_mark_200_50_top5_dpr_flan.md |
| rag_results_#阶段一.csv | 已拆分 | 2 | eval_generate_mark_200_50_top1_dpr_flan_3.md；output_generate_mark_200_50_top1_dpr_flan_2.md |
| rag_results_-阶段一.csv | 已拆分 | 2 | eval_generate_mark_200_50_top1_dpr_flan_4.md；output_generate_mark_200_50_top1_dpr_flan_3.md |
| rag_results_#-pji-top1.txt | 未拆分 | 1 | output_generate_mark_200_50_top1_dpr_phi.md |
| rag_results_#-phi-top3.txt | 未拆分 | 1 | output_generate_mark_200_50_top1_dpr_phi_2.md |
| rag_results_阶段二.csv | 未拆分 | 1 | output_generate_mark_200_50_top1_dpr_phi_3.md |
| rag_results_#阶段三.csv | 已拆分 | 2 | eval_generate_mark_200_50_dpr_flan_vs_phi.md；output_generate_mark_200_50_dpr_phi.md |
| retrieval_results.txt | 已拆分 | 1 | output_retrieval_mixed_dpr_na.md |
| goldContest_results1.csv | 未拆分 | 1 | eval_generate_mark_200_50_goldcontext_dpr_phi.md |
| goldContest_results2.csv | 未拆分 | 1 | eval_generate_mark_200_50_goldcontext_compare_dpr_phi.md |
| goldContext_output.txt | 未拆分 | 1 | output_generate_mark_200_50_goldcontext_dpr_phi.md |
| goldContext_results3.txt | 未拆分 | 1 | eval_generate_mark_200_50_goldcontext_summary_dpr_phi.md |

## 备注

- 当前表格**只保留以 `eval_` 或 `output_` 开头**的命名体系。
- 其它前缀如 `rag_`、`mixed_`、`review_` 均不纳入最终保留版。
- 本文件仅按你当前给定规则做最终收口，未额外修正 `top1/top3/top5` 语义冲突。
