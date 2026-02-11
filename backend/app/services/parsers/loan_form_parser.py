import re
from datetime import datetime


def parse_loan_form_fields(raw_text: str) -> dict:
    fields = {}

    if not raw_text:
        return fields

    text = raw_text.upper()

    # -------------------------
    # APPLICANT NAME
    # -------------------------
    name_match = re.search(
        r"FULL NAME.*?\n([A-Z ]+)",
        raw_text,
        re.IGNORECASE
    )
    if name_match:
        fields["applicant_name"] = name_match.group(1).strip().title()

    # -------------------------
    # DATE OF BIRTH
    # -------------------------
    dob_match = re.search(
        r"(\d{2}/\d{2}/\d{4})",
        raw_text
    )
    if dob_match:
        try:
            fields["dob"] = datetime.strptime(
                dob_match.group(1),
                "%d/%m/%Y"
            ).date()
        except ValueError:
            pass

    # -------------------------
    # AADHAAR NUMBER
    # -------------------------
    aadhaar_match = re.search(
        r"(\d{4}\s\d{4}\s\d{4})",
        raw_text
    )
    if aadhaar_match:
        fields["aadhaar_number"] = aadhaar_match.group(1).replace(" ", "")

    # -------------------------
    # LOAN AMOUNT
    # -------------------------
    loan_match = re.search(
        r"REQUESTED AMOUNT.*?([\d,\.]+)",
        raw_text,
        re.IGNORECASE | re.DOTALL
    )
    if loan_match:
        amount = loan_match.group(1)
        amount = amount.replace(",", "")
        try:
            fields["loan_amount"] = float(amount)
        except:
            pass

    # -------------------------
    # MONTHLY INCOME
    # -------------------------
    income_match = re.search(
        r"MONTHLY INCOME.*?([\d,\.]+)",
        raw_text,
        re.IGNORECASE
    )
    if income_match:
        income = income_match.group(1).replace(",", "")
        try:
            fields["monthly_income"] = float(income)
        except:
            pass

    print("DEBUG | Parsed Loan Application fields:", fields, flush=True)

    return fields
