from dotenv import load_dotenv
load_dotenv()  # MUST be before any app imports so env vars are available

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.review import router as review_router

app = FastAPI(title="GitHub PR Reviewer API")

# Allow all origins for deployment. 
# In a strict production environment, you should replace ["*"] with your specific domain.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include the review router
app.include_router(review_router, prefix="/api")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
