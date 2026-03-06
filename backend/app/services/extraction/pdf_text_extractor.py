import os
from pypdf import PdfReader
import pytesseract
from pdf2image import convert_from_path


# ---------------------------------------------------------
# Extract text using PyPDF (fast path)
# ---------------------------------------------------------
def _extract_with_pypdf(pdf_path: str) -> str:
    text_parts = []

    reader = PdfReader(pdf_path)

    for idx, page in enumerate(reader.pages):
        try:
            text = page.extract_text() or ""
            print(f"DEBUG | PyPDF page {idx+1} length: {len(text)}", flush=True)
            text_parts.append(text)
        except Exception as e:
            print(f"DEBUG | PyPDF error page {idx+1}: {e}", flush=True)

    return "\n".join(text_parts).strip()


# ---------------------------------------------------------
# OCR fallback (slow but reliable)
# ---------------------------------------------------------
def _extract_with_ocr(pdf_path: str) -> str:
    print("DEBUG | Running OCR fallback...", flush=True)

    images = convert_from_path(pdf_path)
    text_parts = []

    for i, img in enumerate(images):
        text = pytesseract.image_to_string(img, lang="eng")
        print(f"DEBUG | OCR page {i+1} length: {len(text)}", flush=True)
        text_parts.append(text)

    return "\n".join(text_parts).strip()


# ---------------------------------------------------------
# Public function used by pipeline
# ---------------------------------------------------------
def extract_text_from_pdf(pdf_path: str) -> str:
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(pdf_path)

    print(f"DEBUG | Extracting text from PDF: {pdf_path}", flush=True)

    # Step 1: Try PyPDF
    text = _extract_with_pypdf(pdf_path)

    # Step 2: If empty -> OCR fallback
    if not text or len(text) < 30:
        print("DEBUG | PyPDF returned empty text. Switching to OCR.", flush=True)
        text = _extract_with_ocr(pdf_path)

    print(f"DEBUG | Final extracted text length: {len(text)}", flush=True)

    return text