import re
from datetime import datetime
from typing import Optional, Dict


# ---------------------------------------------------------
# TEXT CLEANING
# ---------------------------------------------------------
def _clean_text(text: str) -> str:
    """
    Normalize OCR text.
    Removes OCR junk while keeping structure.
    """
    if not text:
        return ""

    text = text.replace("\r", "\n")

    # Remove repeated symbols/noise
    text = re.sub(r"[^\w\n/: -]", " ", text)

    # Collapse whitespace
    text = re.sub(r"[ \t]+", " ", text)

    return text.upper()


# ---------------------------------------------------------
# PAN NUMBER
# ---------------------------------------------------------
def _extract_pan_number(text: str) -> Optional[str]:
    """
    PAN format: AAAAA9999A
    """
    match = re.search(r"\b[A-Z]{5}[0-9]{4}[A-Z]\b", text)
    return match.group(0) if match else None


# ---------------------------------------------------------
# DOB
# ---------------------------------------------------------
def _extract_dob(text: str) -> Optional[datetime.date]:
    """
    Extract DOB like:
    20/12/2001 or 20-12-2001
    """
    match = re.search(r"\b(\d{2}[/-]\d{2}[/-]\d{4})\b", text)
    if not match:
        return None

    date_str = match.group(1)

    for fmt in ("%d/%m/%Y", "%d-%m-%Y"):
        try:
            return datetime.strptime(date_str, fmt).date()
        except ValueError:
            continue

    return None


# ---------------------------------------------------------
# NAME (STOP BEFORE FATHER SECTION)
# ---------------------------------------------------------
def _extract_name(text: str) -> Optional[str]:
    """
    Extract PAN holder name safely from OCR text.

    Strategy:
    1️⃣ Find the line containing NAME keyword
    2️⃣ Take ONLY the immediate next clean text portion
    3️⃣ Reject OCR-noise words like 'FACT', 'ARA', etc.
    """

    lines = text.split("\n")

    for i, line in enumerate(lines):
        if "NAME" in line:
            # Try to extract name from SAME line first
            same_line = re.sub(r".*NAME[:/ ]*", "", line).strip()

            candidate = same_line if same_line else (
                lines[i + 1].strip() if i + 1 < len(lines) else ""
            )

            # Remove OCR noise words commonly seen in PAN scans
            candidate = re.sub(
                r"\b(FATHER|FACT|ARA|SIGNATURE|DATE|DOB|GOVT|INDIA)\b",
                "",
                candidate
            )

            # Keep alphabets only
            candidate = re.sub(r"[^A-Z ]", " ", candidate)

            candidate = re.sub(r"\s+", " ", candidate).strip()

            words = candidate.split()

            # Accept only human-like names
            if 2 <= len(words) <= 4:
                return " ".join(w.capitalize() for w in words)

    return None

# ---------------------------------------------------------
# FATHER NAME
# ---------------------------------------------------------
def _extract_father_name(text: str) -> Optional[str]:
    """
    Extract father's name safely.
    """

    match = re.search(
        r"FATHER(.+?)(DATE|DOB|SIGNATURE)",
        text,
        re.DOTALL
    )

    if not match:
        return None

    segment = match.group(1)

    segment = re.sub(r"[^A-Z ]", " ", segment)

    words = [w for w in segment.split() if len(w) > 1]

    if 2 <= len(words) <= 4:
        return " ".join(w.capitalize() for w in words)

    return None


# ---------------------------------------------------------
# MAIN PARSER
# ---------------------------------------------------------
def parse_pan_fields(raw_text: str) -> Dict:
    """
    PAN document parser resilient to OCR noise.
    """

    if not raw_text:
        return {}

    text = _clean_text(raw_text)

    pan_number = _extract_pan_number(text)
    dob = _extract_dob(text)
    name = _extract_name(text)
    father_name = _extract_father_name(text)

    fields = {}

    if pan_number:
        fields["pan_number"] = pan_number

    if name:
        fields["name"] = name

    if father_name:
        fields["father_name"] = father_name

    if dob:
        fields["dob"] = dob

    print("DEBUG | Parsed PAN fields:", fields, flush=True)

    return fields
