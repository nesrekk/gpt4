"""Question module - generates follow-up questions and collects the answers."""
from prompt_module import build_question_prompt
from utils import ask_llm_json


def generate_questions(profile, symptoms, context):
    data = ask_llm_json(build_question_prompt(profile, symptoms, context), temperature=0)
    return [str(q).strip() for q in data.get("questions", []) if str(q).strip()][:5]


def ask_questions(questions):
    """Ask each question; returns 'Q: A' lines for the questions the user answered."""
    answers = []
    for i, question in enumerate(questions, 1):
        answer = input(f"Q{i}. {question}\n    Answer : ").strip()
        if answer:
            answers.append(f"{question} {answer}")
    return answers
