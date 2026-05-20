from app.rag.vectorstore import load_vectorstore


def search_documents(query: str, k: int = 4) -> str:
    vectorstore = load_vectorstore()

    docs = vectorstore.similarity_search(
        query=query,
        k=k
    )

    if not docs:
        return "没有检索到相关文档。"

    results = []

    for i, doc in enumerate(docs, start=1):
        source = doc.metadata.get("source", "未知来源")
        page = doc.metadata.get("page", "未知页码")

        results.append(
            f"""
文档片段 {i}
来源: {source}
页码: {page}

内容:
{doc.page_content}
"""
        )

    return "\n\n".join(results)