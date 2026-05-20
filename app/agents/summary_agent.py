from app.services.llm import get_llm

llm = get_llm()


def summary_agent(state):
    
    query = state["query"]
    
    chat_history = state.get("chat_history", [])
    
    plan = state["plan"]
    
    tool_result = state["tool_result"]

    prompt = f"""
    你是 AI 研究助手，负责输出最终回答。

    历史对话：
    {chat_history}

    用户当前问题：
    {query}

    研究计划：
    {plan}

    工具执行结果：
    {tool_result}

    请结合历史对话和工具结果，回答用户当前问题。
    如果用户的问题是追问，例如“它有什么风险”“继续分析”，请根据历史对话判断用户指代的内容。
    """

    response = llm.invoke(prompt)

    return {
        "final_answer": response.content
    }