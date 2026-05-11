import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.agent_workflow import AgentWorkflow
from app.rag_pipeline import RagPipeline
import time
import sys
import json
import random
from collections import defaultdict



QUERY_BANK = [
    {"id": "Q01", "gold_type": "definition", "query": "What role does OpenGauss play in a RetrievalQA pipeline?"},
    {"id": "Q02", "gold_type": "definition", "query": "What is stored in the database besides the original text chunks?"},
    {"id": "Q03", "gold_type": "definition", "query": "Why must long source documents be divided into smaller chunks?"},
    {"id": "Q04", "gold_type": "definition", "query": "What factors should be treated as tunable parameters in chunking?"},
    {"id": "Q05", "gold_type": "definition", "query": "What are the two embedding sources mentioned in this project?"},
    {"id": "Q06", "gold_type": "definition", "query": "Why are HuggingFace models suitable for local execution?"},
    {"id": "Q07", "gold_type": "definition", "query": "Why can Cohere embeddings reduce local computation pressure?"},
    {"id": "Q08", "gold_type": "definition", "query": "What metadata fields are recommended for the OpenGauss embedding table?"},

    {"id": "Q09", "gold_type": "comparison", "query": "What are the main differences between HuggingFace embeddings and Cohere embeddings?"},
    {"id": "Q10", "gold_type": "comparison", "query": "How do short chunks and long chunks affect retrieval quality differently?"},
    {"id": "Q11", "gold_type": "comparison", "query": "What is the difference between retrieval evaluation and generation evaluation?"},
    {"id": "Q12", "gold_type": "comparison", "query": "How does offline preprocessing on a stronger machine differ from online query handling on an edge device?"},
    {"id": "Q13", "gold_type": "comparison", "query": "What is the difference between a desktop deployment environment and an RK3568 deployment environment?"},
    {"id": "Q14", "gold_type": "comparison", "query": "Why is a best-practice report more useful than isolated coding experiments?"},
    {"id": "Q15", "gold_type": "comparison", "query": "How is BentoML different from an embedding model in this project?"},
    {"id": "Q16", "gold_type": "comparison", "query": "What is the difference between fixed-length chunking and sentence-based chunking?"},

    {"id": "Q17", "gold_type": "list_or_enumeration", "query": "List the main source types of raw documents in a typical RetrievalQA workflow."},
    {"id": "Q18", "gold_type": "list_or_enumeration", "query": "What tunable parameters are involved in document chunking, and list common value ranges of them."},
    {"id": "Q19", "gold_type": "list_or_enumeration", "query": "List the advantages of adopting HuggingFace local embedding models."},
    {"id": "Q20", "gold_type": "list_or_enumeration", "query": "List the limitations of using Cohere hosted embedding models."},
    {"id": "Q21", "gold_type": "list_or_enumeration", "query": "List key metadata fields included in the practical OpenGauss table for embedding storage."},
    {"id": "Q22", "gold_type": "list_or_enumeration", "query": "List three common distance operators used for vector similarity search."},
    {"id": "Q23", "gold_type": "list_or_enumeration", "query": "List typical evaluation indicators for retrieval performance in a RetrievalQA system."},
    {"id": "Q24", "gold_type": "list_or_enumeration", "query": "List the main contents that generation evaluation of RetrievalQA focuses on."},

    {"id": "Q25", "gold_type": "deployment_or_recommendation", "query": "What dimensions should be tested systematically for best-practice exploration?"},
    {"id": "Q26", "gold_type": "deployment_or_recommendation", "query": "Which chunking parameters should be tuned in experiments?"},
    {"id": "Q27", "gold_type": "deployment_or_recommendation", "query": "What retrieval parameters should be compared during optimization?"},
    {"id": "Q28", "gold_type": "deployment_or_recommendation", "query": "What deployment-related indicators should be measured on an edge device?"},
    {"id": "Q29", "gold_type": "deployment_or_recommendation", "query": "Why should large-scale embedding generation be moved off the edge device?"},
    {"id": "Q30", "gold_type": "deployment_or_recommendation", "query": "What should the edge device focus on in a production-style deployment strategy?"},
    {"id": "Q31", "gold_type": "deployment_or_recommendation", "query": "Why does containerization remain useful even though it cannot remove hardware constraints?"},
    {"id": "Q32", "gold_type": "deployment_or_recommendation", "query": "What kind of deployment role is most suitable for RK3568 in this project?"},

    {"id": "Q33", "gold_type": "unknown", "query": "How does the combination of OpenGauss and BentoML help transform a RetrievalQA prototype into a deployable service, and what key issues should be noted during this process?"},
    {"id": "Q34", "gold_type": "unknown", "query": "What are the reasons why chunking strategy directly affects retrieval quality, and can you give examples of inappropriate chunk sizes and their consequences?"},
    {"id": "Q35", "gold_type": "unknown", "query": "Explain the role of embedding vectors in the RetrievalQA pipeline, and compare the differences in how HuggingFace and Cohere generate these vectors."},
    {"id": "Q36", "gold_type": "unknown", "query": "Why is it necessary to separate retrieval evaluation from generation evaluation in a practical RetrievalQA system, and what indicators are used to measure each?"},
    {"id": "Q37", "gold_type": "unknown", "query": "How does containerization with Docker simplify the deployment of OpenGauss on AArch64 platforms like RK3568, and what hardware constraints still need to be considered?"},
    {"id": "Q38", "gold_type": "unknown", "query": "List the key metadata fields in an OpenGauss table for embedding storage, and explain why these fields are important for experimentation and optimization."},
    {"id": "Q39", "gold_type": "unknown", "query": "What is the division of labor between a development workstation and an RK3568 edge device in a production-style deployment, and how does this division address resource constraints?"},
    {"id": "Q40", "gold_type": "unknown", "query": "Compare the advantages and disadvantages of fixed-length chunking and sentence-based chunking, and under what circumstances is each more suitable?"},

    {"id": "Q41", "gold_type": "unknown", "query": "OpenGauss role?"},
    {"id": "Q42", "gold_type": "comparison", "query": "Cohere vs HuggingFace?"},
    {"id": "Q43", "gold_type": "deployment_or_recommendation", "query": "RK3568 solution?"},
    {"id": "Q44", "gold_type": "unknown", "query": "Why is it useful there?"},
    {"id": "Q45", "gold_type": "unknown", "query": "Why should it be moved off the edge device?"},
    {"id": "Q46", "gold_type": "unknown", "query": "How does this help deployment?"},
    {"id": "Q47", "gold_type": "comparison", "query": "What are the differences between HF embeddings and Cohere embeddings?"},
    {"id": "Q48", "gold_type": "deployment_or_recommendation", "query": "Why is HF better for local RAG deployment?"},
    {"id": "Q49", "gold_type": "deployment_or_recommendation", "query": "What should RK3568 focus on in prod-style RAG?"},
    {"id": "Q50", "gold_type": "unknown", "query": "Which one is better here?"},
    {"id": "Q51", "gold_type": "unknown", "query": "What is the best choice for this project?"},
    {"id": "Q52", "gold_type": "unknown", "query": "Why does that matter?"},
    {"id": "Q53", "gold_type": "unknown", "query": "What is the recommended CUDA version for this project?"},
    {"id": "Q54", "gold_type": "unknown", "query": "Which cloud region should Cohere API be deployed in?"},
    {"id": "Q55", "gold_type": "unknown", "query": "What benchmark result does this project report for FAISS GPU indexing?"},
    {"id": "Q56", "gold_type": "unknown", "query": "Which Linux kernel patch is required for RK3568 in this project?"},
]

