from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.services.case_qa_service import answer_case_question

router = APIRouter(prefix="/cases", tags=["Case Q&A"])

@router.post("/{case_id}/ask")
def ask_case_question(
    case_id: str,
    payload: dict,
    db: Session = Depends(get_db)
):
    question = payload.get("question")
    return {
        "case_id": case_id,
        "answer": answer_case_question(
            db=db,
            case_id=case_id,
            question=question
        )
    }
