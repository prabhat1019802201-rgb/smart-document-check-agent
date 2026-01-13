from datetime import date


MANDATORY_FIELDS = {
    "employee_name": "High",
    "employer_name": "High",
    "employer_address": "High",
    "salary_month": "Medium",
    "gross_salary": "High",
    "net_salary": "High",
    "employee_id": "Medium"
}


def validate_salary_slip(extracted_fields: dict):
    issues = []

    # 1. Mandatory field checks
    for field, severity in MANDATORY_FIELDS.items():
        if not extracted_fields.get(field):
            issues.append({
                "issue_type": "Missing",
                "field_name": field,
                "severity": severity,
                "why_flagged": f"{field.replace('_', ' ').title()} is mandatory for salary verification.",
                "suggested_action": f"Upload a salary slip containing {field.replace('_', ' ')}."
            })

    # 2. Salary consistency check
    gross = extracted_fields.get("gross_salary")
    net = extracted_fields.get("net_salary")

    if gross and net and net > gross:
        issues.append({
            "issue_type": "Invalid",
            "field_name": "net_salary",
            "severity": "High",
            "why_flagged": "Net salary cannot be greater than gross salary.",
            "suggested_action": "Verify salary figures in the uploaded document."
        })

    # 3. Salary month validation
    salary_month = extracted_fields.get("salary_month")
    if salary_month and salary_month > date.today():
        issues.append({
            "issue_type": "Invalid",
            "field_name": "salary_month",
            "severity": "Medium",
            "why_flagged": "Salary month cannot be a future date.",
            "suggested_action": "Upload a salary slip for a valid salary period."
        })

    return issues
