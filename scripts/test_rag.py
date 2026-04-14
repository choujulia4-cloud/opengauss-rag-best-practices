from app.rag_pipeline import RagPipeline
import time
import os

if __name__ == "__main__":
    pipeline = RagPipeline(
        chunk_config={
            "max_chunk_size": 200,
            "overlap": 50,
            "cutting_type": 'mark',
            "dataset_path_title": "./data/kb_chunks_datasets"
        },
        retrieval_top_k=1,
        retrieval_operator="<#>",
        generation_model_name="google/flan-t5-base"
    )
    # query_list = [
    #     "What role does OpenGauss play in a RetrievalQA pipeline?",
    #     "Why must long source documents be divided into smaller chunks?",
    #     "What are the two embedding sources mentioned in this project?",
    #     "What does BentoML do in this project?",
    #     "Why is RK3568 considered a resource-constrained edge device?",
    #     "What tasks should be completed on a stronger machine instead of the edge device?",
    #     "What are the main differences between HuggingFace embeddings and Cohere embeddings?",
    #     "Why should retrieval evaluation be separated from generation evaluation?",
    #     "What dimensions should be tested systematically for best-practice exploration?",
    #     "What is the recommended minimal solution for RK3568 according to the text?",
    #     "What metadata fields are recommended for the OpenGauss embedding table?",
    #     "Why should similarity operator selection be included in best-practice exploration?",
    #     "What are the deployment advantages and disadvantages of using HuggingFace local embeddings versus Cohere hosted embeddings?",
    #     "Why does the project recommend performing large-scale document chunking, bulk embedding generation, and batch insertion on a stronger machine rather than on the RK3568 edge device?",
    #     "According to the text, what are the four main forms of deliverables that the final project output should include?",
    #     "Why does the text suggest including both chunk size and overlap size in the metadata fields of the embedding table?",
    #     "In this project, why does BentoML serve as the application service layer rather than as an embedding model itself?",
    #     "What benefits does using OpenGauss provide by storing both the original text content and the embedding vectors in a RetrievalQA pipeline?"
    # ]
    query_list = [
    "What role does OpenGauss play in a RetrievalQA pipeline?",
    "Why must long source documents be divided into smaller chunks?",
    "What are the two embedding sources mentioned in this project?",
    "What are the main differences between HuggingFace embeddings and Cohere embeddings?",
    "Why should retrieval evaluation be separated from generation evaluation?",
    "What dimensions should be tested systematically for best-practice exploration?",
    "What is the recommended minimal solution for RK3568 according to the text?",
    "What metadata fields are recommended for the OpenGauss embedding table?",
    "According to the text, what are the four main forms of deliverables that the final project output should include?"
    ]
    gold_context_list = [
        "OpenGauss is an enterprise-grade relational database that can also be used as a vector store for retrieval-augmented generation systems. In a RetrievalQA pipeline, the database is not only responsible for storing original text chunks, but also for storing the embedding vectors that represent the semantic meaning of those chunks. When a user submits a question, the system converts the question into an embedding vector and performs similarity search against the stored vectors. The most relevant chunks are then returned as retrieval context for answer generation. This architecture makes it possible to build a complete retrieval and question answering workflow on top of a database system instead of relying only on an in-memory vector engine.",
        
        "Source documents may come from manuals, technical reports, markdown files, project notes, or deployment guides. These documents are often too long to be embedded directly, so they must be divided into smaller chunks. Chunking strategy has a direct influence on retrieval quality. If chunks are too short, important context may be lost. If chunks are too long, retrieval may become noisy because a returned chunk can contain both relevant and irrelevant content.",
        
        "After chunking, the next stage is embedding generation. An embedding model converts each text chunk into a dense numerical vector. In this project, the embedding layer may come from HuggingFace local models or Cohere hosted models.",
        
        "In this project, the embedding layer may come from HuggingFace local models or Cohere hosted models. HuggingFace models are suitable when local execution and offline control are important. They can be integrated directly into Python code and deployed inside containers, which makes them useful for experiments on AArch64 platforms. However, model size, inference latency, and memory usage can become critical on resource-constrained devices. Cohere embeddings, in contrast, are generated by calling a remote API. This reduces local computation pressure and can simplify deployment on lightweight edge devices, but it requires network access and external service credentials. Therefore, choosing between HuggingFace and Cohere is not only a question of retrieval accuracy, but also a question of deployment constraints, response latency, operating cost, and system reliability.",
        
        "A practical RetrievalQA system should separate retrieval evaluation from generation evaluation. Retrieval evaluation asks whether the database returns the correct or at least useful chunks. Typical indicators include top-1 hit rate, top-3 hit rate, mean reciprocal rank, and average retrieval latency. Generation evaluation asks whether the final answer is correct, grounded, and sufficiently complete. A system may retrieve the correct chunk but still produce a weak answer if the generation model fails to use the context properly. Conversely, a strong language model may sometimes produce a plausible answer even when retrieval is poor, which can hide defects in the retrieval layer. Therefore, both stages should be evaluated independently.",
        
        "For best-practice exploration, the project should test several dimensions systematically. The first dimension is chunking strategy. Fixed-length chunking is simple and easy to reproduce, but sentence-based or punctuation-based chunking may better preserve semantic boundaries. The second dimension is embedding backend. HuggingFace local embeddings provide more deployment autonomy, while Cohere embeddings may provide higher convenience or better hosted performance. The third dimension is retrieval parameter tuning, including top-k value, distance metric, and whether embeddings are normalized. The fourth dimension is deployment behavior, including container startup time, memory occupancy, response latency, and service stability under repeated queries.",
        
        "On RK3568, the recommended minimal solution may be to deploy OpenGauss and a lightweight service endpoint locally, while performing large-scale embedding generation on a separate machine. Such conclusions are more valuable than raw benchmark tables because they can guide future engineering decisions. The RK3568 platform is a typical resource-constrained edge device. Its CPU performance and memory capacity are sufficient for lightweight services, databases, and controlled experiments, but they are not ideal for large embedding models and heavy generation models running simultaneously. In such an environment, a common production-style deployment strategy is to push offline preprocessing to a stronger machine. Large-scale document chunking, bulk embedding generation, and batch insertion can be completed on a development workstation or server. The edge device then focuses on online query handling, vector retrieval, and lightweight response assembly.",
        
        "When storing embeddings in OpenGauss, the schema design should support both experimentation and later optimization. A practical table may include the original text content, the embedding vector, document identifier, chunk identifier, source file name, embedding model name, chunk size, overlap size, and creation time. Such metadata allows the engineer to compare different embedding models and chunking strategies without losing traceability.",
        
        "The final project output should include several forms of deliverables. The first is a markdown deployment guide that describes environment preparation, container startup, database initialization, model configuration, and service verification. The second is Python example code that demonstrates document chunking, embedding insertion, vector retrieval, and end-to-end question answering. The third is a best-practice report that summarizes experiments, explains trade-offs, and recommends configurations for both standard Linux servers and AArch64 edge devices. The fourth is a community contribution package, such as a pull request or technical write-up, that makes the results reproducible for other developers interested in OpenGauss-based retrieval systems."
    ]    
    i = 1
    for query in query_list:
        # retrieved_results = pipeline.retrieve(query=query)
        retrieved_results = gold_context_list[i-1]
        start_time = time.time()
        context = pipeline.build_context(retrieved_results)
        result = pipeline.generate_answer(query=query, context=context, max_new_tokens=200)
        end_time = time.time()
        filename = os.path.basename(pipeline.vector_store.ds_with_embeddings_path)
        parts = filename.split("_")
        config_name = "_".join(parts[-3:])
        print("================= Retrival Logs =================")
        print(f"Config: {config_name}")
        print(f"Query: {query}")
        print(f"Retrieved Results: {retrieved_results}")
        print(f"Generate_Time: {end_time - start_time} seconds")
        print(f"Answer [{i}]: {result}")
        i += 1
        print("============================================")

    # result = pipeline.ask(query=query)