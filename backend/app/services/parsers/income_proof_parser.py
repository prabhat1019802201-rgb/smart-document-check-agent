import re


def parse_income_proof_fields(text: str) -> dict:
    fields = {}

    # Employment Status
    if "Unemployed" in text:
        fields["employment_status"] = "Unemployed"
        fields["company_name"] = "SELF / NA"
    else:
        fields["employment_status"] = "Salaried"

    # Company Name
    company_match = re.search(r"Company Name\s*[:\-]?\s*(.+)", text, re.IGNORECASE)
    if company_match:
        fields["company_name"] = company_match.group(1).strip()

    # Gross Income
    gross_match = re.search(r"Gross\s*(Income|Salary)\s*[:\-]?\s*₹?\s*([\d,]+)", text, re.IGNORECASE)
    if gross_match:
        fields["gross_income"] = int(gross_match.group(2).replace(",", ""))

    # Net Income
    net_match = re.search(r"Net\s*(Income|Salary)\s*[:\-]?\s*₹?\s*([\d,]+)", text, re.IGNORECASE)
    if net_match:
        fields["net_income"] = int(net_match.group(2).replace(",", ""))

    return fields
