from sqlalchemy.orm import Session
from app.models.case_document import CaseDocument

from langchain_groq import ChatGroq
import os


# ✅ Initialize Groq LLM once
llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.0,
    api_key=os.getenv("GROQ_API_KEY")
)


def answer_case_question(
    db: Session,
    case_id: str,
    question: str
) -> str:
    """
    LLM-powered Q&A over uploaded case documents.
    """

    records = (
        db.query(CaseDocument)
        .filter(CaseDocument.case_id == case_id)
        .all()
    )

    if not records:
        return "No documents found for this case."

    # -----------------------------
    # Build grounded context
    # -----------------------------
    context_blocks = []

    for record in records:
        context_blocks.append(
            f"""
DOCUMENT TYPE: {record.document_type}
EXTRACTED DATA:
{record.extracted_fields}
""".strip()
        )

    context = "\n\n".join(context_blocks)

    # -----------------------------
    # Strict banking-safe prompt
    # -----------------------------
    prompt = f"""
You are a credit underwriting assistant.

Answer the user's question using ONLY the information provided below.
If information is missing, clearly say it is missing.
Do NOT guess or hallucinate.

CASE DATA:
{context}

USER QUESTION:
{question}

FINAL ANSWER:
"""

    response = llm.invoke(prompt)

    return response.content if hasattr(response, "content") else str(response)
