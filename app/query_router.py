import re
from dataclasses import dataclass

@dataclass
class RewriteDecision:
    original_query: str
    final_query:str
    rewrite_type_requested: str
    rewrite_type_used: str
    query_type: str
    changed: bool
    is_valid: bool
    validator_reason: str
    route_reason: str
    raw_rewrite:str = ""

class QueryRouter:
    VALID_TYPES = [
        "definition", 
        "comparison", 
        "list_or_enumeration", 
        "deployment_or_recommendation", 
        "unknown"
        ]

    INVALID_REWRITE_PREFIXES = [
        "here is",
        "rewritten query",
        "optimized query",
        "the rewritten query",
        "explanation:",
        "after optimization:",
        "this query"
    ]
    PRONOUN_HINTS = ["it", "this", "that", "they", "these", "those", "previous", "above", "former"]
    def __init__(self, rag_pipeline=None,actual_classify_type=""):
        self.query_type = "unknown"
        self.rag_pipeline = rag_pipeline
        self.actual_classify_type = actual_classify_type
        self.query_type_raw = ""

    def classify(self, query, classify_type="rules"):
        self.actual_classify_type = classify_type
        self.query_type_raw = ""
        if classify_type == "rules":
            self.actual_classify_type = "rules"
            query_type = self._classify_by_rules(query)
        elif classify_type == "model":
            self.actual_classify_type = "model"
            query_type = self._classify_by_model(query)
        elif classify_type == "hybrid":
            self.actual_classify_type = "rules"
            query_type = self._classify_by_rules(query=query)
            if query_type == "unknown":
                print("[WARN] Hybrid classify result is 'unknown', try to classify by model.")
                self.query_type_raw = query_type
                self.actual_classify_type = "model"
                query_type = self._classify_by_model(query=query)
                if query_type not in self.VALID_TYPES:
                    print("[WARN] Hybrid classify - rules - model, still invalid query type, fallback to 'unknown'. ")
                    self.query_type_raw = query_type
                    self.actual_classify_type = "default"
                    query_type = "unknown"                    
        else:
            print("[WARN] Invalid classify type! Fallback to rules.")
            self.actual_classify_type = "rules"
            query_type = self._classify_by_rules(query)

        if query_type not in self.VALID_TYPES:
            self.query_type_raw = query_type
            print(f"[WARN] Invalid query type: {self.query_type} , fallback to unknown. ")
            query_type = "unknown"
            self.actual_classify_type = "default"

        self.query_type = query_type
        return self.query_type

    def rewrite(self, query, rewrite_type="none", classify_type="rules", confidence=None):
        """
        问题改写

        Argv:
        query, rewrite_type="none", classify_type="rules", confidence=None

        Return:
        RewriteDecision(
                original_query,  # 处理前后空格和连续空格 query
                final_query  # 最终处理得到的 query
                rewrite_type_requested  # 要求使用的 rewrite_type
                rewrite_type_used  # 实际使用的 rewrite_type
                query_type  # 问题类型
                changed  # query 是否改写
                is_valid  # 改写后的 query 是否合法
                validator_reason  # 是否合法的判断理由
                route_reason  # 选择改写策略的理由
                raw_rewrite  # 原始改写结果
            )
        """
        
        original_query = self._normalize_query(query=query)
        query_type = self.classify(query=query, classify_type=classify_type)

        if rewrite_type == "none":
            return RewriteDecision(
                original_query=original_query,
                final_query=original_query,
                rewrite_type_requested=rewrite_type,
                rewrite_type_used="none",
                query_type=query_type,
                changed=False,
                is_valid=True,
                validator_reason="no_rewrite_baseline",
                route_reason="explicit_none",
                raw_rewrite=""
            )
        
        if rewrite_type == "rules":
            raw_rewrite = self._rewrite_by_rules(query=query)
            final_query, is_valid, validator_reason = self._validate_rewrite(
                original_query=original_query,
                rewritten_query=raw_rewrite
            )
            return RewriteDecision(
                original_query=original_query,
                final_query=final_query,
                rewrite_type_requested=rewrite_type,
                rewrite_type_used="rules" if is_valid else "none",
                query_type=query_type,
                changed=(final_query != original_query),
                is_valid=is_valid,
                validator_reason=validator_reason,
                route_reason="explicit_rules",
                raw_rewrite=raw_rewrite
            )

        if rewrite_type == "model":
            raw_rewrite = self._rewrite_by_model(query=query)
            final_query, is_valid, validator_reason = self._validate_rewrite(
                original_query=original_query,
                rewritten_query=raw_rewrite
            )
            return RewriteDecision(
                original_query=original_query,
                final_query=final_query,
                rewrite_type_requested=rewrite_type,
                rewrite_type_used="model" if is_valid else "none",
                query_type=query_type,
                changed=(final_query != original_query),
                is_valid=is_valid,
                validator_reason=validator_reason,
                route_reason="explicit_model",
                raw_rewrite=raw_rewrite
            )
        
        if rewrite_type == "hybrid":
            return self._rewrite_by_hybird(
                query=original_query,
                query_type=query_type,
                confidence=confidence
            )

        print(f"[WARN] Invalid rewrite type: {rewrite_type} , fallback to none. ")
        return RewriteDecision(
            original_query=original_query,
            final_query=original_query,
            rewrite_type_requested=rewrite_type,
            rewrite_type_used="none",
            query_type=query_type,
            changed=False,
            is_valid=True,
            validator_reason="invalid_rewrite_type_fallback",
            route_reason="fallback_none",
            raw_rewrite=""
        )

    def _rewrite_by_rules(self, query):

        q = self._normalize_query(query)

        replacements = {
            r"\bHF embeddings\b": "HuggingFace embeddings",
            r"\bHF\b": "HuggingFace",
            r"\bvs\.\b": "vs",
            r"\bRAG\b": "RetrievalQA RAG",
            r"\bopengauss\b": "openGauss",
            r"\brk3568\b": "RK3568",
        }
        for pattern, repl in replacements.items():
            query_rewrite = re.sub(pattern, repl, q, flags=re.IGNORECASE)

        query_rewrite = re.sub(r"\s+", " ", query_rewrite).strip()
        return query_rewrite

    def _rewrite_by_model(self, query):
        
        if self.rag_pipeline is None:
            print("[WARN] LLM Rewriter is not initialized for rewriting query, fallback to rules.")
            return self._rewrite_by_rules(query=query)

        prompt = f"""
        You are an expert in query optimization.

        Rewrite the user query into ONE searchable, clean, unambiguous and semantically complete search query. 
        Keep the original meaning unchanged.

        Rules:
        - Output only the rewritten query.
        - Do not change the original meaning.
        - Do not explain.
        - Do not answer the question.
        - Do not add background knowledge not implied by the original query.
        - If the original query is already clear, return it unchanged.

        Query: {query}

        Rewritten Query:
        """
        query_rewrite = self.rag_pipeline.generate_text(prompt=prompt).strip()

        return query_rewrite

    def _rewrite_by_hybird(self, query, query_type="unknown", confidence=None):
        """
        NOTO: 混合策略
        1. 纯净问题，直接检索，不做重写；
        2. 轻量标准问题，直接规则重写；
        3. 模糊/低置信度，模型重写；
        4. default: None
        TODO: fallback机制 
        """
        route_reason = "default_none"
        if self._is_clear_query(query=query, query_type=query_type):
            route_reason = "clear_query_no_rewrite"
            return RewriteDecision(
                original_query=query,
                final_query=query,
                rewrite_type_requested="none",
                rewrite_type_used="none",
                query_type=query_type,
                changed=False,
                is_valid=True,
                validator_reason="no_rewrite_baseline",
                route_reason=route_reason,
                raw_rewrite=""
            )

        if self._is_needs_light_normalization(query=query):
            route_reason = "light_normalization_rules"
            raw_rewrite = self._rewrite_by_rules(query=query)
            final_query, is_valid, validator_reason = self._validate_rewrite(
                original_query=query,
                rewritten_query=raw_rewrite
            )
            return RewriteDecision(
                original_query=query,
                final_query=final_query,
                rewrite_type_requested="hybrid",
                rewrite_type_used="rules" if is_valid else "none",
                query_type=query_type,
                changed=(final_query != query),
                is_valid=is_valid,
                validator_reason=validator_reason,
                route_reason=route_reason,
                raw_rewrite=raw_rewrite
            )

        if self._is_ambiguous_query(query=query) or self._is_low_confidence(confidence=confidence):
            route_reason = "ambiguous_or_low_confidence_model"
            raw_rewrite = self._rewrite_by_model(query=query)
            final_query, is_valid, validator_reason = self._validate_rewrite(
                original_query=query,
                rewritten_query=raw_rewrite
            )
            return RewriteDecision(
                original_query=query,
                final_query=final_query,
                rewrite_type_requested="hybrid",
                rewrite_type_used="model" if is_valid else "none",
                query_type=query_type,
                changed=(final_query != query),
                is_valid=is_valid,
                validator_reason=validator_reason,
                route_reason=route_reason,
                raw_rewrite=raw_rewrite
            )
        
        return RewriteDecision(
            original_query=query,
            final_query=query,
            rewrite_type_requested="hybrid",
            rewrite_type_used="none",
            query_type=query_type,
            changed=False,
            is_valid=True,
            validator_reason="default_no_rewrite",
            route_reason=route_reason,
            raw_rewrite=""
        )

    def _classify_by_rules(self, query):
        q = query.lower().strip()

        if any(x in q for x in ["what is", "what role", "what does", "why is", "why should"]):
            self.query_type = "definition"
        elif any(x in q for x in ["difference", "differences", "compare", "compared", "versus", "vs"]):
            self.query_type = "comparison"
        elif any(x in q for x in ["what are the", "list", "main forms", "fields", "deliverables"]):
            self.query_type = "list_or_enumeration"
        elif any(x in q for x in ["recommended", "recommend", "deployment", "should be completed", "solution for"]):
            self.query_type = "deployment_or_recommendation"
        else:
            self.query_type = "unknown"

        return self.query_type        

    def _classify_by_model(self, query):
        if self.rag_pipeline is None:
            self.actual_classify_type = "rules"
            print("[WARN] LLM Classifier is not initialized for classifying query type, fallback to rules.")
            return self._classify_by_rules(query=query)

        prompt = f"""
        You are a query intent classifier.

        Classify the user query into exactly one label from this set:
        definition
        comparison
        list_or_enumeration
        deployment_or_recommendation
        unknown

        Rules:
        - Return only one label.
        - Do not explain.
        - Do not output any extra words.
        - If uncertain, return unknown.

        Query: {query}
        """
        self.query_type = self.rag_pipeline.generate_text(prompt=prompt).strip().lower()
        if self.query_type not in self.VALID_TYPES:
            print("[WARN] Invalid query type returned by LLM Classifier, fallback to rules.")
            self.actual_classify_type = "rules"
            self.query_type_raw = self.query_type
            return self._classify_by_rules(query=query)
        return self.query_type

    def _validate_rewrite(self, original_query, rewritten_query):  # 7. query 更像解释句而不是问句，方式：检验 .和\n 数量 ??????????????????????
        """
        NOTE: 重写Guard机制
        1. 为空 - 不合法
        2. 含非法前缀 - 不合法
        3. 较原始过长 - 不合法
        4. 几乎没变 - 合法
        5. 关键词重叠度过低 - 不合法
        6. 较原始过短 - 不合法
        7. query 更像解释句而不是问句，方式：检验 .和\n 数量 

        TODO: 【优化】检查改写结果是不是变成了一段可解释文本，而不是一个检索 query
        1) 检查是否有解释性 marker
        2) 是否有多行输出 \n
        3) 是否有多句子输出, 标点: . ? !
        """
        original = self._normalize_query(original_query)
        rewritten = self._normalize_query(rewritten_query)

        if not rewritten:
            return original, False, "empty_rewrite"

        rewritten_lowered = rewritten.lower()
        for bad_prefix in self.INVALID_REWRITE_PREFIXES:
            if rewritten_lowered.startswith(bad_prefix):
                return original, False, "contains_explanatory_prefix"

        original_tokens = self._tokenize(text=original)
        rewritten_tokens = self._tokenize(text=rewritten)
        if len(rewritten_tokens) > max(12, int(len(original_tokens) * 2.2)):
            return original, False, "rewrite_too_long"

        if original.lower() == rewritten.lower():
            return original, True, "no_rewrite"

        original_keywords = self._extract_keywords(text=original)
        rewritten_keywords = self._extract_keywords(text=rewritten)
        if original_keywords:
            overlap_rate = len(original_keywords & rewritten_keywords) / len(original_keywords)
            if overlap_rate < 0.5:
                return original, False, "keyword_overlap_too_low"

        if len(rewritten_tokens) < max(3, int(len(original_tokens) * 0.5)):
            return original, False, "rewrite_too_short"

        if rewritten.count(".") > 1 or rewritten.count("\n") > 0:
            return original, False, "not_single_search_query"

        return rewritten, True, "accepted"    
    # -------------------------------
    # Helper Functions
    # -------------------------------
    def _tokenize(self, text):
        return re.findall(r"[A-Za-z0-9_\-]+", text.lower())

    def _normalize_query(self, query):
        q = (query or "").strip()
        q = re.sub(r"\s+", " ", q)
        return q

    def _contains_pronoun_reference(self, query):
        tokens = set(self._tokenize(text=query))
        return len(tokens & set(self.PRONOUN_HINTS)) > 0

    def _is_clear_query(self, query, query_type):
        # NOTE: 纯净问题的判准
        # 1. 包含的单词数不少于7； 2. 属于前三个基础类型；3. 不包含代词
        tokens = self._tokenize(text=query)

        if len(tokens) >= 7 and query_type in {"definition", "comparison", "list_or_enumeration"}:
            if not self._contains_pronoun_reference(query=query):
                return True
        return False

    def _is_needs_light_normalization(self, query):  
        """
        NOTE: 判断是否需要术语归一化
        """
        q = query.lower()

        pattern = [
            "hf",
            "hf embeddings",
            "vs.",
            "opengauss",
            "rk3568"
        ]
        return any(p in q for p in pattern)

    def _is_ambiguous_query(self, query):
        tokens = self._tokenize(text=query)
        if len(tokens) <= 5:
            return True
        if self._contains_pronoun_reference(query=query):
            return True
        return False

    def _is_low_confidence(self, confidence):
        if confidence is None:
            return False
        try:
            return float(confidence) < 0.35
        except Exception:
            return False

    def _extract_keywords(self, text):
        stopwords = {
            "what", "is", "the", "a", "an", "of", "for", "to", "and", "or", 
            "in", "on", "with", "does", "do", "why", "how", "are", "be", 
            "should", "it", "this", "that"
        }
        tokens = self._tokenize(text=text)
        return {t for t in tokens if t not in stopwords and len(t) > 1}


