from fastapi import FastAPI
# from app.graph import app_graph
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

@app.get("/")
def home():
    """
    Basic test route to check if server is running
    """
    return {"message": "AI Research Assistant is running 🚀"}

@app.post("/query")
def query(input: str):
    """
    This will later connect to LangGraph
    For now → simple placeholder
    """
    
    # Temporary response
    return {
        "input": input,
        "response": f"Received your query: {input}"
    }