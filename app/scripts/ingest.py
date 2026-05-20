import os

from app.rag.loader import load_pdf
from app.rag.splitter import split_documents
from app.rag.vectorstore import create_vectorstore


DOCS_DIR = "app/data/docs"


def ingest_documents():
    all_chunks = []

    for filename in os.listdir(DOCS_DIR):
        if not filename.lower().endswith(".pdf"):
            continue

        file_path = os.path.join(DOCS_DIR, filename)

        print(f"正在加载: {file_path}")

        documents = load_pdf(file_path)

        chunks = split_documents(documents)

        all_chunks.extend(chunks)

    if not all_chunks:
        print("没有找到 PDF 文件。")
        return

    create_vectorstore(all_chunks)

    print(f"入库完成，共写入 {len(all_chunks)} 个文档片段。")


if __name__ == "__main__":
    ingest_documents()