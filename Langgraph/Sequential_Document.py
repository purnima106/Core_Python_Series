# -----------------------------
# 🔹 IMPORTS
# -----------------------------

# StateGraph = lets you define a workflow as a graph (nodes + edges)
# END = special marker that tells LangGraph "stop execution here"
from langgraph.graph import StateGraph, END

# TypedDict = used to define a strict structure for the shared state
from typing import TypedDict

# Groq LLM (drop-in replacement for OpenAI)
from langchain_groq import ChatGroq

import requests
import os


# -----------------------------
# 🔹 STEP 1: DEFINE STATE (VERY IMPORTANT)
# -----------------------------

# Think of this as a "shared memory object"
# Every node reads from it and writes to it

class DocState(TypedDict):
    url: str              # Input: URL to process
    raw_text: str         # Output of fetch step
    summary: str          # Output of summarize step
    key_facts: list[str]  # Output of extraction step
    report: str           # Final output


# -----------------------------
# 🔹 STEP 2: INITIALIZE LLM (GROQ)
# -----------------------------

# This is the ONLY place where provider changes
# Everything else (LangGraph logic) stays same

llm = ChatGroq(
    model="llama3-8b-8192",          # Fast + good enough for most tasks
    api_key=os.getenv("GROQ_API_KEY")  # Always use env variables in real apps
)


# -----------------------------
# 🔹 STEP 3: DEFINE NODES
# -----------------------------

# Each node = ONE STEP in the workflow
# Important rules:
# 1. Takes full state as input
# 2. Returns ONLY what it updates (not full state)
# 3. No side effects ideally (pure transformation)


def fetch_node(state: DocState) -> dict:
    """
    STEP 1: Fetch HTML content from the given URL

    What happens here:
    - Reads 'url' from state
    - Calls external API (requests)
    - Stores raw HTML text (trimmed)
    """

    url = state["url"]  # Read from shared state

    response = requests.get(url)

    # We trim to avoid huge token usage in LLM calls
    text = response.text[:3000]

    return {
        "raw_text": text   # Only updating this field
    }


def summarize_node(state: DocState) -> dict:
    """
    STEP 2: Convert raw HTML/text into a meaningful summary

    What happens:
    - Takes raw_text
    - Sends it to LLM
    - LLM compresses information
    """

    raw_text = state["raw_text"]

    # invoke() → sends prompt to model and returns structured response
    response = llm.invoke(f"Summarize this content clearly:\n{raw_text}")

    return {
        "summary": response.content
    }


def extract_node(state: DocState) -> dict:
    """
    STEP 3: Extract structured insights (key facts)

    Why this step exists:
    - Raw summary is unstructured
    - We want bullet points → easier for downstream usage
    """

    summary = state["summary"]

    response = llm.invoke(
        f"Extract 5 important key facts as bullet points:\n{summary}"
    )

    # LLM returns text → we convert to list
    # Clean parsing to avoid empty lines
    facts = [
        line.strip()
        for line in response.content.split("\n")
        if line.strip()
    ]

    return {
        "key_facts": facts
    }


def report_node(state: DocState) -> dict:
    """
    STEP 4: Generate a final structured report

    Why this step:
    - Combine everything into a polished output
    - This is what user sees
    """

    summary = state["summary"]
    facts = state["key_facts"]

    response = llm.invoke(
        f"""
        Create a clean, readable report.

        Summary:
        {summary}

        Key Facts:
        {facts}

        Format it nicely.
        """
    )

    return {
        "report": response.content
    }


# -----------------------------
# 🔹 STEP 4: BUILD GRAPH
# -----------------------------

# This is where LangGraph starts
# You define the workflow structure here

graph = StateGraph(DocState)

# Register nodes (name → function mapping)
graph.add_node("fetch", fetch_node)
graph.add_node("summarize", summarize_node)
graph.add_node("extract", extract_node)
graph.add_node("report", report_node)


# -----------------------------
# 🔹 STEP 5: DEFINE FLOW (EDGES)
# -----------------------------

# This is the MOST IMPORTANT PART of LangGraph

# Entry point → where execution starts
graph.set_entry_point("fetch")

# Define execution path (like a pipeline)
graph.add_edge("fetch", "summarize")
graph.add_edge("summarize", "extract")
graph.add_edge("extract", "report")

# Tell graph where to stop
graph.add_edge("report", END)


# -----------------------------
# 🔹 STEP 6: COMPILE GRAPH
# -----------------------------

# Converts your defined graph into an executable object
# Think: "build the workflow engine"

app = graph.compile()


# -----------------------------
# 🔹 STEP 7: RUN WORKFLOW
# -----------------------------

# You only pass initial input
# Rest of the state gets filled automatically

result = app.invoke({
    "url": "https://example.com"
})

# Final output
print(result["report"])