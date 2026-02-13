import re
from datetime import datetime


def clean_name(text: str):
    """
    Remove OCR garbage and keep only valid name text
    """
    text = re.sub(r"[^A-Za-z ]", "", text)
    text = re.sub(r"\s+", " ", text).strip()

    if len(text) < 4:
        return None

    # Reject words like DOB, GOVT, etc.
    blacklist = ["DOB", "GOV", "INDIA", "UIDAI", "MALE", "FEMALE"]
    if any(word in text.upper() for word in blacklist):
        return None

    return text.title()


def parse_aadhaar_fields(raw_text: str) -> dict:
    fields = {}

    lines = [l.strip() for l in raw_text.splitlines() if l.strip()]

    # -------------------------
    # Aadhaar Number
    # -------------------------
    aadhaar_match = re.search(r"\b(\d{4}\s?\d{4}\s?\d{4})\b", raw_text)
    if aadhaar_match:
        fields["aadhaar_number"] = aadhaar_match.group(1).replace(" ", "")

    # -------------------------
    # DOB
    # -------------------------
    dob_match = re.search(r"(\d{2}[\/\-]\d{2}[\/\-]\d{4})", raw_text)
    if dob_match:
        try:
            fields["dob"] = datetime.strptime(
                dob_match.group(1),
                "%d/%m/%Y"
            ).date()
        except:
            pass

    # -------------------------
    # Gender
    # -------------------------
    gender_match = re.search(r"\b(Male|Female|Other)\b", raw_text, re.IGNORECASE)
    if gender_match:
        fields["gender"] = gender_match.group(1).capitalize()

    # -------------------------
    # NAME EXTRACTION (BEST LOGIC)
    # -------------------------
    name = None

    # ⭐ Rule 1: First valid alphabetic line
    for line in lines[:5]:  # Only top portion
        candidate = clean_name(line)
        if candidate:
            name = candidate
            break

    # ⭐ Rule 2: Fallback → line before DOB
    if not name:
        for i, line in enumerate(lines):
            if re.search(r"\d{2}/\d{2}/\d{4}", line):
                if i > 0:
                    candidate = clean_name(lines[i - 1])
                    if candidate:
                        name = candidate
                        break

    if name:
        fields["name"] = name

    # -------------------------
    # Address
    # -------------------------
    addr_match = re.search(
        r"Address[:\s]*(.*?)\d{6}",
        raw_text,
        re.IGNORECASE | re.DOTALL
    )
    if addr_match:
        address = re.sub(r"\s+", " ", addr_match.group(1)).strip()
        address = re.sub(r"[-,]+$", "", address).strip()
        fields["address"] = address

    print("DEBUG | Parsed Aadhaar fields:", fields, flush=True)

    return fields
