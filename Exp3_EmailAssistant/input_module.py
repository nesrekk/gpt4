"""Part A - User input (Q1, Q2)."""


def read_email():
    """Q1: read customer name, email subject and customer email."""
    name = input("Customer Name : ").strip()
    subject = input("Subject : ").strip()
    body = input("Customer Email :\n").strip()
    return {"name": name, "subject": subject, "body": body}


def display_email(email):
    """Q2: display the entered details."""
    print("-" * 40)
    print(f"Customer Name : {email['name']}")
    print(f"Subject       : {email['subject']}")
    print("Customer Email")
    print(email["body"])
    print("-" * 40)


if __name__ == "__main__":
    display_email(read_email())
