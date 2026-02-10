import re
from datetime import datetime

PAN_REGEX = r"\b[A-Z]{5}[0-9]{4}[A-Z]\b"
DATE_REGEX = r"\b(\d{2}[/-]\d{2}[/-]\d{4})\b"

def parse_pan_fields(raw_text: str) -> dict:
    fields = {}

    if not raw_text:
        return fields

    text = raw_text.upper()

    # -----------------------------
    # PAN Number
    # -----------------------------
    pan_match = re.search(PAN_REGEX, text)
    if pan_match:
        fields["pan_number"] = pan_match.group(0)

    # -----------------------------
    # Name (line AFTER "NAME")
    # -----------------------------
    name_match = re.search(r"NAME\s*\n([A-Z ]{3,})", text)
    if name_match:
        name = name_match.group(1).strip()
        if len(name.split()) >= 2:
            fields["name"] = name.title()

    # -----------------------------
    # Date of Birth
    # -----------------------------
    dob_match = re.search(DATE_REGEX, text)
    if dob_match:
        try:
            dob = datetime.strptime(
                dob_match.group(1).replace("-", "/"),
                "%d/%m/%Y"
            ).date()
            fields["dob"] = dob
        except ValueError:
            pass

    return fields
