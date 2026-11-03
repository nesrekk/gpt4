"""Profile module - validates and structures the user's age and sex."""

SEX_VALUES = {"m": "Male", "male": "Male", "f": "Female", "female": "Female"}


def build_profile(data):
    """Return a cleaned profile, or raise ValueError with a message for invalid input."""
    if not data["age"].isdigit() or not 0 < int(data["age"]) <= 120:
        raise ValueError("Age must be a whole number between 1 and 120.")
    age = int(data["age"])
    if age < 13:
        group = "Child"
    elif age < 18:
        group = "Adolescent"
    elif age < 60:
        group = "Adult"
    else:
        group = "Older adult"
    sex = SEX_VALUES.get(data["sex"].lower(), "Other / not stated")
    return {"age": age, "age_group": group, "sex": sex}
