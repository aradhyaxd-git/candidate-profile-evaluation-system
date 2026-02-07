from fastapi import FastAPI
from app.api.v1.candidate import router as candidate_router

app = FastAPI()

@app.get("/")
def root():
    return {"status": "Server is running 🚀"}

app.include_router(candidate_router, prefix="/api/v1")
