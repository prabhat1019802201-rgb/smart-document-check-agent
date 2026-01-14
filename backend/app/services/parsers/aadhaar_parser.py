import re
from datetime import datetime


def parse_aadhaar_fields(text: str) -> dict:
    fields = {}

    # Aadhaar Number
    aadhaar_match = re.search(r"\b\d{4}\s\d{4}\s\d{4}\b", text)
    if aadhaar_match:
        fields["aadhaar_number"] = aadhaar_match.group().replace(" ", "")

    # Name
    name_match = re.search(r"Name\s*[:\-]?\s*(.+)", text, re.IGNORECASE)
    if name_match:
        fields["name"] = name_match.group(1).strip()

    # DOB
    dob_match = re.search(r"DOB\s*[:\-]?\s*(\d{2}/\d{2}/\d{4})", text)
    if dob_match:
        try:
            fields["dob"] = datetime.strptime(dob_match.group(1), "%d/%m/%Y").date()
        except ValueError:
            pass

    return fields
