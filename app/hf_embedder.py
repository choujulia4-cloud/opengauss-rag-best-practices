import torch
import numpy as np
from transformers import (
    DPRContextEncoder,
    DPRContextEncoderTokenizer
)
from datasets import load_from_disk

# load Dataset: text_dataset = load_from_disk(path)
class HFEmbedder:
    def __init__(self, db_dataset_path, max_length=512):
        self.db_dataset = load_from_disk(db_dataset_path)
        self.max_length = max_length
        self.ds_with_embeddings_path = db_dataset_path.replace("kb_chunks_datasets", "hf_embeddings_dataset") 

    def generate_embeddings_to_save(self):
        ctx_encoder = DPRContextEncoder.from_pretrained("facebook/dpr-ctx_encoder-single-nq-base")
        ctx_tokenizer = DPRContextEncoderTokenizer.from_pretrained("facebook/dpr-ctx_encoder-single-nq-base")
        print("===== Loaded existing embedder encoder and tokenizer successfully =====")

        def generate_embeddings(dataset):
            inputs = ctx_tokenizer(
                dataset["text"],
                max_length=self.max_length,
                truncation=True,
                padding="max_length",
                return_tensors="pt"
            )

            with torch.no_grad():
                embeddings = ctx_encoder(**inputs).pooler_output.numpy()
            return {'embeddings': [e for e in embeddings]}

        torch.set_grad_enabled(False)
        ds_with_embeddings = self.db_dataset.map(
            generate_embeddings,
            batched=True,
            batch_size=0
        )
        print(f"-- Generated embeddings dimentions: {np.array(ds_with_embeddings['embeddings']).shape} successfully --")

        ds_with_embeddings.save_to_disk(self.ds_with_embeddings_path)
        print(f"-- dataset with embeddings saved to {self.ds_with_embeddings_path} sucessfully.")


