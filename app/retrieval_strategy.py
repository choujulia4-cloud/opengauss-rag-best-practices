

class RetrievalStrategySelector:
    def __init__(self, use_dynamic_strategy=False):
        self.use_dynamic_strategy = use_dynamic_strategy
    
    def select(self, query_type, use_dynamic_strategy=None):
        cur_use_dynamic_strategy = use_dynamic_strategy if use_dynamic_strategy is not None else self.use_dynamic_strategy
        strategy_map = {
            "definition": {
                "top_k": 3,
                "operator": "<#>",
                "need_evidence": True,
                "answer_style": "concise_grounded",
                "generation_config": {
                    "do_sample": False,
                    "temperature": 1.0,
                    "max_new_tokens": 256
                }
            },
            "comparison": {
                "top_k": 4,
                "operator": "<#>",
                "need_evidence": True,
                "answer_style": "compare_points",
                "generation_config": {
                    "do_sample": False,
                    "temperature": 1.0,
                    "max_new_tokens": 512
                }
            },
            "list_or_enumeration": {
                "top_k": 5,
                "operator": "<#>",
                "need_evidence": True,
                "answer_style": "bullet_like",
                "generation_config": {
                    "do_sample": False,
                    "temperature": 1.0,
                    "max_new_tokens": 1024
                }
            },
            "deployment_or_recommendation": {
                "top_k": 5,
                "operator": "<#>",
                "need_evidence": True,
                "answer_style": "decision_reasoning",
                "generation_config": {
                    "do_sample": False,
                    "temperature": 1.0,
                    "max_new_tokens": 2048
                }
            },
            "unknown": {
                "top_k": 3,
                "operator": "<#>",
                "need_evidence": True,
                "answer_style": "safe_default",
                "generation_config": {
                    "do_sample": False,
                    "temperature": 1.0,
                    "max_new_tokens": 256
                }
            } 
        }
        if cur_use_dynamic_strategy == False:
            return strategy_map["unknown"]
        return strategy_map.get(query_type, strategy_map["unknown"])