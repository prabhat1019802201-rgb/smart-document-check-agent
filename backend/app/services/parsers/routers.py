from app.services.parsers.loan_form_parser import parse_loan_form_fields
from app.services.parsers.aadhaar_parser import parse_aadhaar_fields
from app.services.parsers.pan_parser import parse_pan_fields
from app.services.parsers.cibil_parser import parse_cibil_fields
from app.services.parsers.income_proof_parser import parse_income_proof_fields


def parse_fields_by_document_type(document_type: str, raw_text: str) -> dict:
    if document_type == "pan":
        return parse_pan_fields(raw_text)

    if document_type == "aadhaar":
        return parse_aadhaar_fields(raw_text)

    if document_type == "cibil":
        return parse_cibil_fields(raw_text)

    if document_type == "income_proof":
        return parse_income_proof_fields(raw_text)

    if document_type in ["loan_request_form", "loan_application_form"]:
        return parse_loan_form_fields(raw_text)

    return {}
