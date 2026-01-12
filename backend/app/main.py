from fastapi import FastAPI
from app.api import documents

app = FastAPI(
    title="Smart Document Check Agent",
    description="Internal document validation system with explainable AI",
    version="0.1.0"
)

app.include_router(documents.router)

@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "smart-document-check-agent"
    }

