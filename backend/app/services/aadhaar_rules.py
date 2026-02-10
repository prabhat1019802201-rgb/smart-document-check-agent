import re

AADHAAR_REGEX = r"^[0-9]{12}$"


def validate_aadhaar_card(fields: dict):
    issues = []

    if not fields.get("aadhaar_number") or not re.match(AADHAAR_REGEX, fields["aadhaar_number"]):
        issues.append({
            "issue_type": "Invalid",
            "field_name": "aadhaar_number",
            "severity": "High",
            "why_flagged": "Aadhaar number must be a 12-digit numeric value.",
            "suggested_action": "Upload a valid Aadhaar card with a clear Aadhaar number."
        })

    for field in ["name", "dob", "gender", "address"]:
        if not fields.get(field):
            issues.append({
                "issue_type": "Missing",
                "field_name": field,
                "severity": "High",
                "why_flagged": f"{field.capitalize()} is mandatory on Aadhaar card.",
                "suggested_action": f"Upload Aadhaar card with {field} clearly visible."
            })

    return issues
