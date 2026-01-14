import re
from datetime import datetime


CIBIL_SCORE_REGEX = r"(CIBIL\s*Score|Score)\s*[:\-]?\s*(\d{3})"
DATE_REGEX = r"(\d{2}[\/\-]\d{2}[\/\-]\d{4})"
PAN_REGEX = r"[A-Z]{5}[0-9]{4}[A-Z]"


def parse_cibil_fields(raw_text: str) -> dict:
    """
    Best-effort parser for CIBIL report using raw PDF text.
    This parser is intentionally conservative.
    """

    extracted = {}

    if not raw_text:
        return extracted

    # -----------------------------
    # 1. CIBIL Score
    # -----------------------------
    score_match = re.search(CIBIL_SCORE_REGEX, raw_text, re.IGNORECASE)
    if score_match:
        extracted["cibil_score"] = int(score_match.group(2))

    # -----------------------------
    # 2. Report Date
    # -----------------------------
    date_match = re.search(DATE_REGEX, raw_text)
    if date_match:
        try:
            extracted["report_date"] = datetime.strptime(
                date_match.group(1), "%d/%m/%Y"
            ).date()
        except ValueError:
            pass

    # -----------------------------
    # 3. PAN Number (optional)
    # -----------------------------
    pan_match = re.search(PAN_REGEX, raw_text)
    if pan_match:
        extracted["pan_number"] = pan_match.group(0)

    # -----------------------------
    # 4. Name (weak heuristic)
    # -----------------------------
    lines = raw_text.splitlines()
    for line in lines[:30]:  # only top section
        if "name" in line.lower():
            extracted["name"] = line.split(":")[-1].strip()
            break

    return extracted
