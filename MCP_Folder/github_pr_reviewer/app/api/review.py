from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.mcp.tools.analyze import analyze_pr

router = APIRouter()

class ReviewRequest(BaseModel):
    pr_url: str

@router.post("/review")
async def review_pr(data: ReviewRequest):
    try:
        review = await analyze_pr(data.pr_url)
        return {
            "status": "success",
            "review": review
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
# Frontend
#    ↓
# POST /review
#    ↓
# FastAPI
#    ↓
# analyze_pr()
#    ↓
# Claude
#    ↓
# calls get_pr_diff
#    ↓
# gets code
#    ↓
# writes review
#    ↓
# returns response