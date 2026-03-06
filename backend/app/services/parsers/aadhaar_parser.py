import re
from datetime import datetime


def _normalize(text: str) -> str:
    if not text:
        return ""
    return re.sub(r"\s+", " ", text)


def _extract_aadhaar_number(text: str):
    """
    Extract Aadhaar number while ignoring VID numbers.
    """

    candidates = re.finditer(r"\b\d{4}\s\d{4}\s\d{4}\b", text)

    for match in candidates:
        number = match.group()
        start = match.start()

        # Look at nearby text
        context = text[max(0, start-20): start+20].upper()

        # Skip if part of VID
        if "VID" in context:
            continue

        return number.replace(" ", "")

    return None


def _extract_dob(text: str):
    """
    Extract DOB only from DOB marker.
    """
    match = re.search(r"DOB\s*[:\-]?\s*(\d{2}/\d{2}/\d{4})", text.upper())
    if match:
        try:
            return datetime.strptime(match.group(1), "%d/%m/%Y").date()
        except:
            pass
    return None


def _extract_gender(text: str):
    text = text.upper()

    if "MALE" in text:
        return "Male"
    if "FEMALE" in text:
        return "Female"

    return None


def _extract_name(lines):
    """
    UIDAI Aadhaar normally prints:
    Hindi Name
    English Name
    """
    for i, line in enumerate(lines):

        if "DOB" in line.upper():
            # Name is usually above DOB line
            if i >= 1:
                name = lines[i-1].strip()

                if (
                    len(name) > 2
                    and not any(x in name.upper() for x in ["ENROLMENT", "GOVERNMENT", "AADHAAR"])
                ):
                    return name.title()

    return None


def _extract_address(text: str):
    """
    Extract address block starting from 'Address'
    """
    match = re.search(
        r"ADDRESS\s*[:\-]?\s*(.+?)(\d{6})",
        text.upper(),
        re.DOTALL,
    )

    if match:
        addr = match.group(1) + " " + match.group(2)
        return addr.replace("\n", " ").title()

    return None


def parse_aadhaar_fields(raw_text: str) -> dict:

    text = _normalize(raw_text)
    lines = [l.strip() for l in raw_text.splitlines() if l.strip()]

    fields = {}

    # -------------------------
    # Aadhaar Number
    # -------------------------
    aadhaar = _extract_aadhaar_number(text)
    if aadhaar:
        fields["aadhaar_number"] = aadhaar

    # -------------------------
    # DOB
    # -------------------------
    dob = _extract_dob(text)
    if dob:
        fields["dob"] = dob

    # -------------------------
    # Gender
    # -------------------------
    gender = _extract_gender(text)
    if gender:
        fields["gender"] = gender

    # -------------------------
    # Name
    # -------------------------
    name = _extract_name(lines)
    if name:
        fields["name"] = name

    # -------------------------
    # Address
    # -------------------------
    address = _extract_address(raw_text)
    if address:
        fields["address"] = address

    print("DEBUG | Parsed Aadhaar fields:", fields, flush=True)

    return fields