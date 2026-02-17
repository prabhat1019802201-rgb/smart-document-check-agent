import re
from typing import Dict, Optional


# ---------------------------------------------------------
# TEXT NORMALIZATION
# ---------------------------------------------------------
def _normalize_text(text: str) -> str:
    """
    Clean OCR noise while preserving structure.
    """
    if not text:
        return ""

    text = text.replace("\r", "\n")

    # Remove repeated spaces
    text = re.sub(r"[ \t]+", " ", text)

    # Remove strange OCR symbols
    text = re.sub(r"[^\x00-\x7F₹\n.,:/()-]", " ", text)

    return text


def _lines(text: str):
    return [l.strip() for l in text.split("\n") if l.strip()]


# ---------------------------------------------------------
# GENERIC AMOUNT EXTRACTOR (STRICT)
# ---------------------------------------------------------
def _extract_amounts(line: str):
    """
    Extract only valid currency numbers.
    Avoid picking IDs, years, etc.
    """
    matches = re.findall(r"₹?\s?([\d,]+\.\d{2})", line)
    values = []

    for m in matches:
        try:
            values.append(float(m.replace(",", "")))
        except Exception:
            pass

    return values


# ---------------------------------------------------------
# PAN EXTRACTION
# ---------------------------------------------------------
def _extract_pan(text: str) -> Optional[str]:
    match = re.search(r"\b[A-Z]{5}[0-9]{4}[A-Z]\b", text.upper())
    return match.group(0) if match else None


# ---------------------------------------------------------
# NAME EXTRACTION (FROM CERTIFICATE TEXT)
# Example:
# "This is to certify that Mr. Prabhat Kumar..."
# ---------------------------------------------------------
def _extract_employee_name(text: str) -> Optional[str]:
    match = re.search(
        r"(Mr\.?|Ms\.?|Mrs\.?)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+){1,3})",
        text,
        re.IGNORECASE,
    )
    if match:
        return match.group(2).strip()

    return None


# ---------------------------------------------------------
# COMPANY EXTRACTION
# ---------------------------------------------------------
def _extract_company(lines) -> Optional[str]:
    """
    Look for Pvt Ltd / Limited etc.
    """
    for line in lines:
        if re.search(r"(PVT|PRIVATE|LIMITED|LTD)", line.upper()):
            return line.strip()

    return None


# ---------------------------------------------------------
# SALARY TABLE PARSING
# ---------------------------------------------------------
def _extract_salary_components(lines):
    """
    Extract structured salary rows like:
    Basic Salary ........ ₹25,000.00
    HRA ................. ₹10,000.00
    Net Salary .......... ₹42,800.00
    """

    basic = hra = gross = net = None

    for line in lines:
        upper = line.upper()

        values = _extract_amounts(line)
        if not values:
            continue

        amount = values[0]

        if "BASIC" in upper:
            basic = amount

        elif "HRA" in upper:
            hra = amount

        elif "GROSS" in upper:
            gross = amount

        elif "NET" in upper or "TAKE HOME" in upper or "IN HAND" in upper:
            net = amount

    return basic, hra, gross, net


# ---------------------------------------------------------
# FALLBACK: FIND ISOLATED "MONTHLY" SENTENCE
# ---------------------------------------------------------
def _extract_inline_monthly_income(text: str) -> Optional[float]:
    """
    Handles narrative certificates:
    "His monthly salary is ₹42,800.00"
    """
    match = re.search(
        r"(monthly\s+(net|salary|income)[^\d]{0,10})(₹?\s?[\d,]+\.\d{2})",
        text,
        re.IGNORECASE,
    )
    if match:
        values = _extract_amounts(match.group(0))
        if values:
            return values[0]

    return None


# ---------------------------------------------------------
# MAIN PARSER
# ---------------------------------------------------------
def parse_income_proof_fields(raw_text: str) -> Dict:
    """
    Primary parser used by extraction node.
    """

    text = _normalize_text(raw_text)
    lines = _lines(text)

    fields = {
        "income_proof_type": "salary_certificate",
    }

    # -----------------------------
    # Identity Information
    # -----------------------------
    name = _extract_employee_name(text)
    if name:
        fields["employee_name"] = name

    company = _extract_company(lines)
    if company:
        fields["company_name"] = company

    pan = _extract_pan(text)
    if pan:
        fields["pan_number"] = pan

    # -----------------------------
    # Salary Extraction
    # -----------------------------
    basic, hra, gross, net = _extract_salary_components(lines)

    # fallback if structured rows missing
    if not net:
        net = _extract_inline_monthly_income(text)

    # -----------------------------
    # BUSINESS RULE (IMPORTANT)
    # 👉 Take Monthly Net as FINAL income
    # -----------------------------
    final_income = net or gross or basic

    if basic:
        fields["basic_salary"] = basic

    if hra:
        fields["hra"] = hra

    if gross:
        fields["gross_income"] = gross

    if final_income:
        fields["net_income"] = final_income

    print("DEBUG | Parsed Income Proof fields:", fields, flush=True)

    return fields
