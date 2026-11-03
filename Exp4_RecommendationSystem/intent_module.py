"""Part H - Intelligent intent detection (Q9)."""
import re

from utils import ask_llm

INTENTS = ["GENERATE_RECOMMENDATION", "REFINE_RECOMMENDATION", "SHOW_PROFILE",
           "EXPLAIN_RECOMMENDATION", "SAVE_RECOMMENDATION", "EXIT"]

PROMPT = """Identify the user's intent in a personalized recommendation app.
GENERATE_RECOMMENDATION - asks for (new) recommendations, courses, books or resources
REFINE_RECOMMENDATION - wants changes: more/fewer of something, easier, different, or gives feedback
SHOW_PROFILE - wants to see their profile or details
EXPLAIN_RECOMMENDATION - asks why something was recommended
SAVE_RECOMMENDATION - wants to save or export the recommendations
EXIT - wants to quit

Examples:
Recommend some AI courses. -> GENERATE_RECOMMENDATION
Give me more beginner-friendly options. -> REFINE_RECOMMENDATION
Why did you recommend this course? -> EXPLAIN_RECOMMENDATION
Show my profile -> SHOW_PROFILE
Save these to a file -> SAVE_RECOMMENDATION
Bye -> EXIT

User: {text}
Answer with the intent label only."""


def detect_intent(text):
    reply = ask_llm(PROMPT.format(text=text), system="You are an intent classifier.",
                    temperature=0).upper()
    for intent in INTENTS:
        if re.search(rf"\b{intent}\b", reply):
            return intent
    return "GENERATE_RECOMMENDATION"


if __name__ == "__main__":
    for i, text in enumerate(["Recommend some AI courses.",
                              "Give me more beginner-friendly options.",
                              "Why did you recommend this course?"], 1):
        print(f"Example {i}")
        print("User:")
        print(text)
        print("Detected Intent:")
        print(detect_intent(text))
        print()
