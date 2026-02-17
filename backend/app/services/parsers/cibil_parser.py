import re
from datetime import datetime


def parse_cibil_fields(raw_text: str) -> dict:
    fields = {}

    if not raw_text:
        return fields

    # -------------------------
    # CIBIL Score
    # -------------------------
    score_match = re.search(
        r"CIBIL\s+Score\s+is\s+(\d{3})",
        raw_text,
        re.IGNORECASE
    )
    if score_match:
        fields["cibil_score"] = int(score_match.group(1))

    # -------------------------
    # Report Date
    # -------------------------
    date_match = re.search(
        r"as of Date\s*:\s*(\d{2}/\d{2}/\d{4})",
        raw_text,
        re.IGNORECASE
    )
    if date_match:
        try:
            fields["report_date"] = datetime.strptime(
                date_match.group(1),
                "%d/%m/%Y"
            ).date()
        except:
            pass

    # -------------------------
    # Name
    # -------------------------
    name_match = re.search(
        r"Hello,\s*([A-Z ]+)",
        raw_text
    )
    if name_match:
        fields["name"] = name_match.group(1).title().strip()

    # -------------------------
    # PAN
    # -------------------------
    pan_match = re.search(
        r"\b[A-Z]{5}[0-9]{4}[A-Z]\b",
        raw_text
    )
    if pan_match:
        fields["pan_number"] = pan_match.group(0)

    print("DEBUG | Parsed CIBIL fields:", fields, flush=True)

    return fields
