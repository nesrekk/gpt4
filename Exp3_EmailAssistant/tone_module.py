"""Part E - Tone improver (Q7)."""
from utils import ask_llm, clean_email

TONES = {
    "Friendly": "warm, friendly and conversational",
    "Formal": "formal, polite and business-like",
    "Empathetic": "empathetic, understanding the customer's frustration and reassuring them",
}


def rewrite_tone(reply, tone):
    """Q7: rewrite the reply in the requested tone without changing the facts."""
    return clean_email(ask_llm(
        f"Rewrite this customer support email so the tone is {TONES[tone]}. Keep the same "
        "facts, the greeting and the 'Regards, Support Team' sign-off. Return only the email.\n\n"
        + reply,
        temperature=0.6,
    ))


if __name__ == "__main__":
    text = input("Reply to rewrite : ")
    for tone in TONES:
        print(f"\n--- {tone} Tone ---")
        print(rewrite_tone(text, tone))
