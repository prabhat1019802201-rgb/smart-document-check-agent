import re
from datetime import datetime
from typing import Dict


def parse_cibil_fields(raw_text: str) -> Dict:
    """
    Parse structured fields from CIBIL credit report text.

    Expected output schema (USED BY VALIDATOR):
    {
        "cibil_score": int,
        "report_date": date,
        "name": str,
        "pan_number": str
    }
    """

    fields: Dict = {}

    if not raw_text:
        return fields

    text = raw_text.replace("\n", " ")

    # --------------------------------------------------
    # 1. CIBIL SCORE
    # Example:
    #   CIBIL SCORE
    #   785
    # --------------------------------------------------
    score_match = re.search(
        r"CIBIL\s*SCORE\s*(\d{3})",
        raw_text,
        re.IGNORECASE
    )
    if score_match:
        try:
            fields["cibil_score"] = int(score_match.group(1))
        except ValueError:
            pass

    # --------------------------------------------------
    # 2. REPORT DATE
    # Example:
    #   As of Date: 15-01-2026
    # --------------------------------------------------
    date_match = re.search(
        r"As\s*of\s*Date\s*[:\-]?\s*(\d{2}-\d{2}-\d{4})",
        raw_text,
        re.IGNORECASE
    )
    if date_match:
        try:
            fields["report_date"] = datetime.strptime(
                date_match.group(1), "%d-%m-%Y"
            ).date()
        except ValueError:
            pass

    # --------------------------------------------------
    # 3. FULL NAME
    # Example:
    #   Full Name: Rajesh Kumar Sharma
    # --------------------------------------------------
    name_match = re.search(
        r"Full\s*Name\s*[:\-]?\s*([A-Za-z ]{3,})",
        text,
        re.IGNORECASE
    )
    if name_match:
        fields["name"] = name_match.group(1).strip()

    # --------------------------------------------------
    # 4. PAN NUMBER
    # Example:
    #   PAN Number: BFGPS1234K
    # --------------------------------------------------
    pan_match = re.search(
        r"PAN\s*Number\s*[:\-]?\s*([A-Z]{5}[0-9]{4}[A-Z])",
        text,
        re.IGNORECASE
    )
    if pan_match:
        fields["pan_number"] = pan_match.group(1)

    return fields
