import os
import shutil

from fastapi import APIRouter, UploadFile, File
from pydantic import BaseModel

from app.graph.workflow import graph
from app.rag.loader import load_pdf
from app.rag.splitter import split_documents
from app.rag.vectorstore import create_vectorstore

from fastapi.responses import StreamingResponse
from app.services.memory import load_chat_history, save_chat_message


router = APIRouter()

UPLOAD_DIR = "app/data/docs"


class ChatRequest(BaseModel):
    query: str
    
    session_id: str = "default"


@router.post("/chat")
def chat(request: ChatRequest):
    chat_history = load_chat_history(request.session_id)

    result = graph.invoke({
        "query": request.query,
        "chat_history": chat_history
    })

    answer = result["final_answer"]

    save_chat_message(
        session_id=request.session_id,
        role="user",
        content=request.query
    )

    save_chat_message(
        session_id=request.session_id,
        role="assistant",
        content=answer
    )

    return {
        "answer": answer,
        "session_id": request.session_id
    }


@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        return {
            "error": "只支持上传 PDF 文件"
        }

    os.makedirs(UPLOAD_DIR, exist_ok=True)

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    documents = load_pdf(file_path)
    chunks = split_documents(documents)
    create_vectorstore(chunks)

    return {
        "message": "PDF 上传并入库完成",
        "file": file.filename,
        "chunks": len(chunks)
    }

@router.post("/chat/stream")
def chat_stream(request: ChatRequest):
    def generate():
        chat_history = load_chat_history(request.session_id)

        result = graph.invoke({
            "query": request.query,
            "chat_history": chat_history
        })

        final_answer = result["final_answer"]

        save_chat_message(
            session_id=request.session_id,
            role="user",
            content=request.query
        )

        save_chat_message(
            session_id=request.session_id,
            role="assistant",
            content=final_answer
        )

        for char in final_answer:
            yield char

    return StreamingResponse(
        generate(),
        media_type="text/plain"
    )