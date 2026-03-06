from app.services.extraction.pdf_text_extractor import extract_text_from_pdf
from app.services.parsers.routers import parse_fields_by_document_type


def extraction_node(state):
    print("DEBUG | extraction_node invoked")

    file_path = state.get("file_path")
    document_type = state.get("document_type")

    print("DEBUG | Graph received document_type:", document_type)
    print("DEBUG | file_path:", file_path)

    if not file_path:
        print("ERROR | file_path missing in state")
        state["extracted_fields"] = {}
        return state

    # -------------------------------------------------
    # STEP 1 — Extract text (Smart extractor handles OCR internally)
    # -------------------------------------------------
    try:
        raw_text = extract_text_from_pdf(file_path)
    except Exception as e:
        print("ERROR | Text extraction failed:", e)
        raw_text = ""

    state["raw_text"] = raw_text

    print("DEBUG | Raw text length:", len(raw_text))
    print("DEBUG | Raw text preview:\n", raw_text[:500])

    # -------------------------------------------------
    # STEP 2 — Parse fields (DO NOT re-detect type here)
    # -------------------------------------------------
    extracted_fields = parse_fields_by_document_type(raw_text)

    print("DEBUG | Extracted fields:", extracted_fields)

    state["extracted_fields"] = extracted_fields

    return state