type_id_list = defaultdict(list)
for item in QUERY_BANK:
    type_id_list[item["gold_type"]].append(item["id"])

queries_id_list = []
random.seed(42)
for typ, ids in type_id_list.items():
    sampled = random.sample(ids, min(2, len(ids)))
    queries_id_list.extend(sampled)

    
EXPERIMENT_CONFIGS = {
    "CFG-01": {"classify_type": "rules",  "rewrite_type": "none",   "use_dynamic_strategy": False, "fixed_top_k": 5, "enable_confidence": False, "query_ids": [f"Q{i:02d}" for i in range(1, 41)]},
    "CFG-02": {"classify_type": "model",  "rewrite_type": "none",   "use_dynamic_strategy": False, "fixed_top_k": 5, "enable_confidence": False, "query_ids": [f"Q{i:02d}" for i in range(1, 41)]},
    "CFG-03": {"classify_type": "hybrid", "rewrite_type": "none",   "use_dynamic_strategy": False, "fixed_top_k": 5, "enable_confidence": False, "query_ids": [f"Q{i:02d}" for i in range(1, 41)]},
    "CFG-04": {"classify_type": "rules",  "rewrite_type": "none",   "use_dynamic_strategy": False, "fixed_top_k": 5, "enable_confidence": False, "query_ids": ["Q01", "Q09", "Q17", "Q25"] + [f"Q{i:02d}" for i in range(41, 57)]},
    "CFG-05": {"classify_type": "rules",  "rewrite_type": "rules",  "use_dynamic_strategy": False, "fixed_top_k": 5, "enable_confidence": False, "query_ids": ["Q01", "Q09", "Q17", "Q25"] + [f"Q{i:02d}" for i in range(41, 57)]},
    "CFG-06": {"classify_type": "rules",  "rewrite_type": "model",  "use_dynamic_strategy": False, "fixed_top_k": 5, "enable_confidence": False, "query_ids": ["Q01", "Q09", "Q17", "Q25"] + [f"Q{i:02d}" for i in range(41, 57)]},
    "CFG-07": {"classify_type": "rules",  "rewrite_type": "hybrid", "use_dynamic_strategy": False, "fixed_top_k": 5, "enable_confidence": False, "query_ids": ["Q01", "Q09", "Q17", "Q25"] + [f"Q{i:02d}" for i in range(41, 57)]},
    # "CFG-08": {"classify_type": "hybrid", "rewrite_type": "hybrid", "use_dynamic_strategy": False, "fixed_top_k": 5, "enable_confidence": False, "query_ids": [f"Q{i:02d}" for i in range(1, 41)]},
    # "CFG-09": {"classify_type": "hybrid", "rewrite_type": "hybrid", "use_dynamic_strategy": True,  "fixed_top_k": None, "enable_confidence": False, "query_ids": [f"Q{i:02d}" for i in range(1, 41)]},
    "CFG-08": {"classify_type": "hybrid", "rewrite_type": "hybrid", "use_dynamic_strategy": False, "fixed_top_k": 5, "enable_confidence": False, "query_ids": queries_id_list},
    "CFG-09": {"classify_type": "hybrid", "rewrite_type": "hybrid", "use_dynamic_strategy": True,  "fixed_top_k": None, "enable_confidence": False, "query_ids": queries_id_list},    
    "CFG-10": {"classify_type": "hybrid", "rewrite_type": "hybrid", "use_dynamic_strategy": True,  "fixed_top_k": None, "enable_confidence": False, "query_ids": [f"Q{i:02d}" for i in range(1, 41)]},

    "CFG-11": {"classify_type": "hybrid", "rewrite_type": "hybrid", "use_dynamic_strategy": True,  "fixed_top_k": None, "enable_confidence": False, "query_ids": [f"Q{i:02d}" for i in range(41, 57)]},
    # "CFG-12": {"classify_type": "hybrid", "rewrite_type": "hybrid", "use_dynamic_strategy": True,  "fixed_top_k": None, "enable_confidence": True,  "query_ids": [f"Q{i:02d}" for i in range(41, 57)]},  # 暂时跑不了， confidence 没有真正接入代码中
}

