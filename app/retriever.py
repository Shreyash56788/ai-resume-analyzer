import faiss
import numpy as np
import pickle


def create_faiss_index(embedding_matrix):

    dimension = embedding_matrix.shape[1]

    faiss.normalize_L2(embedding_matrix)

    index = faiss.IndexFlatIP(dimension)

    index.add(embedding_matrix)

    return index


def search_index(index, query_embedding, k=2):

    query_embedding = np.array(
        [query_embedding],
        dtype="float32"
    )

    faiss.normalize_L2(query_embedding)

    scores, indices = index.search(
        query_embedding,
        k
    )

    return scores, indices


def save_faiss_index(index, file_path):

    faiss.write_index(
        index,
        file_path
    )


def load_faiss_index(file_path):

    return faiss.read_index(
        file_path
    )


def save_chunks(chunks, file_path):

    with open(
        file_path,
        "wb"
    ) as file:

        pickle.dump(
            chunks,
            file
        )


def load_chunks(file_path):

    with open(
        file_path,
        "rb"
    ) as file:

        return pickle.load(file)