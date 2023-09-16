from sentence_transformers import SentenceTransformer
import torch

class Embeddings:

    def __init__(self, model: str ='thenlper/gte-small') -> None:
        self.device = "cuda:0" if torch.cuda.is_available() else "cpu"
        self.device = 'cpu' # for gte-small (fails with cuda)
        print(self.device)
        self.model = SentenceTransformer(model, device=self.device)

    def get_sentence_embedding(self, s: str):
        return self.model.encode(s)
    
