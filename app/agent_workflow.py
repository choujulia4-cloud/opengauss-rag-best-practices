from app.rag_pipeline import RagPipeline
from app.query_router import QueryRouter
from app.answer_formatter import AnswerFormatter
from app.retrieval_strategy import RetrievalStrategySelector

class AgentWorkflow:
    def __init__(self, rag_pipeline, classify_type="rules", rewrite_type="none", use_dynamic_strategy=False):
        self.rag_pipeline = rag_pipeline
        self.router = QueryRouter(rag_pipeline=rag_pipeline)
        self.answer_formatter = AnswerFormatter()
        self.strategy_selector = RetrievalStrategySelector(use_dynamic_strategy=use_dynamic_strategy)
        self.classify_type = classify_type
        self.rewrite_type = rewrite_type

    def run(self, query, classify_type=None, rewrite_type=None):
        """
        执行完整的 agent 流程: 意图识别 - 动态策略 - 向量检索 - 生成推理

        **【Args】
        query: 【必传】用户原始问题 
        classify_type
        rewrite_type: 

        ** 【Return】
        answer_format: [dict]
            "query": query,
            "query_type": query_type,
            "query_rewrite": query_rewrite,
            "classify_type_requested": classify_type_requested,
            "classify_type_used":classify_type_used,
            "query_type_raw":query_type_raw,
            "rewrite_type_requested": rewrite_type_requested,
            "rewrite_type_used": rewrite_type_used,
            "rewrite_changed": rewrite_changed,
            "rewrite_route_reason": rewrite_decision.route_reason if rewrite_changed else "",
            "rewrite_is_valid": rewrite_decision.is_valid,
            "rewrite_valid_reason": rewrite_decision.validator_reason,
            "raw_rewrite": rewrite_decision.raw_rewrite if rewrite_changed else "",
            "answer_with_refs":answer_with_refs,
            "answer": answer,
            "citations": citations,
            "strategy": strategy,
            "confidence": self._build_confidence(retrieval_results)
        """
        actual_classify_type = classify_type or self.classify_type
        actual_rewrite_type = rewrite_type or self.rewrite_type
        query_type = self.router.classify(query=query, classify_type=actual_classify_type)
        rewrite_decision = self.router.rewrite(query=query, rewrite_type=actual_rewrite_type)

        query_rewrite = rewrite_decision.final_query


        retrieval_strategy = self.strategy_selector.select(query_type=query_type)
        gen_config = retrieval_strategy["generation_config"]
        retrieval_results = self.rag_pipeline.retrieve(
            query=query_rewrite, 
            top_k=retrieval_strategy["top_k"], 
            operator=retrieval_strategy["operator"])
        retrieval_context = self.rag_pipeline.build_context(retrieved_results=retrieval_results)
        answer = self.rag_pipeline.generate_answer(
            query=query_rewrite, 
            context=retrieval_context, 
            answer_style=retrieval_strategy["answer_style"],
            max_new_tokens=gen_config["max_new_tokens"],
            temperature=gen_config["temperature"],
            do_sample=gen_config["do_sample"])
        answer_format = self.answer_formatter.format(
            classify_type_requested=actual_classify_type,
            classify_type_used=self.router.actual_classify_type,
            query_type_raw=self.router.query_type_raw,
            rewrite_decision=rewrite_decision,
            strategy=retrieval_strategy, 
            answer=answer, 
            retrieval_results=retrieval_results)
        return answer_format


