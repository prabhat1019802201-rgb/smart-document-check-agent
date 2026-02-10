import re
from datetime import datetime


def parse_aadhaar_fields(raw_text: str) -> dict:
    fields = {}

    text = raw_text.replace("\n", " ").strip()

    # -------------------------
    # Aadhaar Number
    # -------------------------
    aadhaar_match = re.search(
        r"(\d{4}\s\d{4}\s\d{4})",
        raw_text
    )
    if aadhaar_match:
        fields["aadhaar_number"] = aadhaar_match.group(1).replace(" ", "")

    # -------------------------
    # Name
    # -------------------------
    name_match = re.search(
        r"Name:\s*([A-Za-z ]+)",
        raw_text,
        re.IGNORECASE
    )
    if name_match:
        fields["name"] = name_match.group(1).strip()

    # -------------------------
    # Date of Birth
    # -------------------------
    dob_match = re.search(
        r"(DOB|Date of Birth)\s*[:\-]?\s*(\d{2}[\/\-]\d{2}[\/\-]\d{4})",
        raw_text,
        re.IGNORECASE
    )
    if dob_match:
        try:
            fields["dob"] = datetime.strptime(
                dob_match.group(2),
                "%d/%m/%Y"
            ).date()
        except ValueError:
            pass

    # -------------------------
    # Gender
    # -------------------------
    gender_match = re.search(
        r"Gender\s*[:\-]?\s*(Male|Female|Other)",
        raw_text,
        re.IGNORECASE
    )
    if gender_match:
        fields["gender"] = gender_match.group(1).capitalize()

    # -------------------------
    # Address (multi-line)
    # -------------------------
    address_match = re.search(
        r"Address\s*:\s*(.*?)\d{6}",
        raw_text,
        re.IGNORECASE | re.DOTALL
    )
    if address_match:
        address = address_match.group(1)
        address = re.sub(r"\s+", " ", address).strip()
        fields["address"] = address

    print("DEBUG | Parsed Aadhaar fields:", fields, flush=True)

    return fields
