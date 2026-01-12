from fastapi import FastAPI

app = FastAPI(
    title="Smart Document Check Agent",
    description="Internal document validation system with explainable AI",
    version="0.1.0"
)


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "smart-document-check-agent"
    }
