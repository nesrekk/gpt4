"""Part H (Q10) - complete Intelligent Email Assistant with a continuous menu."""
from input_module import display_email, read_email
from intent_module import detect_intent
from reply_module import generate_reply
from retrieval_module import EmailRetriever, display_match
from summary_module import summarize_conversation
from tone_module import TONES, rewrite_tone
from utils import save_reply

MENU = """
==============================================
    INTELLIGENT EMAIL ASSISTANT (Ollama)
==============================================
 1. Enter Customer Email
 2. Detect Intent
 3. Find Similar Previous Email
 4. Generate AI Reply
 5. Improve Tone (Friendly / Formal / Empathetic)
 6. Conversation Summary
 7. Save Reply
 8. Exit
=============================================="""


def main():
    print("Loading previous customer interactions...")
    retriever = EmailRetriever()
    print(f"{len(retriever.history)} previous emails loaded from data/emails.csv")

    email = intent = match = reply = None

    while True:
        print(MENU)
        choice = input("Enter your choice : ").strip()

        if choice == "8":
            print("\nThank you for using the Intelligent Email Assistant. Goodbye!")
            break
        if choice == "1":
            email = read_email()
            display_email(email)
            intent = match = reply = None
            continue
        if choice not in {"2", "3", "4", "5", "6", "7"}:
            print("Invalid choice. Please enter 1-8.")
            continue
        if email is None:
            print("\nPlease enter a customer email first (option 1).")
            continue

        # Later steps reuse earlier results, computing anything that is still missing
        if intent is None or choice == "2":
            intent = detect_intent(email)
            if choice == "2":
                print("\nDetected Intent")
                print(intent)
                continue
        if match is None or choice == "3":
            match = retriever.most_similar(email)
            if choice == "3":
                print()
                display_match(*match)
                continue
        if reply is None or choice == "4":
            reply = generate_reply(email, match[0]["Previous_Reply"], intent)
            if choice == "4":
                print("\nAI Generated Reply")
                print("-" * 40)
                print(reply)
                continue

        if choice == "5":
            for tone in TONES:
                print(f"\n--- {tone} Tone ---")
                print(rewrite_tone(reply, tone))
        elif choice == "6":
            print("\nConversation Summary")
            print(summarize_conversation(email, intent, reply))
        elif choice == "7":
            path = save_reply(email, reply, intent)
            print("\nReply saved successfully to outputs/" + path.rsplit("/", 1)[-1])


if __name__ == "__main__":
    main()
