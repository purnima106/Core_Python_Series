from typing import TypedDict

class ResearchState(TypedDict):
    input: str
    decision: str
    research_data: str
    doc_data: str
    code_result: str
    final_answer: str
    approved: bool
    