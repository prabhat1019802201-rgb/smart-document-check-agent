from pypdf import PdfReader

def extract_text_from_pdf(file_path: str) -> str:
    """
    Extract raw text from text-based PDFs using PyPDF.
    """
    reader = PdfReader(file_path)
    text_chunks = []

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text_chunks.append(page_text)

    return "\n".join(text_chunks).strip()


