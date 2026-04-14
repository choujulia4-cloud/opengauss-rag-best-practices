from app.op_controller import OPController
import time

# 测试得到的检索结果
if __name__ == "__main__":
    # query = "What role does OpenGauss play in a RetrievalQA pipeline?"

    op_controller1 = OPController(ds_with_embeddings_path="./data/hf_embeddings_dataset_mark_200_100")
    op_controller2 = OPController(ds_with_embeddings_path="./data/hf_embeddings_dataset_mark_200_50")
    op_controller3 = OPController(ds_with_embeddings_path="./data/hf_embeddings_dataset_mark_200_10")
    op_controller4 = OPController(ds_with_embeddings_path="./data/hf_embeddings_dataset_mark_200_0")
    conn = None
    
    # with op_controller.connect_to_opengauss() as conn:
    #     while True:
    #         query = input(">>> ").strip()
    #         if query.lower() == "exit":
    #             print("-------- Exiting retrieval loop --------")
    #             break
    #         op_controller.opengauss_retrieve_text(conn=conn, query=query, top_k=5)

    query = [
        "What are the deployment advantages and disadvantages of using HuggingFace local embeddings versus Cohere hosted embeddings?",
        "Why does the project recommend performing large-scale document chunking, bulk embedding generation, and batch insertion on a stronger machine rather than on the RK3568 edge device?",
        "According to the text, what are the four main forms of deliverables that the final project output should include?",
        "Why does the text suggest including both chunk size and overlap size in the metadata fields of the embedding table?",
        "In this project, why does BentoML serve as the application service layer rather than as an embedding model itself?",
        "What benefits does using OpenGauss provide by storing both the original text content and the embedding vectors in a RetrievalQA pipeline?"
    ]
    with op_controller1.connect_to_opengauss() as conn:
        for q in query:
            op_controller1.opengauss_retrieve_text(conn=conn, query=q, top_k=5, operator='<#>')
    time.sleep(3)
    with op_controller2.connect_to_opengauss() as conn:
        for q in query:
            op_controller2.opengauss_retrieve_text(conn=conn, query=q, top_k=5, operator='<#>')  
    time.sleep(3)
    with op_controller3.connect_to_opengauss() as conn:
        for q in query:
            op_controller3.opengauss_retrieve_text(conn=conn, query=q, top_k=5, operator='<#>')
    time.sleep(3)
    with op_controller4.connect_to_opengauss() as conn:
        for q in query:
            op_controller4.opengauss_retrieve_text(conn=conn, query=q, top_k=5, operator='<#>')
