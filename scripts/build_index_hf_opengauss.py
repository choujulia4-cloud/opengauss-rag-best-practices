from app.text_chunker import TextChunker
from app.hf_embedder import HFEmbedder
from app.op_controller import OPController
import time

# 使用huggingface的模型进行文本嵌入, 将生成的嵌入向量保存至Opengauss
if __name__ == "__main__":
    # text_chunker = TextChunker(max_chunk_size=200, overlap=100, cutting_type='mark', dataset_path="./data/kb_chunks_datasets_mark_200_100")
    # text_chunker.split_text_into_dataset()
    # dataset_path = "./data/kb_chunks_datasets_mark_200_100"
    # hf_embedder = HFEmbedder(db_dataset_path=dataset_path)
    # hf_embedder.generate_embeddings_to_save()

    # op_controller = OPController(ds_with_embeddings_path=hf_embedder.ds_with_embeddings_path)

    # --- 直接给 path
    # op_controller1 = OPController(ds_with_embeddings_path="./data/hf_embeddings_dataset_mark_200_100")
    # op_controller1.insert_embeddings_to_opengauss()
    op_controller2 = OPController(ds_with_embeddings_path="./data/hf_embeddings_dataset_mark_200_50")
    op_controller2.insert_embeddings_to_opengauss()
    # time.sleep(3)
    # op_controller3 = OPController(ds_with_embeddings_path="./data/hf_embeddings_dataset_mark_200_10")
    # op_controller3.insert_embeddings_to_opengauss()
    # op_controller4 = OPController(ds_with_embeddings_path="./data/hf_embeddings_dataset_mark_200_0")
    # op_controller4.insert_embeddings_to_opengauss()
