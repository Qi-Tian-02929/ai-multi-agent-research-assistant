from langchain.chat_models import init_chat_model
from dotenv import load_dotenv

load_dotenv()

def get_llm():

    return init_chat_model(
        model="deepseek-chat",
        temperature=0,
        streaming=True
    )