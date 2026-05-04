from dotenv import load_dotenv
load_dotenv()  # MUST be before any app imports so env vars are available

from fastapi import FastAPI
from app.api.review import router as review_router

app = FastAPI(title="GitHub PR Reviewer API")

# Include the review router
app.include_router(review_router, prefix="/api")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
