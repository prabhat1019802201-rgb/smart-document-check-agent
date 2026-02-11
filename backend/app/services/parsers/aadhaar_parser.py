import re
from datetime import datetime


def parse_aadhaar_fields(raw_text: str) -> dict:
    fields = {}

    if not raw_text:
        return fields

    # Normalize text
    text = raw_text.replace("\n", " ").strip()
    lines = [line.strip() for line in raw_text.splitlines() if line.strip()]

    # --------------------------------------------------
    # Aadhaar Number (12 digits with optional spaces)
    # --------------------------------------------------
    aadhaar_match = re.search(r"\b\d{4}\s?\d{4}\s?\d{4}\b", raw_text)
    if aadhaar_match:
        fields["aadhaar_number"] = re.sub(r"\s+", "", aadhaar_match.group())

    # --------------------------------------------------
    # Date of Birth (supports multiple patterns)
    # --------------------------------------------------
    dob_match = re.search(
        r"\b(\d{2}[\/\-]\d{2}[\/\-]\d{4})\b",
        raw_text
    )
    if dob_match:
        try:
            fields["dob"] = datetime.strptime(
                dob_match.group(1).replace("-", "/"),
                "%d/%m/%Y"
            ).date()
        except ValueError:
            pass

    # --------------------------------------------------
    # Gender (label or standalone)
    # --------------------------------------------------
    gender_match = re.search(
        r"\b(MALE|FEMALE|Male|Female|Other)\b",
        raw_text
    )
    if gender_match:
        fields["gender"] = gender_match.group().capitalize()

    # --------------------------------------------------
    # Name Extraction (Robust Logic)
    # --------------------------------------------------
    # Case 1: Labeled format
    name_label_match = re.search(
        r"Name\s*[:\-]?\s*([A-Za-z ]+)",
        raw_text,
        re.IGNORECASE
    )
    if name_label_match:
        fields["name"] = name_label_match.group(1).strip()
    else:
        # Case 2: Positional format
        # Find line containing DOB and extract name before it
        dob_pattern = r"\d{2}[\/\-]\d{2}[\/\-]\d{4}"
        for line in lines:
            if re.search(dob_pattern, line):
                parts = re.split(dob_pattern, line)
                if parts:
                    candidate = parts[0]

                    # Remove noise
                    candidate = re.sub(r"/000[:\s]*", "", candidate)
                    candidate = re.sub(r"[^A-Za-z ]", "", candidate)
                    candidate = candidate.strip()

                    if len(candidate.split()) >= 2:
                        fields["name"] = candidate
                        break

    # --------------------------------------------------
    # Address Extraction
    # --------------------------------------------------
    # Look for "Address" label first
    address_match = re.search(
        r"Address\s*[:\-]?\s*(.*?)(\d{6})",
        raw_text,
        re.IGNORECASE | re.DOTALL
    )
    if address_match:
        address = address_match.group(1)
        address = re.sub(r"\s+", " ", address).strip()
        fields["address"] = address
    else:
        # Fallback: find 6-digit pincode line
        pincode_match = re.search(r"\b\d{6}\b", raw_text)
        if pincode_match:
            pin_index = raw_text.find(pincode_match.group())
            snippet = raw_text[max(0, pin_index - 150):pin_index]
            snippet = re.sub(r"\s+", " ", snippet).strip()
            fields["address"] = snippet

    print("DEBUG | Parsed Aadhaar fields:", fields, flush=True)

    return fields
