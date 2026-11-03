"""Input module - collects basic user information and the symptom description."""


def read_patient_input():
    print("Please answer the following (press Enter to skip optional fields)")
    return {
        "age": input("Age (years) : ").strip(),
        "sex": input("Sex (Male/Female/Other) : ").strip(),
        "symptoms": input("Describe your symptoms : ").strip(),
        "duration": input("Duration (e.g. 2 days, 1 week) : ").strip(),
        "severity": input("Severity (Mild/Moderate/Severe) : ").strip(),
        "history": input("Medical history (e.g. Asthma, Diabetes, None) : ").strip() or "None",
        "medication": input("Current medication : ").strip() or "None",
        "allergies": input("Allergies : ").strip() or "None",
        "additional": input("Additional information (temperature, travel, contacts) : ").strip()
                      or "None",
    }
