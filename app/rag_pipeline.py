from app.text_chunker import TextChunker
from app.hf_embedder import HFEmbedder
from app.op_controller import OPController

class RagPipeline:
    def __init__(self, chunk_config = None, retrieval_top_k = 5, retrieval_operator = "<=>", generation_model_name = "google/flan-t5-base"):
        self.chunk_config = chunk_config or {
            "max_chunk_size": 200,
            "overlap": 10,
            "cutting_type": 'mark',
            "dataset_path_title": "./data/kb_chunks_datasets"
        }
        self.retrieval_top_k = retrieval_top_k
        self.retrieval_operator = retrieval_operator
        self.generation_model_name = generation_model_name

        self.chunker = TextChunker(
            max_chunk_size=self.chunk_config["max_chunk_size"], 
            overlap=self.chunk_config["overlap"], 
            cutting_type=self.chunk_config["cutting_type"], 
            dataset_path_title=self.chunk_config["dataset_path_title"])
        self.embedder = HFEmbedder(db_dataset_path=self.chunker.dataset_path, max_length=512)
        self.vector_store = OPController(ds_with_embeddings_path=self.embedder.ds_with_embeddings_path)
        self.generator_tokenizer = None
        self.generator_model = None

    def build_chunks_dataset(self):
        # 原始文本分块，构成dataset
        self.chunker.split_text_into_dataset()

    def build_embeddings_dataset(self):
        # 基于chunk dataset , 生成文本的embedding
        self.embedder.generate_embeddings_to_save()

    def insert_embeddings(self):
        # 将 embedding dataset 写入 opengauss
        self.vector_store.insert_embeddings_to_opengauss()

    def build_knowledge_base(self):
        # 一键构建知识库：切块 - 生成向量 - 写入数据库
        self.build_chunks_dataset()
        self.build_embeddings_dataset()
        self.insert_embeddings()

    def retrieve(self, query, top_k = None, operator = None):
        # 根据 query， 从 opengauss 检索相关文本
        top_k = top_k if top_k is not None else self.retrieval_top_k
        operator = operator if operator is not None  else self.retrieval_operator

        conn = self.vector_store.connect_to_opengauss()
        if not conn:
            return RuntimeError("Failed to connect to OpenGauss for retrieval.")
        try:
            retrieved_results = self.vector_store.opengauss_retrieve_text(conn=conn, query=query, top_k=top_k, operator=operator)
            return retrieved_results
        finally:
            conn.close()
    
    def build_context(self, retrieved_results):
        # 将检索结果拼成生成模型输入上下文
        context_list = []
        for item in retrieved_results:
            text = item[0].strip()
            if text:
                context_list.append(text)
        return "\n".join(context_list)
    
    def load_generator(self):
        # 加载生成模型
        from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, AutoModelForCausalLM
        import os
        gen_dir = "/home/zl/文档/models/Phi-3.5-mini-instruct"
        print(f"Generator model: {os.path.basename(gen_dir)}")
        if self.generator_tokenizer is None or self.generator_model is None:
            # self.generator_tokenizer = AutoTokenizer.from_pretrained(self.generation_model_name)
            # self.generator_model = AutoModelForSeq2SeqLM.from_pretrained(self.generation_model_name)

            # gen_dir = "/home/robot/Documents/models/flan_t5_base"
            # self.generator_tokenizer = AutoTokenizer.from_pretrained(gen_dir, local_files_only=True)
            # self.generator_model = AutoModelForSeq2SeqLM.from_pretrained(gen_dir, local_files_only=True)

            
            self.generator_tokenizer = AutoTokenizer.from_pretrained(gen_dir, local_files_only=True)
            self.generator_model = AutoModelForCausalLM.from_pretrained(gen_dir, local_files_only=True)
            
    def generate_answer(self, query, context, max_new_tokens):
        # 生成答案
        self.load_generator()
        # prompt = (
        #     "Answer the question based only on the given context.\n\n"
        #     f"Context:\n{context}\n\n"
        #     f"Question:\n{query}\n\n"
        #     "Answer:"
        #     )
        # prompt = (
        #     "Answer the question based only on the given context."
        #     "Give a complete and specific answer."
        #     "Do not omit important details that are details that are directly supported by the context.\n\n"
        #     f"Context:\n{context}\n\n"
        #     f"Question:\n{query}\n\n"
        #     "Answer:"
        # )
        # prompt = (
        #     "Answer the question based only on the given context."
        #     "If the context does not contain enough information, say that the answer is not available in the context."
        #     "Do not use outside knowledge.\n\n"
        #     f"Context:\n{context}\n\n"
        #     f"Question:\n{query}\n\n"
        #     "Answer:"
        # )
     

        # inputs = self.generator_tokenizer(
        #     prompt,
        #     return_tensors="pt",
        #     truncation=True,
        #     max_length=1024,
        # )
        # outputs = self.generator_model.generate(
        #     **inputs,
        #     max_new_tokens=max_new_tokens
        # )
        # answer = self.generator_tokenizer.decode(outputs[0], skip_special_tokens=True)
        # return answer.strip()

        messages = [
            {"role": "user", "content": (
                "Answer the question based only on the given context."
                "If the context does not contain enough information, say no.\n\n"
                f"Context:\n{context}\n\n"
                f"Question:\n{query}\n\n"
                "Answer:"
            )},
        ]
        inputs = self.generator_tokenizer.apply_chat_template(
            messages,
            add_generation_prompt=True,
            tokenize=True,
            return_dict=True,
            return_tensors="pt",
        )

        outputs = self.generator_model.generate(**inputs, max_new_tokens=40)
        return self.generator_tokenizer.decode(outputs[0][inputs["input_ids"].shape[-1]:]).strip()
    
    def ask(self, query, top_k = None, operator = None, return_retrieval = True):
        retrieved_results = self.retrieve(query=query, top_k=top_k, operator=operator)
        context = self.build_context(retrieved_results=retrieved_results)
        answer = self.generate_answer(query=query, context=context)

        result = {
            "query": query,
            "answer": answer,
            "context": context
        }

        if return_retrieval:
            result["retrieved_results"] = retrieved_results

        return result
        
