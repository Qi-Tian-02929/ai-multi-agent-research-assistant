from langchain.tools import tool

@tool
def calculator(expression: str) -> str:
    """
    用于执行数学计算。
    """

    try:
        result = eval(expression)

        return str(result)

    except Exception as e:
        return f"计算错误: {str(e)}"