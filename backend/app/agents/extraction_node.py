from app.services.extraction.pdf_text_extractor import extract_text_from_pdf
from app.services.parsers.routers import parse_fields_by_document_type


def extraction_node(state):
    """
    Extracts raw text from PDF and parses structured fields.
    Pure deterministic node.
    """

    file_path = state.get("file_path")
    document_type = state.get("document_type")

    # Safety guard (never crash graph)
    if not file_path:
        state["raw_text"] = ""
        state["extracted_fields"] = {}
        return state

    # Extract text using PyPDF
    raw_text = extract_text_from_pdf(file_path) or ""
    state["raw_text"] = raw_text

    # Parse structured fields
    extracted_fields = parse_fields_by_document_type(
        document_type=document_type,
        raw_text=raw_text
    )

    state["extracted_fields"] = extracted_fields
    
    print("DEBUG | Extracted PAN fields:", extracted_fields)
    return state
