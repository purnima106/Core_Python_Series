# -----------------------------
# 🔹 IMPORTS
# -----------------------------

from langgraph.graph import StateGraph, END  
# StateGraph → used to define workflow graph
# END → marks termination

from typing import TypedDict  
# Defines structure of shared state

from langchain_openai import ChatOpenAI  
# LLM (used by supervisor + agents)


# -----------------------------
# 🔹 DEFINE STATE
# -----------------------------

class AgentState(TypedDict):
    input: str        # user query
    decision: str     # which agent to call next
    result: str       # output from agents
    final_answer: str # final response to user


# 👉 This state is shared across:
# supervisor + all agents


# -----------------------------
# 🔹 INITIALIZE LLM
# -----------------------------

llm = ChatOpenAI(model="gpt-4o-mini")


# -----------------------------
# 🔹 SUPERVISOR NODE (BRAIN)
# -----------------------------

def supervisor_node(state: AgentState) -> AgentState:
    """
    This node decides WHICH agent should handle the task.
    """
    
    user_input = state["input"]
    
    # LLM decides routing based on query type
    decision = llm.invoke(
        f"""
        You are a supervisor deciding which agent to use.

        Options:
        - research → for web search, latest info
        - analysis → for calculations, data reasoning
        - writing → for formatting, summarizing, drafting
        
        User query: {user_input}
        
        Return ONLY one word: research / analysis / writing
        """
    ).content.strip().lower()
    
    return {"decision": decision}


# -----------------------------
# 🔹 RESEARCH AGENT
# -----------------------------

def research_agent(state: AgentState) -> AgentState:
    """
    Handles web search / external info tasks.
    """
    
    query = state["input"]
    
    # Simulating search (you can plug Tavily here)
    result = llm.invoke(
        f"Find information about: {query}"
    ).content
    
    return {"result": result}


# -----------------------------
# 🔹 ANALYSIS AGENT
# -----------------------------

def analysis_agent(state: AgentState) -> AgentState:
    """
    Handles math, logic, calculations.
    """
    
    query = state["input"]
    
    result = llm.invoke(
        f"Solve this problem step-by-step: {query}"
    ).content
    
    return {"result": result}


# -----------------------------
# 🔹 WRITING AGENT
# -----------------------------

def writing_agent(state: AgentState) -> AgentState:
    """
    Handles formatting, summarizing, drafting.
    """
    
    query = state["input"]
    
    result = llm.invoke(
        f"Write a well-structured response for: {query}"
    ).content
    
    return {"result": result}


# -----------------------------
# 🔹 FINAL RESPONSE NODE
# -----------------------------

def final_node(state: AgentState) -> AgentState:
    """
    Prepares final answer for user.
    """
    
    return {"final_answer": state["result"]}


# -----------------------------
# 🔹 ROUTER (CONTROL FLOW)
# -----------------------------

def router(state: AgentState) -> str:
    """
    Routes to correct agent based on supervisor decision.
    """
    
    decision = state["decision"]
    
    if decision == "research":
        return "research_agent"
    
    elif decision == "analysis":
        return "analysis_agent"
    
    else:
        return "writing_agent"


# -----------------------------
# 🔹 BUILD GRAPH
# -----------------------------

graph = StateGraph(AgentState)

# Add all nodes
graph.add_node("supervisor", supervisor_node)
graph.add_node("research_agent", research_agent)
graph.add_node("analysis_agent", analysis_agent)
graph.add_node("writing_agent", writing_agent)
graph.add_node("final", final_node)


# -----------------------------
# 🔹 DEFINE FLOW
# -----------------------------

# Start from supervisor
graph.set_entry_point("supervisor")

# Conditional routing → supervisor decides next agent
graph.add_conditional_edges(
    "supervisor",  # decision happens here
    router,        # routing logic
    
    {
        "research_agent": "research_agent",
        "analysis_agent": "analysis_agent",
        "writing_agent": "writing_agent"
    }
)

# After any agent → go to final node
graph.add_edge("research_agent", "final")
graph.add_edge("analysis_agent", "final")
graph.add_edge("writing_agent", "final")

# End workflow
graph.add_edge("final", END)


# -----------------------------
# 🔹 COMPILE GRAPH
# -----------------------------

app = graph.compile()


# -----------------------------
# 🔹 RUN EXAMPLES
# -----------------------------

# Example 1 → research
result1 = app.invoke({
    "input": "Latest AI trends"
})

# Example 2 → analysis
result2 = app.invoke({
    "input": "What is 45 * 23?"
})

# Example 3 → writing
result3 = app.invoke({
    "input": "Write a professional email for leave request"
})

print(result1["final_answer"])
print(result2["final_answer"])
print(result3["final_answer"])