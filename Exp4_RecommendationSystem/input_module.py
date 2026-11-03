"""Part A - User profile collection (Q1)."""


def read_profile():
    """Q1: read the user's details, interests, preferences and requirements."""
    print("Enter your profile details")
    profile = {
        "name": input("Name : ").strip(),
        "age": input("Age : ").strip(),
        "background": input("Background (education / profession) : ").strip(),
        "interests": input("Interests : ").strip(),
        "skill_level": input("Skill Level : ").strip(),
        "category": input("Preferred Category (courses / books / projects ...) : ").strip(),
        "preference": input("Preference : ").strip(),
        "goal": input("Goal : ").strip(),
    }
    count = input("No. of Items : ").strip()
    profile["count"] = int(count) if count.isdigit() else 5
    return profile


if __name__ == "__main__":
    print(read_profile())
