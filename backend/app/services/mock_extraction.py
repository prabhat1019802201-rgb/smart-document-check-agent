from datetime import date
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

def mock_extract_pan_card():
    return {
        "pan_number": "ABCDE1234F",  # change to test invalid cases
        "name": "RAVI KUMAR",
        "dob": date(1992, 5, 12)
    }

def mock_extract_aadhaar_card():
    return {
        "aadhaar_number": "123412341234",  # change to test invalid
        "name": "RAVI KUMAR",
        "dob": date(1992, 5, 12),
        "gender": "Male",
        "address": "Bangalore, Karnataka"
    }


def mock_extract_cibil_report():
    return {
        "name": "RAVI KUMAR",
        "cibil_score": 720,
        "report_date": date(2025, 12, 1)
    }

def mock_extract_loan_request_form():
    return {
        "applicant_name": "RAVI KUMAR",
        "loan_amount": 1500000,
        "loan_tenure_months": 240,
        "employment_type": "Salaried",  # Salaried / Self-employed
        "monthly_income": 85000,
        "company_name": None,  # intentionally missing
        "residential_address": "Bangalore, Karnataka"
    }

def mock_extract_income_proof_salary_slip():
    return {
        "income_proof_type": "salary_slip",
        "employment_status": "Salaried",
        "company_name": "ABC Technologies Pvt Ltd",
        "gross_income": 570900.00,
        "net_income": 509300.03,
        "income_period": "Monthly"
    }


def mock_extract_income_proof_certificate():
    return {
        "income_proof_type": "income_certificate",
        "employment_status": "Unemployed",
        "company_name": "SELF / NA",
        "gross_income": 300000.00,
        "net_income": 300000.00,
        "income_period": "Annual"
    }