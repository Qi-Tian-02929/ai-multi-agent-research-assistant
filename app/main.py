from app.graph.workflow import graph

query = input("请输入问题: ")

result = graph.invoke({
    "query": query
})

print("\n最终结果:\n")

print(result["final_answer"])