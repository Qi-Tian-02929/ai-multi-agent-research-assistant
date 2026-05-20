import json
from app.services import redis_client
from app.services.redis_client import get_redis_client

redis_client = get_redis_client()

def get_memory_key(session_id: str) -> str:
    
    return f"chat:memory:{session_id}"


def load_chat_history(session_id: str, limit: int = 6) -> list:
   
    key = get_memory_key(session_id)

    messages = redis_client.lrange(key, -limit, -1)

    return [
        json.loads(message)
        for message in messages
    ]


def save_chat_message(session_id: str, role: str, content: str):
    
    key = get_memory_key(session_id)

    message = {
        "role": role,
        "content": content
    }

    redis_client.rpush(
        key,
        json.dumps(message, ensure_ascii=False)
    )

    redis_client.expire(key, 60 * 60 * 24)