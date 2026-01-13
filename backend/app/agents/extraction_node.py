from app.services.mock_extraction import (
    mock_extract_income_proof_salary_slip,
    mock_extract_salary_slip,
    mock_extract_pan_card,
    mock_extract_aadhaar_card,
    mock_extract_cibil_report,
    mock_extract_loan_request_form
)


def extraction_node(state):
    doc_type = (state.get("document_type") or "").lower()

    if doc_type == "income_proof":
        state["extracted_fields"] = mock_extract_income_proof_salary_slip()
    elif doc_type == "pan":
         state["extracted_fields"] = mock_extract_pan_card()
    elif doc_type == "aadhaar":
         state["extracted_fields"] = mock_extract_aadhaar_card()
    elif doc_type == "cibil":
         state["extracted_fields"] = mock_extract_cibil_report()
    elif doc_type == "loan request form":
         state["extracted_fields"] = mock_extract_loan_request_form()
    else:
         state["extracted_fields"] = {}

