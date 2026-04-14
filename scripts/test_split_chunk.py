from datasets import load_from_disk
import os
import re
import statistics
# 计算相邻两个chunk之间的最大重叠字符数
def compute_overlap_chars(chunk1, chunk2, max_check=200):
    max_len = min(len(chunk1), len(chunk2), max_check)
    for i in range(max_len, 0, -1):
        if chunk1[-i:] == chunk2[:i]:
            return i

    return 0

def compute_chunk_metrics(dataset_path, too_short_threshold=20):

    dataset = load_from_disk(dataset_path)
    texts = [item["text"] for item in dataset]

    if not texts:
        return {
            "dataset_path": dataset_path,
            "num_chunks": 0,
            "avg_chunk_length": 0,
            "min_chunk_length": 0,
            "max_chunk_length": 0,
            "median_chunk_length": 0,
            "std_chunk_length": 0,
            "num_empty_chunks": 0,
            "num_too_short_chunks": 0,
            "num_too_long_chunks": 0,
            "avg_words_per_chunk": 0,
            "avg_overlap_chars": 0,
        }

    folder_name = os.path.basename(dataset_path)
    match = re.match(r"kb_chunks_datasets_(\w+)_(\d+)_(\d+)", folder_name)
    if match:
        cutting_type = match.group(1)
        max_chunk_size = int(match.group(2))
        overlap = int(match.group(3))
    else:
        cutting_type = "unknown"
        max_chunk_size = None
        overlap = None
    
    lengths = [len(t) for t in texts]
    word_counts = [len(t.split()) for t in texts]

    num_chunks = len(texts)
    avg_chunk_length = sum(lengths) / num_chunks
    min_chunk_length = min(lengths)
    max_chunk_length = max(lengths)
    median_chunk_length = statistics.median(lengths)
    std_chunk_length = statistics.pstdev(lengths) if len(lengths) > 1 else 0

    num_empty_chunks = sum(1 for t in texts if not t.strip())
    num_too_short_chunks = sum(1 for t in texts if len(t.strip()) < too_short_threshold)
    num_too_long_chunks = (
        sum(1 for t in texts if len(t) > max_chunk_size)
        if max_chunk_size is not None else 0
    )
    avg_words_per_chunk = sum(word_counts) / num_chunks 

    overlap_num_list = []
    for i in range(len(texts) - 1):
        overlap_chars_num = compute_overlap_chars(texts[i], texts[i + 1])
        overlap_num_list.append(overlap_chars_num)
    
    avg_overlap_chars = sum(overlap_num_list) / len(overlap_num_list) if overlap_num_list else 0

    return {
        "dataset_path": dataset_path,
        "cutting_type": cutting_type,
        "max_chunk_size": max_chunk_size,
        "overlap": overlap,
        "num_chunks": num_chunks,
        "avg_chunk_length": round(avg_chunk_length, 2),
        "min_chunk_length": min_chunk_length,
        "max_chunk_length": max_chunk_length,
        "median_chunk_length": round(median_chunk_length, 2),
        "std_chunk_length": round(std_chunk_length, 2),
        "num_empty_chunks": num_empty_chunks,
        "num_too_short_chunks": num_too_short_chunks,
        "num_too_long_chunks": num_too_long_chunks,
        "avg_words_per_chunk": round(avg_words_per_chunk, 2),
        "avg_overlap_chars": round(avg_overlap_chars, 2)
    }

def collect_all_chunk_metrics(data_dir="./data"):
    results = []
    for name in os.listdir(data_dir):
        path = os.path.join(data_dir, name)
        if os.path.isdir(path) and name.startswith("kb_chunks_datasets_mark_200"):
            try:
                metrics = compute_chunk_metrics(path)
                results.append(metrics)
            except Exception as e:
                print(f"Failed to process {path}: {e}")
    results.sort(key=lambda x: (
        str(x.get("cutting_type")),
        x.get("max_chunk_size") if x.get("max_chunk_size") is not None else -1,
        x.get("overlap") if x.get("overlap") is not None else -1,
    ))
    return results

def print_metrics_table(results):
    if not results:
        print("[ERROR] No results found.")
        return

    headers = [
        "cutting_type", "max_chunk_size", "overlap",
        "num_chunks", "avg_chunk_length", "min_chunk_length", "max_chunk_length",
        "median_chunk_length", "std_chunk_length",
        "num_empty_chunks", "num_too_short_chunks", "num_too_long_chunks",
        "avg_words_per_chunk", "avg_overlap_chars"
    ]
    print("\t".join(headers))
    for r in results:
        print("\t".join(str(r.get(h, "")) for h in headers))

if __name__ == "__main__":
    results = collect_all_chunk_metrics()
    print_metrics_table(results)