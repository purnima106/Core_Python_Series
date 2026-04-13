from langchain_google_genai import ChatGoogleGenerativeAI
import os

llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash",api_key=os.getenv("GEMINI_API_KEY"))

def orchestrator(state):
    """Decides how to handle the query.
    (For now → simple response, later → routing)
    """

    user_input = state["input"]
    response = llm.invoke(f"Answer this: {user_input}").content
    return {"output": response}
    