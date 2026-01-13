from datetime import date


def mock_extract_salary_slip():
    return {
        "employee_name": "Ravi Kumar",
        "employer_name": "ABC Technologies Pvt Ltd",
        "employer_address": None,   # Missing on purpose
        "salary_month": date(2025, 12, 1),
        "gross_salary": 80000,
        "net_salary": 85000,        # Invalid on purpose
        "employee_id": "EMP12345"
    }
