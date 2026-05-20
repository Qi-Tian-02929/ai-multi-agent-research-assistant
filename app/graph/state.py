from typing import TypedDict,List,Dict

class AgentState(TypedDict):

    query: str

    chat_history: List[Dict[str, str]]

    plan: str

    tool_result: str

    final_answer: str