def build_pipeline():
    # 这里的 chunk_config 都是采用的默认结果  
    # 动态策略的实现主要体现在 AgentWorkflow 和 RetrievalStrategySelector 中，rag_pipeline 只负责执行给定的策略
    return RagPipeline()

def build_workflow(config, rag_pipeline):
    classify_type = config["classify_type"]
    rewrite_type = config["rewrite_type"]
    use_dynamic_strategy = config["use_dynamic_strategy"]

    return AgentWorkflow(
        rag_pipeline=rag_pipeline,
        classify_type=classify_type,
        rewrite_type=rewrite_type,
        use_dynamic_strategy=use_dynamic_strategy
    )

def get_queries_by_ids(query_ids):
    bank = {item["id"]: item for item in QUERY_BANK}
    return [bank[qid] for qid in query_ids]

def flatten_result(cfg_id, query_item, result_format, latency_s):
    """
    单个问题的结果格式化

    Args:
    cfg_id
    query_item
    result_format:
            # "query": query,
            # "query_type": query_type,
            # "query_rewrite": query_rewrite,
            # "classify_type_requested": classify_type_requested,
            # "classify_type_used":classify_type_used,
            # "query_type_raw":query_type_raw,
            # "rewrite_type_requested": rewrite_type_requested,
            # "rewrite_type_used": rewrite_type_used,
            # "rewrite_changed": rewrite_changed,
            # "rewrite_route_reason": rewrite_decision.route_reason if rewrite_changed else "",
            # "rewrite_is_valid": rewrite_decision.is_valid,
            # "rewrite_valid_reason": rewrite_decision.validator_reason,
            # "raw_rewrite": rewrite_decision.raw_rewrite if rewrite_changed else "",
            # "answer_with_refs":answer_with_refs,
            # "answer": answer,
            # "citations": citations,
            # "strategy": strategy,
            # "confidence": self._build_confidence(retrieval_results)
    latency_s

    """
    config = EXPERIMENT_CONFIGS[cfg_id]

    return {
        "config_id":cfg_id,
        "query_id":query_item["id"],
        "query":query_item["query"],
        "gold_type":query_item["gold_type"],
        "predicted_type":result_format["query_type"],
        "predicted_type_raw": result_format["query_type_raw"],
        "classify_type":config["classify_type"],
        "actual_classify_type": result_format["classify_type_used"],
        "rewrite_type_requested":result_format["rewrite_type_requested"],
        "rewrite_type_used":result_format["rewrite_type_used"],
        "query_rewrite":result_format["query_rewrite"],
        "query_rewrite_raw":result_format["raw_rewrite"],
        "rewrite_changed":result_format["rewrite_changed"],
        "rewrite_route_reason":result_format["rewrite_route_reason"],
        "rewrite_is_valid":result_format["rewrite_is_valid"],
        "rewrite_valid_reason":result_format["rewrite_valid_reason"],
        "strategy_top_k":result_format["strategy"]["top_k"], 
        # "strategy_operator":, # 全部都是 <#>
        "strategy_generation_max_new_tokens":result_format["strategy"]["generation_config"]["max_new_tokens"],        
        "strategy_answer_style":result_format["strategy"]["answer_style"],
        # "citation_count":,  # 这里的 citation_count = top_k
        # "top1_score":,  # 这部分在 citations 中已经集成了
        "citations":result_format["citations"],  # 返回的 answer 中也存在这部分
        # "confidence":,  # 这部分的逻辑只是检索到的文本的数量，目前直接等于top_k
        "answer":result_format["answer"],
        "latency_s":round(latency_s, 4),
    }

