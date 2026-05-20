from langchain_community.embeddings import DashScopeEmbeddings
from dotenv import load_dotenv

load_dotenv()

def get_embedding():

    return DashScopeEmbeddings(model="text-embedding-v4")