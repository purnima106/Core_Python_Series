#LLM → thinks → searches → reads → calculates → thinks again → answers

# This is called the ReAct pattern:

# Reason + Act + Observe + Repeat

from langchain_core.tools import tool
from langchain.memory import ConversationBufferMemory
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain.agents import create_tool_calling_agent,AgentExecutor
import requests

#web search Tool

@tool
def search_web(query:str) -> str:
    """search the web for information"""
    from tavily import TavilyClient
    client = TavilyClient(api_key="")
    result = client.search(query)
    return str(result)


# 2. URL Reader Tool
@tool
def read_url(url: str) -> str:
    """Fetch and read content from a URL"""
    response = requests.get(url)
    return response.text[:2000]


# 3. Python REPL Tool
@tool
def calculator(code: str) -> str:
    """Execute Python code for calculations"""
    try:
        return str(eval(code))
    except Exception as e:
        return str(e)

memory = ConversationBufferMemory(
    memory_key = "chat_history",
    return_messages=True
)

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a smart research assistant. Use tools when needed."),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}")
])
llm = ChatGroq(model="llama3-70b-8192", temperature=0)

tools = [search_web,read_url, calculator]

agent = create_tool_calling_agent(llm, tools, prompt)

executor = AgentExecutor(
    agent= agent,
    tools=tools,
    memory=memory,
    verbose=True
)

executor.invoke({"input":"Find the latest news about AI and summarize it"})







    
