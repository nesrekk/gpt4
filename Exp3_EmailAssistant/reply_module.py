"""Part D - AI reply generation (Q6)."""
from utils import ask_llm, clean_email


def generate_reply(email, previous_reply, intent):
    """Q6: professional reply using the customer email and the most similar previous reply."""
    return clean_email(ask_llm(
        "Write a professional customer support email reply.\n"
        f"Customer name: {email['name']}\n"
        f"Subject: {email['subject']}\n"
        f"Detected intent: {intent}\n"
        f"Customer email: {email['body']}\n"
        f"Reply our team sent to a similar past email (use it as guidance): {previous_reply}\n\n"
        f"Start with 'Dear {email['name']},', keep it to 3-4 short sentences, do not invent "
        "order numbers, dates or amounts, and end with:\nRegards,\nSupport Team\n"
        "Return only the email."
    ))


if __name__ == "__main__":
    from input_module import read_email

    email = read_email()
    previous = input("Previous Reply : ")
    print("\n" + generate_reply(email, previous, "General Inquiry"))
