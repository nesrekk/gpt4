"""Part F - LLM based intent detection (Q12)."""
import re

from llm_utils import ask_llm

INTENTS = ["FAQ", "RECOMMENDATION", "PRODUCT", "REVIEW"]

SYSTEM_PROMPT = """You are an intent classifier for an e-commerce chatbot.
Classify the user's message into exactly ONE label:
FAQ - orders, delivery, tracking, returns, refunds, payment, account or store policy questions
RECOMMENDATION - the user wants suggestions or asks which product to buy
PRODUCT - the user asks about a specific product's details, price, brand or features
REVIEW - the user asks what customers think, reviews, ratings or opinions of a product

Examples:
Where is my parcel? -> FAQ
How do I return my order? -> FAQ
Recommend a gaming laptop -> RECOMMENDATION
Suggest a good smartwatch under 20000 -> RECOMMENDATION
Tell me about Samsung Galaxy -> PRODUCT
What is the price of HP Laptop 2? -> PRODUCT
What do customers say about Lenovo Laptop 3? -> REVIEW
Show reviews for Sony Headphones 1 -> REVIEW

Reply with the label only."""

# Used only if the small model replies with something that is not a valid label.
KEYWORDS = {
    "REVIEW": ["review", "customers think", "customers say", "opinion", "feedback"],
    "RECOMMENDATION": ["recommend", "suggest", "best", "which should i buy"],
    "PRODUCT": ["tell me about", "price", "brand", "details", "specification"],
}


def keyword_intent(message):
    text = message.lower()
    for intent, words in KEYWORDS.items():
        if any(w in text for w in words):
            return intent
    return "FAQ"


def detect_intent(message):
    reply = ask_llm(SYSTEM_PROMPT, message, temperature=0).upper()
    for intent in INTENTS:
        if re.search(rf"\b{intent}\b", reply):
            return intent
    return keyword_intent(message)


if __name__ == "__main__":
    for i, question in enumerate(
        ["Where is my parcel?", "Recommend a gaming laptop", "Tell me about Samsung Galaxy"], 1
    ):
        print(f"Example {i}")
        print("Question")
        print(question)
        print("Output")
        print("Intent")
        print(detect_intent(question))
        print()
    while True:
        question = input("Question (exit to stop): ")
        if question.strip().lower() == "exit":
            break
        print("Intent :", detect_intent(question))
