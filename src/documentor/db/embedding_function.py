import numpy as np
from chromadb import (
    Documents,
    Embeddings,
    EmbeddingFunction
)
from typing import Any, List
from numpy.linalg import norm
from sentence_transformers import SentenceTransformer


class CustomEmbeddingFunction(EmbeddingFunction[Documents]):

    @staticmethod
    def cosine_similarity(a: np.ndarray, b: np.ndarray) -> np.ndarray:
        """ Basically finds the angle between two vectors.
        
        * Value Range: `[-1, 1]`

        * Mathematical Formula:

            a.b = |a||b|cos(theta)
            => theta = cos^-1(a.b / |a||b|)

        """
        return (a @ b.T) / (norm(a) * norm(b))

    def __init__(self, 
        model_name: str = 'jinaai/jina-embeddings-v2-base-en',
        device: str | None = 'cuda',
        trust_remote_code: bool = True
    ) -> None:
        
        self.model = SentenceTransformer(
            model_name,
            device=device,
            trust_remote_code=trust_remote_code
        )

    def __call__(self, input: Documents) -> List[Embeddings]:
        # Convert the numpy array to Python List
        return self.model.encode(input).tolist()
    
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        return [self.model.encode(t).tolist() for t in texts]
            
    def embed_query(self, query: str) -> List[float]:
        return self.model.encode([query]).tolist()
    
    def encode(self, text) -> Any:
        return self.model.encode(text)
