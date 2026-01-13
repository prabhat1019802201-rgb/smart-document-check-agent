from app.services.mock_extraction import mock_extract_salary_slip


def extraction_node(state):
    if state["document_type"] == "Salary Slip":
        state["extracted_fields"] = mock_extract_salary_slip()
    else:
        state["extracted_fields"] = {}

    return state


