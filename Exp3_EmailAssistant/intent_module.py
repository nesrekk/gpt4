"""Part B - Intent detection with Ollama (Q3)."""
from utils import ask_llm

# The six intents from the lab sheet plus the extra categories found in the dataset
INTENTS = ["Delivery Issue", "Refund Request", "Product Complaint", "Technical Support",
           "Order Cancellation", "General Inquiry", "Payment Issue", "Warranty",
           "Account Issue", "Exchange Request"]


def detect_intent(email):
    reply = ask_llm(
        "Classify the customer email into exactly one of these intents:\n"
        + "\n".join(f"- {i}" for i in INTENTS)
        + f"\n\nSubject: {email['subject']}\nEmail: {email['body']}\n\n"
        "Answer with the intent name only.",
        system="You are an email intent classifier.",
        temperature=0,
    )
    for intent in INTENTS:
        if intent.lower() in reply.lower():
            return intent
    return "General Inquiry"


if __name__ == "__main__":
    from input_module import read_email

    email = read_email()
    print("\nDetected Intent")
    print(detect_intent(email))
