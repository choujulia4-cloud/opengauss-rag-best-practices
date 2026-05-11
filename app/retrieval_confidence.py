import re

class RetrievalConfidenceEstimator:
    STOPWORDS = {
        "what", "is", "the", "does", "do", "a", "an", "in", "on", "of", "to",
        "and", "are", "why", "how", "should", "be", "this", "that", "for"        
    }

    def _tokenize(self, text):
        text = text.lower()
        text = re.sub(r"['^a-z0-9\s]", " ", text)
        tokens = text.split()
        return [t for t in tokens if t not in self.STOPWORDS]

    def _keyword_overlap_ratio(self, query, text):
        query_tokens = set(self._tokenize(query))

        if not query_tokens:
            return 0.0

        text_tokens = set(self._tokenize(text))
        overlap_tokens = query_tokens & text_tokens
        return len(overlap_tokens) / len(query_tokens)

    def estimate(self, query, retrieved_results):
        if not retrieved_results:
            print("[WARN] No retrieved results to estimate confidence")
            return {
                "level": "low",
                "reason": "no_results",
                "top1_score": None,
                "keyword_overlap": 0.0,
                "score_signal": "false"
            }
        
        top1_text, top1_score = retrieved_results[0]
        lexical_overlap = self._keyword_overlap_ratio(query, top1_text)

        score_signal = "unknown"
        if top1_score is not None:
            score_signal = "available"

        if lexical_overlap >= 0.5:
            level = "high"
            reason = "strong_keyword_overlap"
        elif lexical_overlap >= 0.25:
            level = "medium"
            reason = "partial_keyword_overlap"
        else:
            level = "low"
            reason = "weak_keyword_overlap"

        return {
            "level": level,
            "reason": reason,
            "top1_score": top1_score,
            "keyword_overlap": lexical_overlap,
            "score_signal": score_signal
        }