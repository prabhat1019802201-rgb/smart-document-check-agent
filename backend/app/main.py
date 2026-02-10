from fastapi import FastAPI
from app.api import documents
from app.db.session import engine
from app.db.base import Base
from app.models import document  # IMPORTANT: import model
from app.models import validation
from app.models import genai_explanation
from app.models import *  # ensures models are registered
#from app.db import init_models  # # TODO: Enable init_models when DB migrations are added
from app.api import documents
import logging
from app.api import case_qa
from fastapi.middleware.cors import CORSMiddleware


logging.basicConfig(
    level=logging.DEBUG,
    format="%(levelname)s | %(message)s"
)

app = FastAPI(
    title="Smart Document Check Agent",
    description="Internal document validation system with explainable AI",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",   # Vite frontend
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


Base.metadata.create_all(bind=engine)
app.include_router(documents.router)
app.include_router(case_qa.router) 

@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "smart-document-check-agent"
    }

