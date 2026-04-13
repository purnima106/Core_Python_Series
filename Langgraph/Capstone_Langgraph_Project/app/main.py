from fastapi import FastAPI
from pydantic import BaseModel
from app.graph.graph import app_graph
from dotenv import load_dotenv
import os

class QueryRequest(BaseModel):
    input: str

load_dotenv(dotenv_path=r"C:\Users\Purnima.N\OneDrive - DXC Production\Desktop\Practice_series\Core_Python_Series\Langgraph\Capstone_Langgraph_Project\.env")

app = FastAPI()

@app.get("/")
def home():
    """
    Basic test route to check if server is running
    """
    return {"message": "AI Research Assistant is running 🚀"}

@app.post("/query")
def query(request: QueryRequest):
    """Now this calls Langgraph instead of dummy response"""
    result = app_graph.invoke({"input": request.input})
    return {"response": result["output"]}
