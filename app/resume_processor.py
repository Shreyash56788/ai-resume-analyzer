from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


def load_and_split_resume(file_path):

    loader = PyPDFLoader(file_path)
    documents = loader.load()

    print("Pages:", len(documents))

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=700,
        chunk_overlap=100
    )

    chunks = splitter.split_documents(documents)

    print("Pages:", len(documents))
    print("Chunks:", len(chunks))

    return chunks