# Import required modules
from langchain.vectorstores import FAISS          # Used to store embeddings (vector DB)
from langchain.embeddings import OpenAIEmbeddings # Converts text → vectors
from langchain_core.tools import tool             # Decorator to define tools
from langchain_openai import ChatOpenAI           # LLM
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate
import pandas as pd


# -----------------------------
# 🔹 STEP 1: CREATE VECTOR DB (RAG)
# -----------------------------

# These are your internal documents (in real case → PDFs, DB, etc.)
documents = [
    "LangChain is a framework for building LLM applications",
    "LangGraph is used for building stateful workflows with LLMs"
]

# Convert text → embeddings and store in FAISS
vectorstore = FAISS.from_texts(documents, OpenAIEmbeddings())

# Retriever is what we actually use to fetch relevant docs
retriever = vectorstore.as_retriever()


# -----------------------------
# 🔹 STEP 2: DEFINE TOOLS
# -----------------------------

@tool
def search_docs(query: str) -> str:
    """
    Search internal company documents.
    Use this when the question is about internal knowledge or concepts.
    """
    # This calls vector DB → retrieves relevant chunks
    docs = retriever.invoke(query)
    
    # Always return string (important for LLM)
    return str(docs)


@tool
def search_web(query: str) -> str:
    """
    Search the web for latest or real-time information.
    Use this for current events or recent updates.
    """
    from tavily import TavilyClient
    
    # Tavily is a search API designed for LLM agents
    client = TavilyClient(api_key="YOUR_API_KEY")
    
    # Returns search results
    return str(client.search(query))


# Load CSV (structured data)
df = pd.read_csv("sales.csv")


@tool
def query_csv(question: str) -> str:
    """
    Answer questions about sales data stored in CSV.
    Use this for numerical or structured data queries.
    """
    try:
        # Basic version → returns statistics
        # (later you can replace with LLM + pandas reasoning)
        return str(df.describe())
    
    except Exception as e:
        return str(e)


# -----------------------------
# 🔹 STEP 3: CREATE LLM
# -----------------------------

# This is the brain deciding which tool to use
llm = ChatOpenAI(model="gpt-4o-mini")


# -----------------------------
# 🔹 STEP 4: DEFINE TOOLS LIST
# -----------------------------

# Agent will choose ONLY from these tools
tools = [search_docs, search_web, query_csv]


# -----------------------------
# 🔹 STEP 5: PROMPT
# -----------------------------

prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        # This instruction controls agent behavior
        "You are an intelligent assistant. "
        "Choose the most appropriate tool based on the user's question."
    ),
    
    ("human", "{input}"),  # User input comes here
    
    # VERY IMPORTANT:
    # This is where reasoning + tool history is stored
    ("placeholder", "{agent_scratchpad}")
])


# -----------------------------
# 🔹 STEP 6: CREATE AGENT
# -----------------------------

# This wraps LLM + tools into an agent
agent = create_tool_calling_agent(llm, tools, prompt)


# -----------------------------
# 🔹 STEP 7: EXECUTOR
# -----------------------------

executor = AgentExecutor(
    agent=agent,
    tools=tools,
    
    # Shows step-by-step reasoning (VERY IMPORTANT for learning)
    verbose=True
)


# -----------------------------
# 🔹 STEP 8: RUN QUERIES
# -----------------------------

# Example 1 → should use RAG (internal docs)
executor.invoke({
    "input": "What is LangChain?"
})

# Example 2 → should use web
executor.invoke({
    "input": "Latest AI news"
})

# Example 3 → should use CSV
executor.invoke({
    "input": "What is the average sales?"
})