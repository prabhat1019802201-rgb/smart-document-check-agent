import re
from datetime import datetime

PAN_REGEX = r"[A-Z]{5}[0-9]{4}[A-Z]"


def parse_pan_fields(raw_text: str) -> dict:
    fields = {}

    if not raw_text:
        return fields

    # PAN Number
    pan_match = re.search(PAN_REGEX, raw_text)
    if pan_match:
        fields["pan_number"] = pan_match.group(0)

    # Name
    name_match = re.search(r"Full Name:\s*(.+)", raw_text, re.IGNORECASE)
    if name_match:
        fields["name"] = name_match.group(1).strip()

    # DOB
    dob_match = re.search(r"Date of Birth:\s*(\d{2}-\d{2}-\d{4})", raw_text)
    if dob_match:
        try:
            fields["dob"] = datetime.strptime(
                dob_match.group(1), "%d-%m-%Y"
            ).date()
        except ValueError:
            pass

    return fields
