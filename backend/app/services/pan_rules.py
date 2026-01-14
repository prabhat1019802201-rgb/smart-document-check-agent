import re
from datetime import date, datetime

PAN_REGEX = r"^[A-Z]{5}[0-9]{4}[A-Z]{1}$"


def validate_pan_card(fields: dict):
    issues = []

    pan_number = fields.get("pan_number")
    name = fields.get("name")
    dob_raw = fields.get("dob")

    # 1. PAN format check
    if not pan_number or not re.match(PAN_REGEX, pan_number):
        issues.append({
            "issue_type": "Invalid",
            "field_name": "pan_number",
            "severity": "High",
            "why_flagged": "PAN number format is invalid.",
            "suggested_action": "Upload a PAN card with a valid PAN number."
        })

    # 2. Name presence
    if not name:
        issues.append({
            "issue_type": "Missing",
            "field_name": "name",
            "severity": "High",
            "why_flagged": "Name is mandatory on PAN card.",
            "suggested_action": "Upload a PAN card where the name is clearly visible."
        })

    # 3. DOB normalization + validation
    dob = None

    if not dob_raw:
        issues.append({
            "issue_type": "Missing",
            "field_name": "dob",
            "severity": "Medium",
            "why_flagged": "Date of birth is missing on PAN card.",
            "suggested_action": "Upload a PAN card with date of birth visible."
        })
    else:
        if isinstance(dob_raw, date):
            dob = dob_raw
        elif isinstance(dob_raw, str):
            try:
                dob = datetime.fromisoformat(dob_raw).date()
            except ValueError:
                issues.append({
                    "issue_type": "Invalid",
                    "field_name": "dob",
                    "severity": "High",
                    "why_flagged": "Date of birth format is invalid.",
                    "suggested_action": "Upload a PAN card with a valid date of birth."
                })
        else:
            issues.append({
                "issue_type": "Invalid",
                "field_name": "dob",
                "severity": "High",
                "why_flagged": "Unsupported date of birth format.",
                "suggested_action": "Upload a PAN card with readable date of birth."
            })

    # 4. Age sanity check (only if DOB parsed correctly)
    if dob:
        age = date.today().year - dob.year
        if age < 18:
            issues.append({
                "issue_type": "Invalid",
                "field_name": "dob",
                "severity": "High",
                "why_flagged": "PAN holder must be at least 18 years old.",
                "suggested_action": "Verify the date of birth on the PAN card."
            })

    return issues
