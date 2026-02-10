from pypdf import PdfReader


def extract_text_from_pdf(file_path: str) -> str:
    print(f"DEBUG | Extracting text from PDF: {file_path}")

    reader = PdfReader(file_path)
    text_chunks = []

    for idx, page in enumerate(reader.pages):
        page_text = page.extract_text()
        if page_text:
            print(f"DEBUG | Page {idx+1} text length:", len(page_text))
            text_chunks.append(page_text)
        else:
            print(f"DEBUG | Page {idx+1} has NO extractable text")

    final_text = "\n".join(text_chunks).strip()
    print("DEBUG | Total extracted text length:", len(final_text))

    return final_text
