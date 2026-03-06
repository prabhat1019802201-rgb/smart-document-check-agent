import re
from datetime import datetime


def parse_pan_fields(raw_text: str) -> dict:
    """
    Robust PAN parser for physical PAN and e-PAN.
    Works without relying on labels.
    """

    fields = {}

    text = raw_text.upper()

    # -------------------------------------------------
    # PAN Number
    # -------------------------------------------------
    pan_match = re.search(r"\b[A-Z]{5}[0-9]{4}[A-Z]\b", text)
    if pan_match:
        fields["pan_number"] = pan_match.group()

    # -------------------------------------------------
    # DOB
    # -------------------------------------------------
    dob_match = re.search(r"\b\d{2}/\d{2}/\d{4}\b", text)
    if dob_match:
        try:
            fields["dob"] = datetime.strptime(
                dob_match.group(), "%d/%m/%Y"
            ).date()
        except Exception:
            pass

    # -------------------------------------------------
    # Extract Candidate Names (ALL CAPS, 2+ words)
    # -------------------------------------------------
    lines = [l.strip() for l in raw_text.splitlines() if l.strip()]

    name_candidates = []

    for line in lines:
        clean = line.strip()

        # Remove PAN number lines
        if re.fullmatch(r"[A-Z]{5}[0-9]{4}[A-Z]", clean):
            continue

        # Ignore dates
        if re.search(r"\d{2}/\d{2}/\d{4}", clean):
            continue

        # Must be uppercase words (likely name)
        if re.fullmatch(r"[A-Z ]{5,}", clean):
            words = clean.split()

            if 1 < len(words) <= 4:  # reasonable name length
                name_candidates.append(clean.title())

    # Remove duplicates while preserving order
    seen = set()
    unique_names = []
    for n in name_candidates:
        if n not in seen:
            seen.add(n)
            unique_names.append(n)

    # -------------------------------------------------
    # Assign Name and Father Name
    # -------------------------------------------------
    if len(unique_names) >= 1:
        fields["name"] = unique_names[0]

    if len(unique_names) >= 2:
        fields["father_name"] = unique_names[1]

    print("DEBUG | Parsed PAN fields:", fields, flush=True)

    return fields