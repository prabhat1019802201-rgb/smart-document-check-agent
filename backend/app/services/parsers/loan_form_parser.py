import re
from datetime import datetime


# ---------------------------------------------------------
# TEXT NORMALIZATION
# ---------------------------------------------------------
def _clean_lines(raw_text: str):
    """
    Normalize OCR text into clean ordered lines.
    """
    lines = [l.strip() for l in raw_text.splitlines()]
    return [l for l in lines if l]


# ---------------------------------------------------------
# HANDLE TWO-COLUMN OCR COLLAPSE (VERY COMMON IN BANK FORMS)
# Example:
# FULL NAME FATHER'S NAME
# PRABHAT KUMAR MAHESH SAH
# ---------------------------------------------------------
def _split_two_values(value_line: str):
    tokens = value_line.split()

    # assume Indian names (2–3 words each)
    if len(tokens) >= 4:
        mid = len(tokens) // 2
        left = " ".join(tokens[:mid])
        right = " ".join(tokens[mid:])
        return left, right

    return value_line, None


# ---------------------------------------------------------
# FIND VALUE AFTER LABEL (VERTICAL FORMS)
# ---------------------------------------------------------
def _value_after_label(lines, label_keywords):
    for i, line in enumerate(lines):
        upper = line.upper()

        if any(keyword in upper for keyword in label_keywords):
            for j in range(i + 1, len(lines)):
                value = lines[j].strip()

                # skip if next line is another label
                if value and not any(k in value.upper() for k in label_keywords):
                    return value

    return None


# ---------------------------------------------------------
# DETECT HORIZONTAL NAME + FATHER ROW
# ---------------------------------------------------------
def _extract_names_from_layout(lines):
    applicant = None
    father = None

    for i, line in enumerate(lines):
        u = line.upper()

        if "FULL NAME" in u and "FATHER" in u:
            if i + 1 < len(lines):
                val_line = lines[i + 1]

                left, right = _split_two_values(val_line)

                applicant = left.title()
                if right:
                    father = right.title()
            break

    return applicant, father


# ---------------------------------------------------------
# SAFE AMOUNT EXTRACTION (HANDLES OCR % / ₹ LOSS)
# ---------------------------------------------------------
def _extract_amount(text):
    """
    OCR-safe amount extraction with noise correction.
    """

    if not text:
        return None

    print("DEBUG | Raw amount text:", text, flush=True)

    # Remove common OCR garbage before parsing
    cleaned = (
        text.replace("₹", "")
            .replace("%", "")
            .replace("l", "")     # OCR misreads ₹ as 'l'
            .replace("I", "")
            .strip()
    )

    # Extract numeric patterns
    matches = re.findall(r"[\d,]+\.\d{2}", cleaned)

    if not matches:
        return None

    values = [float(m.replace(",", "")) for m in matches]

    print("DEBUG | Candidate values:", values, flush=True)

    # -------------------------------------------------
    # BUSINESS SANITY FILTER
    # -------------------------------------------------
    # Monthly salary cannot realistically exceed 10 lakh.
    # If OCR added prefix digit (742800 instead of 42800),
    # choose the smaller realistic number.
    # -------------------------------------------------

    realistic = [v for v in values if v < 1_000_000]

    if realistic:
        selected = min(realistic)
    else:
        selected = min(values)

    print("DEBUG | Selected amount:", selected, flush=True)

    return selected


# ---------------------------------------------------------
# MONTH EXTRACTION
# ---------------------------------------------------------
def _extract_months(text):
    match = re.search(r"(\d+)\s*MONTH", text.upper())
    if match:
        return int(match.group(1))
    return None


# ---------------------------------------------------------
# MAIN PARSER
# ---------------------------------------------------------
def parse_loan_form_fields(raw_text: str) -> dict:
    """
    Robust parser for Indian loan application forms.
    Handles OCR + scanned + generated PDFs.
    """

    if not raw_text:
        return {}

    lines = _clean_lines(raw_text)
    fields = {}

    # -----------------------------------------------------
    # 1️⃣ NAME EXTRACTION (Handle Horizontal Layout First)
    # -----------------------------------------------------
    applicant, father = _extract_names_from_layout(lines)

    if applicant:
        fields["applicant_name"] = applicant
    if father:
        fields["father_name"] = father

    # fallback to vertical extraction if not found
    if "applicant_name" not in fields:
        name = _value_after_label(lines, ["FULL NAME"])
        if name:
            fields["applicant_name"] = name.title()

    if "father_name" not in fields:
        father = _value_after_label(lines, ["FATHER"])
        if father:
            fields["father_name"] = father.title()

    # -----------------------------------------------------
    # 2️⃣ DOB
    # -----------------------------------------------------
    dob_text = _value_after_label(lines, ["DATE OF BIRTH"])
    if dob_text:
        try:
            fields["dob"] = datetime.strptime(dob_text.strip(), "%d/%m/%Y").date()
        except Exception:
            pass

    # -----------------------------------------------------
    # 3️⃣ Aadhaar
    # -----------------------------------------------------
    aadhaar = re.search(r"\d{4}\s?\d{4}\s?\d{4}", raw_text)
    if aadhaar:
        fields["aadhaar_number"] = aadhaar.group(0).replace(" ", "")

    # -----------------------------------------------------
    # 4️⃣ PAN
    # -----------------------------------------------------
    pan = re.search(r"[A-Z]{5}[0-9]{4}[A-Z]", raw_text)
    if pan:
        fields["pan_number"] = pan.group(0)

    # -----------------------------------------------------
    # 5️⃣ Loan Amount
    # -----------------------------------------------------
    amount_line = _value_after_label(lines, ["REQUESTED AMOUNT"])
    if amount_line:
        amt = _extract_amount(amount_line)
        if amt:
            fields["loan_amount"] = amt

    # -----------------------------------------------------
    # 6️⃣ Loan Tenure
    # -----------------------------------------------------
    tenure_line = _value_after_label(lines, ["LOAN TENURE"])
    if tenure_line:
        months = _extract_months(tenure_line)
        if months:
            fields["loan_tenure_months"] = months

    # -----------------------------------------------------
    # 7️⃣ Monthly Income
    # -----------------------------------------------------
    income_line = _value_after_label(lines, ["MONTHLY NET INCOME", "MONTHLY INCOME"])
    if income_line:
        income = _extract_amount(income_line)
        if income:
            fields["monthly_income"] = income

    # -----------------------------------------------------
    # 8️⃣ Employer
    # -----------------------------------------------------
    employer = _value_after_label(lines, ["EMPLOYER NAME"])
    if employer:
        fields["company_name"] = employer

    print("DEBUG | Parsed Loan Application fields:", fields, flush=True)

    return fields
