from app.services.llm import get_llm

llm = get_llm()

def planner_agent(state):

    query = state["query"]

    chat_history = state.get("chat_history", [])

    prompt = f"""
    你是 AI 研究规划助手。

    历史对话：
    {chat_history}

    当前用户问题：
    {query}

    请结合历史对话，拆解当前研究任务。
    如果当前问题中出现“它”“这个”“上面内容”等指代词，请根据历史对话判断指代对象。
    """


    response = llm.invoke(prompt)

    return {
        "plan": response.content
    }