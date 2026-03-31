from langchain_groq import ChatGroq
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.tools import tool
from langchain_core.prompts import ChatPromptTemplate

@tool
def multiply(a: int, b: int) -> int:
    return a * b

@tool
def search(query: str) -> str:
    return f"Search results for: {query}"

llm = ChatGroq(model="llama3-70b-8192", temperature=0)

tools = [multiply, search]

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant. Use tools when needed."),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}"),
])

agent = create_tool_calling_agent(llm, tools, prompt)

executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

executor.invoke({"input": "What is 42 * 17?"})