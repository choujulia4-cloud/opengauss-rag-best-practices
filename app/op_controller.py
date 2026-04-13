import os
import numpy as np
import torch

class OPController: 
    def __init__(self, ds_with_embeddings_path="./data/hf_embeddings_dataset"):
        self.ds_with_embeddings_path = ds_with_embeddings_path
        self.query_tokenizer = None
        self.query_encoder = None

    def connect_to_opengauss(self):
        import psycopg2
        from psycopg2 import OperationalError
        # db_host = os.getenv("DB_HOST", "opengauss_pcTocont_container") ##########################################################
        db_host = os.getenv("DB_HOST", "localhost")
        db_port = os.getenv("DB_PORT", "5432")
        db_name = os.getenv("DB_NAME", "ragdb")
        db_user = os.getenv("DB_USER", "rag_user")
        db_pass = os.getenv("DB_PASS", "rag_pass0")

        try:
            conn = psycopg2.connect(
                host=db_host,
                port=db_port,
                dbname=db_name,
                user=db_user,
                password=db_pass
            )
            print("-- Connection to OpenGauss established sucessfully --")
            return conn
        except OperationalError as e:
            print(f"[ERROR] Failed to connect to OpenGauss: {e}")
            return None

    def insert_embeddings_to_opengauss(self):
        from datasets import load_from_disk
        from psycopg2 import extras

        if not os.path.exists(self.ds_with_embeddings_path):
            print(f"[ERROR] Embeddings dataset not found at {self.ds_with_embeddings_path}")
            return
        
        ds_with_embeddings = load_from_disk(self.ds_with_embeddings_path)
        embeddings = np.array(ds_with_embeddings["embeddings"])
        texts = ds_with_embeddings["text"]
        conn = self.connect_to_opengauss()
        if not conn:
            return
        insert_data = [
            (text, embedding.tolist())
            for text, embedding in zip(texts, embeddings)
        ]
        cursor = conn.cursor()
        table_name = self.ds_with_embeddings_path.replace("./data/hf_embeddings_dataset_mark", "embeddings")
        insert_sql = f"INSERT INTO {table_name} (text_content, text_embedding) VALUES (%s, %s)"
        extras.execute_batch(cursor, insert_sql, insert_data)
        conn.commit()
        cursor.close()
        conn.close()
        print(f"-- Embeddings inserted into OpenGauss table {table_name} successfully --")

    def opengauss_retrieve_text(self, conn, query, top_k=5, operator='<=>'):
        from transformers import (
            DPRQuestionEncoderTokenizer,
            DPRQuestionEncoder
        )
        import time
        def generate_query_embedding(query):
            if self.query_tokenizer is None or self.query_encoder is None:
                self.query_tokenizer = DPRQuestionEncoderTokenizer.from_pretrained("facebook/dpr-question_encoder-single-nq-base")
                self.query_encoder = DPRQuestionEncoder.from_pretrained("facebook/dpr-question_encoder-single-nq-base")
                self.query_encoder.eval()
            inputs = self.query_tokenizer(
                query,
                max_length=512,
                truncation=True,
                padding="max_length",
                return_tensors="pt"
            )
            with torch.no_grad():
                query_embedding = self.query_encoder(**inputs).pooler_output

            # del self.query_encoder
            return query_embedding
        
        start_time = time.time()
        query_embedding = generate_query_embedding(query=query)
        query_embedding = query_embedding.squeeze()
        print(f"-- Generate query embedding with shape: {query_embedding.shape} --")
        sorting_direction = "ASC"
        table_name = self.ds_with_embeddings_path.replace("./data/hf_embeddings_dataset_mark", "embeddings")
        retrieve_sql = f"""
        SELECT text_content, (text_embedding {operator} %s::vector) as distance
        FROM {table_name}
        ORDER BY distance {sorting_direction}
        LIMIT %s;
        """
        cursor = conn.cursor()
        cursor.execute(retrieve_sql, (query_embedding.tolist(), top_k))
        retrieved_result = cursor.fetchall()
        end_time = time.time()
        retrieval_time = end_time - start_time

        filename = os.path.basename(self.ds_with_embeddings_path)
        parts = filename.split("_")
        config_name = "_".join(parts[-3:])

        print("================= Retrival Logs =================")
        print(f"Config: {config_name}")
        print(f"Query: {query}")
        print(f"Operator: {operator}")
        print(f"Retrieval Time: {retrieval_time:.4f} seconds")

        for i, (text, dist) in enumerate(retrieved_result):
            print(f"== Rand {i+1}: Distance/Score = {dist} | Text = {text} ")

        
        
        cursor.close()
        return retrieved_result


if __name__ == "__main__":
    pass
