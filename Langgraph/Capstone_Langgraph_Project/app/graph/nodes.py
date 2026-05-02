from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini")

def orchestrator(state):
    """
    Decides how to handle the query.
    (For now → simple response, later → routing)
    """
    user_input = state["input"]

    response = llm.invoke(f"You are a helpful assistant. User: {user_input}").content
    return {"output": response}