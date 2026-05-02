# -----------------------------
# 🔹 IMPORTS
# -----------------------------

from langgraph.graph import StateGraph, END  
# StateGraph → used to define workflow as a graph (nodes + edges)
# END → special marker to stop execution

from typing import TypedDict  
# TypedDict → defines structure of shared state (like schema)

from langchain_openai import ChatOpenAI  
# LLM that generates + fixes code


# -----------------------------
# 🔹 DEFINE STATE (CORE CONCEPT)
# -----------------------------

class CodeState(TypedDict):
    input: str        # user problem (e.g., "write python code for factorial")
    code: str         # generated code by LLM
    output: str       # execution result of code
    error: str        # error message if execution fails
    iterations: int   # how many times we've tried fixing


# 👉 IMPORTANT:
# State is SHARED MEMORY across nodes
# Each node:
#   - reads from state
#   - writes ONLY updated fields


# -----------------------------
# 🔹 INITIALIZE LLM
# -----------------------------

llm = ChatOpenAI(model="gpt-4o-mini")


# -----------------------------
# 🔹 NODE 1: WRITE CODE
# -----------------------------

def write_code(state: CodeState) -> CodeState:
    """
    This node generates Python code from user input.
    """
    
    user_input = state["input"]  # read problem statement
    
    # Prompt LLM to generate ONLY Python code
    code = llm.invoke(
        f"Write only Python code for this problem:\n{user_input}"
    ).content
    
    # Return ONLY updated fields
    return {
        "code": code,
        "iterations": state.get("iterations", 0) + 1  # increment retry count
    }


# -----------------------------
# 🔹 NODE 2: RUN CODE
# -----------------------------

def run_code(state: CodeState) -> CodeState:
    """
    This node executes generated Python code.
    """
    
    code = state["code"]  # get code from previous node
    
    try:
        # VERY IMPORTANT:
        # exec() runs code dynamically
        # {} = empty global/local scope (basic sandbox)
        local_vars = {}
        exec(code, {}, local_vars)
        
        # If code runs successfully:
        return {
            "output": str(local_vars),  # capture variables/output
            "error": ""                # no error
        }
    
    except Exception as e:
        # If code fails:
        return {
            "output": "",
            "error": str(e)  # store error message
        }


# -----------------------------
# 🔹 NODE 3: FIX CODE
# -----------------------------

def fix_code(state: CodeState) -> CodeState:
    """
    This node fixes buggy code using LLM.
    """
    
    code = state["code"]    # previous code
    error = state["error"]  # error from execution
    
    # Ask LLM to debug and fix code
    fixed_code = llm.invoke(
        f"""
        Fix this Python code:
        Code:
        {code}
        
        Error:
        {error}
        
        Return ONLY corrected code.
        """
    ).content
    
    return {"code": fixed_code}


# -----------------------------
# 🔹 ROUTER (BRAIN OF FLOW CONTROL)
# -----------------------------

def router(state: CodeState) -> str:
    """
    Decides which node to execute next.
    This is CONDITIONAL ROUTING.
    """
    
    # Case 1: If error exists → fix code
    if state["error"]:
        return "fix_code"
    
    # Case 2: Stop after too many retries
    elif state["iterations"] > 3:
        return "give_up"
    
    # Case 3: No error → done
    else:
        return "done"


# -----------------------------
# 🔹 BUILD GRAPH
# -----------------------------

graph = StateGraph(CodeState)

# Add nodes (each node = one step)
graph.add_node("write_code", write_code)
graph.add_node("run_code", run_code)
graph.add_node("fix_code", fix_code)


# -----------------------------
# 🔹 DEFINE FLOW
# -----------------------------

# Entry point → first node
graph.set_entry_point("write_code")

# Normal flow
graph.add_edge("write_code", "run_code")

# CONDITIONAL FLOW (MOST IMPORTANT PART)
graph.add_conditional_edges(
    "run_code",   # after this node, decision happens
    router,       # function that decides next step
    
    # mapping: router output → next node
    {
        "fix_code": "fix_code",   # go fix code
        "done": END,              # success → stop
        "give_up": END            # too many retries → stop
    }
)

# Loop: after fixing → run again
graph.add_edge("fix_code", "run_code")


# -----------------------------
# 🔹 COMPILE GRAPH
# -----------------------------

app = graph.compile()


# -----------------------------
# 🔹 RUN WORKFLOW
# -----------------------------

result = app.invoke({
    "input": "Write python code to divide 10 by 0"
})

print(result)