def print_markdown_record(record):
    print("=" * 100)
    print(f"### Query ID: {record['query_id']}")
    print(f"- Config ID: {record['config_id']}")
    print(f"- Query: {record['query']}")
    print(f"- Gold Type: {record['gold_type']}")
    print(f"- Predicted Query Type: {record['predicted_type']}")
    print(f"- Predicted Query Type Raw: {record['predicted_type_raw']}")
    print(f"- classify_type: {record['classify_type']}")
    print(f"- Actual Classify Type: {record['actual_classify_type']}")
    print(f"- query_rewrite: {record['query_rewrite']}"),
    print(f"- query_rewrite_raw: {record['query_rewrite_raw']}"),
    print(f"- rewrite_type_requested: {record['rewrite_type_requested']}"),
    print(f"- rewrite_type_used: {record['rewrite_type_used']}"),
    print(f"- Rewrite Changed: {record['rewrite_changed']}")
    print(f"- Rewrite_is_valid: {record['rewrite_is_valid']}")
    print(f"- Rewrite valid reason: {record['rewrite_valid_reason']}")
    print(f"- Rewrite route reason: {record['rewrite_route_reason']}")
    print(f"- Retrieval Strategy: strategy_top_k={record['strategy_top_k']}")
    print(f"- Generate Strategy: max_new_tokens={record['strategy_generation_max_new_tokens']}  answer_style= {record['strategy_answer_style']}")
    print(f"- Response Latency: {record['latency_s']}")
    print("- Retrieved Evidence Summary:")    
    if record["citations"]:
        for c in record["citations"]:
            print(f"  - [{c['id']}] {c['source_id']} | score={c['score_or_distance']} | {c['snippet']}")
    else:
        print("  - None")
    print("- Final Answer:")
    print(record["answer"])
    # print("- JSON Record:")  # 暂时不需要 JSON 格式的终端打印
    # print(json.dumps(record, ensure_ascii=False))



def run_config(cfg_id):
    if cfg_id not in EXPERIMENT_CONFIGS:
        return ValueError(f"Invalid config ID:{cfg_id}")
    
    config = EXPERIMENT_CONFIGS[cfg_id]
    rag_pipeline = build_pipeline()
    workflow = build_workflow(config=config, rag_pipeline=rag_pipeline)

    queries = get_queries_by_ids(query_ids=config["query_ids"])

    all_records = []
    for query in queries:
        start_time = time.time()
        answer_raw_format = workflow.run(
            query=query["query"], 
            classify_type=config["classify_type"],
            rewrite_type=config["rewrite_type"])

        latency_s = time.time() - start_time
        actual_classify_type = workflow.router.actual_classify_type
        query_type_raw = workflow.router.query_type_raw
        record = flatten_result(
            cfg_id=cfg_id, 
            query_item=query, 
            result_format=answer_raw_format, 
            latency_s=latency_s)
        all_records.append(record)
        print_markdown_record(record=record)
    print("=" * 100)
    print(f"# Summary for {cfg_id}")
    print(f"- Query Count: {len(all_records)}")
    if all_records:
        avg_latency = sum(r["latency_s"] for r in all_records) / len(all_records)
        print(f"- Avg Latency: {avg_latency:.4f}")
    for record in all_records:
        file_name = f"./data/agentWorkflow_json/{record['config_id']}_{record['query_id']}_output.json"
        with open(file_name, "w", encoding="utf-8") as f:
            json.dump(record, f, ensure_ascii=False, indent=2)
    

if __name__ == "__main__":
    cfg_id = sys.argv[1] if len(sys.argv) > 1 else "CFG-01"
    run_config(cfg_id=cfg_id)
