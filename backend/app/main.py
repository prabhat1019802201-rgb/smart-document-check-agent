from fastapi import FastAPI
from app.api import documents
from app.db.session import engine
from app.db.base import Base
from app.models import document  # IMPORTANT: import model
from app.models import validation
from app.models import genai_explanation
from app.models import *  # ensures models are registered

app = FastAPI(
    title="Smart Document Check Agent",
    description="Internal document validation system with explainable AI",
    version="0.1.0"
)

Base.metadata.create_all(bind=engine)
app.include_router(documents.router)

@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "smart-document-check-agent"
    }

