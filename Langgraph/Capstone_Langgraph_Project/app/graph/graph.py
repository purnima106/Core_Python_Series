from langgraph.graph import StateGraph, END
from app.graph.state import ResearchState
from app.graph.nodes import orchestrator

graph = StateGraph(ResearchState)

graph.add_node("orchestrator", orchestrator)

graph.set_entry_point("orchestrator")
graph.add_edge("orchestrator", END)

app_graph = graph.compile()

# StateGraph → defines workflow
# add_node → adds logic
# entry_point → start
# END → stop