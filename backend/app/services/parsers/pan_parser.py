import re
from datetime import datetime


def parse_pan_fields(raw_text: str) -> dict:
    fields = {}

    if not raw_text:
        return fields

    # Normalize
    text = raw_text.upper()

    # Remove all spaces/newlines for PAN detection
    compact_text = re.sub(r"\s+", "", text)

    # -------------------------
    # PAN NUMBER (Strong Detection)
    # -------------------------
    pan_match = re.search(r"[A-Z]{5}[0-9]{4}[A-Z]", compact_text)
    if pan_match:
        fields["pan_number"] = pan_match.group()

    # -------------------------
    # Date of Birth
    # -------------------------
    dob_match = re.search(r"\b\d{2}[\/\-]\d{2}[\/\-]\d{4}\b", raw_text)
    if dob_match:
        try:
            fields["dob"] = datetime.strptime(
                dob_match.group().replace("-", "/"),
                "%d/%m/%Y"
            ).date()
        except ValueError:
            pass

    # -------------------------
    # Name
    # -------------------------
    lines = [line.strip() for line in raw_text.splitlines() if line.strip()]

    for i, line in enumerate(lines):
        if "NAME" in line.upper():
            if i + 1 < len(lines):
                candidate = re.sub(r"[^A-Za-z ]", "", lines[i + 1]).strip()
                if len(candidate.split()) >= 2:
                    fields["name"] = candidate.title()
                    break

    print("DEBUG | Parsed PAN fields:", fields, flush=True)

    return fields
