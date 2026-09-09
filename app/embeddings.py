from sentence_transformers import SentenceTransformer
import numpy as np


EMBEDDING_MODEL = "all-MiniLM-L6-v2"

model = SentenceTransformer(
    EMBEDDING_MODEL
)


def create_embeddings(texts):

    embeddings = model.encode(
        texts,
        convert_to_numpy=True
    )

    return np.array(
        embeddings,
        dtype="float32"
    )