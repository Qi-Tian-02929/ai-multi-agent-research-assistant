from langchain_core.messages import HumanMessage, ToolMessage, SystemMessage

from app.services.llm import get_llm
from app.tools import tools

llm = get_llm()

llm_with_tools = llm.bind_tools(tools)


def format_history(chat_history):
    text = ""

    for item in chat_history:
        role = item.get("role", "")
        content = item.get("content", "")
        text += f"{role}: {content}\n"

    return text


def router_agent(state):
    query = state["query"]
    chat_history = state.get("chat_history", [])
    plan = state.get("plan", "")

    history_text = format_history(chat_history)

    messages = [
        SystemMessage(
    content=f"""
    你是一个多工具 AI 研究助手。

    你可以根据任务选择工具：
    1. calculator:用于数学计算
    2. web_search:用于搜索互联网最新信息
    3. rag_search:用于检索本地 PDF / 文档知识库

    重要规则：
    - 只要用户提到 PDF、文档、资料、报告、论文、财报、上传文件、本地知识库,必须调用 rag_search。
    - 如果用户说“这份 PDF”“这个文档”“刚上传的文件”,也必须调用 rag_search。
    - 不要直接说不知道，请先尝试检索本地知识库。

    历史对话：
    {history_text}

    当前研究计划：
    {plan}

    如果用户问题依赖历史上下文，请先理解指代关系，再选择工具。
    """
    ),
        HumanMessage(content=query)
    ]

    final_result = []

    for _ in range(5):
        response = llm_with_tools.invoke(messages)

        messages.append(response)

        if not response.tool_calls:
            final_result.append(response.content)
            break

        for tool_call in response.tool_calls:
            tool_name = tool_call["name"]
            tool_args = tool_call["args"]

            selected_tool = next(
                tool for tool in tools
                if tool.name == tool_name
            )

            tool_output = selected_tool.invoke(tool_args)

            final_result.append(
                f"{tool_name}: {tool_output}"
            )

            messages.append(
                ToolMessage(
                    content=str(tool_output),
                    tool_call_id=tool_call["id"]
                )
            )

    return {
        "tool_result": "\n".join(final_result)
    }