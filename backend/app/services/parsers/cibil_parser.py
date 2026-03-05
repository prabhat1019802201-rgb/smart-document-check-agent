import re
from datetime import datetime


def parse_cibil_fields(raw_text: str) -> dict:
    """
    Extract fields from CIBIL Score report.
    """

    text = raw_text.upper()
    fields = {}

    # --------------------------------------------------
    # Name
    # --------------------------------------------------
    name_match = re.search(r"HELLO[, ]+([A-Z ]+)", text)

    if name_match:
        name = name_match.group(1).strip()
        fields["name"] = name.title()

    # --------------------------------------------------
    # CIBIL Score
    # --------------------------------------------------
    score_match = re.search(r"CIBIL SCORE.*?(\b[3-9][0-9]{2}\b)", text)

    if score_match:
        fields["cibil_score"] = int(score_match.group(1))

    # --------------------------------------------------
    # Report Date
    # --------------------------------------------------
    date_match = re.search(r"DATE\s*:\s*(\d{2}/\d{2}/\d{4})", text)

    if date_match:
        try:
            fields["report_date"] = datetime.strptime(
                date_match.group(1), "%d/%m/%Y"
            ).date()
        except:
            pass

    # --------------------------------------------------
    # Control Number
    # --------------------------------------------------
    control_match = re.search(r"CONTROL NUMBER\s*:\s*([\d,\.]+)", text)

    if control_match:
        control = re.sub(r"[^\d]", "", control_match.group(1))
        fields["control_number"] = control

    print("DEBUG | Parsed CIBIL fields:", fields, flush=True)

    return fields