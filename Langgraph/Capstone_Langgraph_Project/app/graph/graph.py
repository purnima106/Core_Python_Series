from langgraph.graph import StateGraph, START, END
from app.graph.nodes import orchestrator
from app.graph.state import ResearchState

graph = StateGraph(ResearchState)

graph.add_node("orchestrator", orchestrator)

graph.set_entry_point("orchestrator")
graph.add_edge(START, "orchestrator")
graph.add_edge("orchestrator", END)

app_graph = graph.compile()