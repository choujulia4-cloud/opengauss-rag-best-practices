class AnswerFormatter:
    def __init__(self):
        self.answer_format = None

    def format(self, rewrite_decision, strategy, answer, retrieval_results,classify_type_requested,classify_type_used,query_type_raw):
        citations = self._build_citations(retrieval_results)
        answer_with_refs = self._attach_reference(answer=answer, citations=citations)

        query = rewrite_decision.original_query
        query_rewrite = rewrite_decision.final_query
        query_type = rewrite_decision.query_type
        rewrite_type_requested = rewrite_decision.rewrite_type_requested
        rewrite_type_used = rewrite_decision.rewrite_type_used
        rewrite_changed = rewrite_decision.changed


        self.answer_format = {
            "query": query,
            "query_type": query_type,
            "query_rewrite": query_rewrite,
            "classify_type_requested": classify_type_requested,
            "classify_type_used":classify_type_used,
            "query_type_raw":query_type_raw,
            "rewrite_type_requested": rewrite_type_requested,
            "rewrite_type_used": rewrite_type_used,
            "rewrite_changed": rewrite_changed,
            "rewrite_route_reason": rewrite_decision.route_reason,
            "rewrite_is_valid": rewrite_decision.is_valid,
            "rewrite_valid_reason": rewrite_decision.validator_reason,
            "raw_rewrite": rewrite_decision.raw_rewrite if rewrite_changed else "",
            "answer_with_refs":answer_with_refs,
            "answer": answer,
            "citations": citations,
            "strategy": strategy,
            "confidence": self._build_confidence(retrieval_results)
        }
        return self.answer_format

    def _build_confidence(self, retrieval_results):
        if not retrieval_results:
            return "No retrieval result returned."
        elif len(retrieval_results) == 1:
            return "Answer is based on a single retrieved passage."
        return "Answer is based on multiple retrieved passages."

    def _build_citations(self, retrieval_results):
        citations = []
        for idx, item in enumerate(retrieval_results[:3], start=1):
            text = item[0].strip().replace("\n", " ")
            score = item[1] if len(item) > 1 else None

            citations.append({
                "id": idx,
                "rank": idx,
                "score_or_distance": score,
                "source_id": f"retrieved_chunk_{idx}",
                "snippet": text[:220],
            })
        return citations

    def _attach_reference(self, answer, citations):
        if not citations:
            return answer
        ref_ids = "".join(f"[{c['id']}]" for c in citations)
        source_lines = "\n".join(
            f"[{c['id']}]{c['source_id']}[score={c['score_or_distance']} | {c['snippet']}]"
            for c in citations
        )
        return f"{answer}\n\nReferences:{ref_ids}\nSources:\n{source_lines}"