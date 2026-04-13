```json
{
  "document_type": "review",
  "test_stage_type": "chunk",
  "chunk_method": "mixed",
  "max_length": "mixed",
  "overlap": "mixed",
  "sim_operator": "na",
  "embed_model": "na",
  "llm_model": "na",
  "original_file": "/raw/split_chunk_results.txt"
}
```

# review_chunk_mixed_na_na.md

## 配置参数

| key | value |
|---|---|
| document_type | review |
| test_stage_type | chunk |
| chunk_method | mixed |
| max_length | mixed |
| overlap | mixed |
| sim_operator | na |
| embed_model | na |
| llm_model | na |
| original_file | /raw/split_chunk_results.txt |

---
title: Chunk Statistics and Overlap Distribution Summary
experiment_type: chunk
chunk_method: mixed
max_length: mixed
overlap: mixed
sim_operator: null
embed_model: null
llm_model: null
date: 20260408
original_file: split_chunk_results.txt
original_path: \docs\split_chunk_results.txt
normalized_from: "direct_standardization"
---

# Chunk Statistics and Overlap Distribution Summary

## 配置参数

| key | value |
|---|---|
| experiment_scope | chunk statistics |
| compared_chunk_methods | length, mark |
| compared_max_length | 100, 150, 200 |
| compared_overlap | 0, 10, 20, 50, 100 |
| source | 原始统计输出 |

## 原始终端输出
| cutting_type | num_chunks | avg_chunk_length | min_chunk_length | max_chunk_length | median_chunk_length | std_chunk_length | num_empty_chunks | num_too_short_chunks | num_too_long_chunks | avg_words_per_chunk | avg_overlap_chars |
|---|---|---|---|---|---|---|---|---|---|---|---|
| length 100 10 | 130 | 92.13 | 20 | 100 | 96.0 | 13.86 | 0 | 0 | 0 | 13.08 | 0.09 |
| length 150 10 | 90 | 133.62 | 8 | 156 | 146.0 | 35.31 | 0 | 4 | 1 | 18.9 | 0.18 |
| length 200 10 | 67 | 179.7 | 19 | 200 | 195 | 39.79 | 0 | 1 | 0 | 25.37 | 0.05 |
| mark 100 10 | 161 | 74.33 | 5 | 106 | 90 | 28.63 | 0 | 12 | 3 | 10.58 | 0.17 |
| mark 150 10 | 107 | 112.15 | 12 | 150 | 124 | 34.73 | 0 | 2 | 0 | 15.89 | 0.05 |
| mark 200 10 | 82 | 146.65 | 51 | 200 | 148.5 | 36.46 | 0 | 0 | 0 | 20.73 | 0.0 |
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
| cutting_type | num_chunks | avg_chunk_length | min_chunk_length | max_chunk_length | median_chunk_length | std_chunk_length | num_empty_chunks | num_too_short_chunks | num_too_long_chunks | avg_words_per_chunk | avg_overlap_chars |
|---|---|---|---|---|---|---|---|---|---|---|---|
| mark 150 0 | 107 | 112.15 | 12 | 150 | 124 | 34.73 | 0 | 2 | 0 | 15.89 | 0.05 |
| mark 150 10 | 107 | 112.15 | 12 | 150 | 124 | 34.73 | 0 | 2 | 0 | 15.89 | 0.05 |
| mark 150 20 | 107 | 112.42 | 12 | 156 | 124 | 35.0 | 0 | 2 | 2 | 15.91 | 0.3 |
| mark 150 50 | 107 | 114.94 | 12 | 196 | 125 | 37.9 | 0 | 2 | 9 | 16.26 | 2.78 |
| mark 200 0 | 82 | 146.65 | 51 | 200 | 148.5 | 36.46 | 0 | 0 | 0 | 20.73 | 0.0 |
| mark 200 10 | 82 | 146.65 | 51 | 200 | 148.5 | 36.46 | 0 | 0 | 0 | 20.73 | 0.0 |
| mark 200 20 | 82 | 146.65 | 51 | 200 | 148.5 | 36.46 | 0 | 0 | 0 | 20.73 | 0.0 |
| mark 200 50 | 82 | 147.71 | 51 | 200 | 150.5 | 36.54 | 0 | 0 | 0 | 20.89 | 1.05 |

=== length 暂时不适合作为主候选 ===
150-10 更偏向mark
没有超长块、过短块更少、上限控制更稳定
200-10 更偏向mark
| min=51 | 几乎没有尾部残缺问题；too_short=0；chunk数量虽多，但在可接受范围 |
|---|---|

---

===`mark 100 10` 可以基本排除 ===
* chunk 太碎、过短块多、还有超长块
* `100` 对这份英文技术文本偏小;句子切分后再拼接，很多块装不稳

---

=== mark 150 下不要继续增大 overlap ===
* mark 150 0 和 mark 150 10 完全一样，而 mark 150 20开始出现超长块，50 时超长块明显增多且 max_chunk_length 到了 196

=== mark 200 更稳定 ===
* mark 200 0 / 10 / 20 完全一致；mark 200 50 也没有超长块
* num_too_short_chunks 始终是 0
* max_chunk_length 始终受控在 200

** 在基于句子边界的 mark 切分下，max_chunk_size=150 时仅适合较小 overlap（0~10），
** 而 max_chunk_size=200 对 overlap 更稳定，在 overlap=50 下仍能保持长度约束与 chunk 质量。
** 因此，后续检索测试优先选择 mark 150 10、mark 200 10 和 mark 200 50 作为候选配置。
---------------------------------------------------------------------------------------------------------------------------------
