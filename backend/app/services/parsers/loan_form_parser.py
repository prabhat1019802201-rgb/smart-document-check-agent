import re


def parse_loan_form_fields(text: str) -> dict:
    fields = {}

    # Applicant Name
    name_match = re.search(r"Applicant Name\s*[:\-]?\s*(.+)", text, re.IGNORECASE)
    if name_match:
        fields["applicant_name"] = name_match.group(1).strip()

    # Loan Amount
    amount_match = re.search(r"Loan Amount\s*[:\-]?\s*₹?\s*([\d,]+)", text, re.IGNORECASE)
    if amount_match:
        fields["loan_amount"] = int(amount_match.group(1).replace(",", ""))

    # Employment Type
    emp_match = re.search(r"Employment Type\s*[:\-]?\s*(Salaried|Self[- ]Employed)", text, re.IGNORECASE)
    if emp_match:
        fields["employment_type"] = emp_match.group(1).title()

    # Company Name
    company_match = re.search(r"Company Name\s*[:\-]?\s*(.+)", text, re.IGNORECASE)
    if company_match:
        fields["company_name"] = company_match.group(1).strip()

    return fields
