from langgraph.graph import START,StateGraph, END

from app.graph.state import AgentState

from app.agents.planner import planner_agent
from app.agents.router import router_agent
from app.agents.summary_agent import summary_agent

workflow = StateGraph(AgentState)

workflow.add_node("planner", planner_agent)
workflow.add_node("router", router_agent)
workflow.add_node("summary", summary_agent)

workflow.add_edge(START,"planner")

workflow.add_edge("planner", "router")
workflow.add_edge("router", "summary")

workflow.add_edge("summary", END)

graph = workflow.compile()