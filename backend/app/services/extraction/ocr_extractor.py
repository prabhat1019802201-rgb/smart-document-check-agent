from pdf2image import convert_from_path
import pytesseract
import os

POPPLER_PATH = r"C:\Program Files\poppler-25.12.0\Library\bin"
TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH


def extract_text_with_ocr(pdf_path: str) -> str:
    print(f"DEBUG | OCR fallback triggered for: {pdf_path}", flush=True)

    if not os.path.exists(pdf_path):
        print("ERROR | PDF path does not exist", flush=True)
        return ""

    try:
        images = convert_from_path(
            pdf_path,
            dpi=300,
            poppler_path=POPPLER_PATH
        )
    except Exception as e:
        print(f"ERROR | pdf2image failed: {e}", flush=True)
        return ""

    text_chunks = []

    for idx, image in enumerate(images, start=1):
        try:
            text = pytesseract.image_to_string(image, lang="eng")
            print(
                f"DEBUG | OCR page {idx} text length: {len(text)}",
                flush=True
            )

            if text.strip():
                text_chunks.append(text)

        except Exception as e:
            print(f"ERROR | Tesseract failed on page {idx}: {e}", flush=True)

    final_text = "\n".join(text_chunks).strip()
    print(f"DEBUG | OCR total extracted length: {len(final_text)}", flush=True)

    return final_text
