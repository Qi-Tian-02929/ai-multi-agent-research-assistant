from langchain_chroma import Chroma
from app.services.embedding import get_embedding

PERSIST_DIR = "chroma_db"

COLLECTION_NAME = "research_docs"

embedding = get_embedding()

def create_vectorstore(documents):

    vectorstore = Chroma.from_documents(
        documents=documents,
        embedding=embedding,
        persist_directory=PERSIST_DIR,
        collection_name=COLLECTION_NAME
    )

    return vectorstore

def load_vectorstore():

    vectorstore = Chroma(
        persist_directory=PERSIST_DIR,
        embedding_function=embedding,
        collection_name=COLLECTION_NAME
    )

    return vectorstore