"""Part F - Conversation summary (Q8)."""
from utils import ask_llm


def summarize_conversation(email, intent, reply):
    """Q8: summary of the customer issue in about 50 words."""
    return ask_llm(
        "Summarize this customer support conversation in about 50 words: the customer's "
        "issue and the action promised by support. Return one paragraph only.\n\n"
        f"Customer: {email['name']}\nSubject: {email['subject']}\nIntent: {intent}\n"
        f"Customer email: {email['body']}\nSupport reply: {reply}",
        temperature=0.2,
    )


if __name__ == "__main__":
    from input_module import read_email

    email = read_email()
    print("\nSummary")
    print(summarize_conversation(email, "General Inquiry", ""))
