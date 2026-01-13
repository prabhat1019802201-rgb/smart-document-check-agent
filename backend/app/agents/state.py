from typing import TypedDict, List, Dict, Any

class ValidationState(TypedDict):
    document_id: str
    document_type: str | None

    extracted_fields: Dict[str, Any]
    issues: List[Dict[str, Any]]

    validation_status: str
    severity: str
    ocr_confidence: float
