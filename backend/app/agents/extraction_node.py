from app.services.extraction.pdf_text_extractor import extract_text_from_pdf
from app.services.extraction.ocr_extractor import extract_text_with_ocr
from app.services.parsers.routers import parse_fields_by_document_type


def extraction_node(state):
    print("DEBUG | extraction_node invoked")

    file_path = state.get("file_path")
    document_type = (state.get("document_type") or "").lower()

    print("DEBUG | document_type:", document_type)
    print("DEBUG | file_path:", file_path)

    if not file_path:
        print("ERROR | file_path missing in state")
        state["extracted_fields"] = {}
        return state

    # 1️⃣ Try PyPDF first
    try:
       raw_text = extract_text_with_ocr(file_path)
    except Exception as e:
       print("ERROR | OCR node crashed:", e)
       raw_text = ""

    # 2️⃣ OCR fallback if PyPDF fails
    if not raw_text:
        print("WARNING | No text extracted via PyPDF, switching to OCR")
        raw_text = extract_text_with_ocr(file_path)

    state["raw_text"] = raw_text
    print("DEBUG | Raw text length:", len(raw_text))
    print("DEBUG | Raw text preview:\n", raw_text[:500])

    # 3️⃣ Parse fields
    extracted_fields = parse_fields_by_document_type(
        document_type=document_type,
        raw_text=raw_text
    )

    print("DEBUG | Extracted fields:", extracted_fields)

    state["extracted_fields"] = extracted_fields
    return state
