from app.services.parsers.aadhaar_parser import parse_aadhaar_fields
from app.services.parsers.pan_parser import parse_pan_fields
from app.services.parsers.cibil_parser import parse_cibil_fields
from app.services.parsers.income_proof_parser import parse_income_proof_fields
from app.services.parsers.loan_form_parser import parse_loan_form_fields

from app.services.classifier.document_classifier import detect_document_type


def parse_fields_by_document_type(raw_text: str) -> dict:
    """
    Route extracted text to correct document parser.
    """

    document_type = detect_document_type(raw_text)

    print("DEBUG | Auto-detected document type:", document_type)

    # --------------------------------------------------
    # Aadhaar
    # --------------------------------------------------
    if document_type == "aadhaar":
        return parse_aadhaar_fields(raw_text)

    # --------------------------------------------------
    # PAN
    # --------------------------------------------------
    elif document_type == "pan":
        return parse_pan_fields(raw_text)

    # --------------------------------------------------
    # CIBIL
    # --------------------------------------------------
    elif document_type == "cibil":
        return parse_cibil_fields(raw_text)

    # --------------------------------------------------
    # Income Proof
    # --------------------------------------------------
    elif document_type == "income_proof":
        return parse_income_proof_fields(raw_text)

    # --------------------------------------------------
    # Loan Application
    # --------------------------------------------------
    elif document_type == "loan_application_form":
        return parse_loan_form_fields(raw_text)

    # --------------------------------------------------
    # Unknown
    # --------------------------------------------------
    print("DEBUG | Unknown document type")
    return {}