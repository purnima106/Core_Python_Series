from langgraph.graph import StateGraph, END
from typing import TypedDict
from langchain_openai import ChatOpenAI

class CodeState(TypedDict):
    input: str
    code: str
    output: str
    error: str
    iterations: int
    