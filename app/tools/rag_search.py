from langchain.tools import tool
from app.rag.retriever import search_documents


@tool
def rag_search(query: str) -> str:
   
    """
    必须用于检索本地知识库、本地 PDF、上传文档、论文、报告、财报、资料。
    当用户提到“PDF”“文档”“资料”“这份文件”“刚上传的文件”“本地知识库”时,必须优先使用该工具。
    """

    return search_documents(query)