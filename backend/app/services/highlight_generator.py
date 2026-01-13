def generate_mock_highlight(field_name: str):
    """
    Mock highlight coordinates for document preview.
    These coordinates simulate OCR bounding boxes.
    Later, this will be replaced by real OCR output.
    """

    mapping = {
        # -----------------------------
        # Salary Slip fields
        # -----------------------------
        "employer_address": {
            "page": 1,
            "x": 100,
            "y": 300,
            "width": 260,
            "height": 40
        },
        "net_salary": {
            "page": 1,
            "x": 380,
            "y": 520,
            "width": 180,
            "height": 35
        },

        # -----------------------------
        # PAN Card fields
        # -----------------------------
        "pan_number": {
            "page": 1,
            "x": 220,
            "y": 260,
            "width": 260,
            "height": 35
        },
        "name": {
            "page": 1,
            "x": 220,
            "y": 300,
            "width": 260,
            "height": 35
        },
        "dob": {
            "page": 1,
            "x": 220,
            "y": 340,
            "width": 180,
            "height": 35
        },

        # -----------------------------
        # Aadhaar fields
        # -----------------------------
        "aadhaar_number": {
            "page": 1,
            "x": 180,
            "y": 240,
            "width": 300,
            "height": 35
        },
        "gender": {
            "page": 1,
            "x": 180,
            "y": 280,
            "width": 150,
            "height": 35
        },
        "address": {
            "page": 1,
            "x": 180,
            "y": 320,
            "width": 400,
            "height": 60
        },

        # -----------------------------
        # CIBIL fields
        # -----------------------------
        "cibil_score": {
            "page": 1,
            "x": 250,
            "y": 200,
            "width": 120,
            "height": 40
        },
        "report_date": {
            "page": 1,
            "x": 250,
            "y": 250,
            "width": 180,
            "height": 35
        },


        # -----------------------------
        # Loan Request Form fields
        # -----------------------------
        "applicant_name": {
           "page": 1,
            "x": 200,
            "y": 180,
            "width": 280,
           "height": 35
         },
       "loan_amount": {
         "page": 1,
         "x": 200,
         "y": 220,
         "width": 200,
         "height": 35
     },
     "loan_tenure_months": {
        "page": 1,
        "x": 200,
        "y": 260,
        "width": 160,
       "height": 35
      },
    "employment_type": {
       "page": 1,
       "x": 200,
       "y": 300,
      "width": 200,
      "height": 35
       },
     "company_name": {
       "page": 1,
        "x": 200,
       "y": 340,
       "width": 300,
      "height": 35
     },
     "residential_address": {
        "page": 1,
        "x": 200,
        "y": 380,
        "width": 420,
        "height": 60
      }

    }

    return mapping.get(field_name)
