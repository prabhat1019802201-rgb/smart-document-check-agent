from typing import TypedDict, Dict, Any


class ValidationState(TypedDict, total=False):
    case_id: str
    document_id: str
    document_type: str

    # 🔑 ADD THIS
    file_path: str

    extracted_fields: Dict[str, Any]
    documents_by_type: Dict[str, Any]

    issues: list
    validation_status: str
    severity: str
    ocr_confidence: float

    raw_text: str
    db: Any
