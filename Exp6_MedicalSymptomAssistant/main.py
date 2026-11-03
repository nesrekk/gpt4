"""Main module - AI-Powered Medical Symptom Assistant with continuous interaction until Exit."""
import os
import textwrap

from analysis_module import analyze_symptoms
from context_module import build_context
from input_module import read_patient_input
from profile_module import build_profile
from question_module import ask_questions, generate_questions
from safety_module import assess
from save_module import save_report
from symptom_module import extract_symptoms
from utils import DISCLAIMER

BANNER = f"""
==============================================================
      AI-POWERED MEDICAL SYMPTOM ASSISTANT (Ollama)
==============================================================
{textwrap.fill("DISCLAIMER: " + DISCLAIMER, 62)}
=============================================================="""


def wrap(text, first=" • ", rest="   "):
    return textwrap.fill(str(text), 96, initial_indent=first, subsequent_indent=rest)


def build_report(profile, symptoms, context, safety, analysis, questions):
    lines = []

    def section(title):
        lines.extend(["", title, "-" * 62])

    section("PATIENT PROFILE")
    lines.append(f"Age / Sex      : {profile['age']} years ({profile['age_group']}), {profile['sex']}")
    lines.append(f"Duration       : {context['duration']}    Severity : {context['severity']}")
    lines.append(f"History        : {context['history']}")
    lines.append(f"Medication     : {context['medication']}")
    lines.append(f"Allergies      : {context['allergies']}")
    lines.append(f"Risk factors   : {', '.join(context['risk_factors']) or 'None identified'}")
    section("IDENTIFIED SYMPTOMS")
    lines.extend(wrap(s) for s in symptoms)
    section(f"TRIAGE LEVEL : {safety['level']}")
    lines.extend(wrap(f) for f in safety["red_flags"])
    lines.append(wrap(safety["advice"], "Advice : ", "         "))
    section("POSSIBLE CONDITIONS (not a diagnosis)")
    for i, c in enumerate(analysis["possible_conditions"], 1):
        lines.append(f"{i}. {c.get('condition')}  [Likelihood: {c.get('likelihood')}]")
        lines.append(wrap(c.get("reasoning", ""), "   ", "   "))
    if safety["level"] == "EMERGENCY":
        # the rule-based triage overrides the model's routine advice
        section("WHAT TO DO NOW")
        lines.append(wrap("Call 108 or go to the nearest emergency department immediately."))
        lines.append(wrap("Do not drive yourself; ask someone to take you or wait for the ambulance."))
        lines.append(wrap("Rest in a comfortable position and keep someone with you until help arrives."))
        lines.append("Recommended : Emergency department (immediately)")
    else:
        section("GENERAL SELF-CARE")
        lines.extend(wrap(s) for s in analysis["self_care"])
        section("SEE A DOCTOR IF")
        lines.extend(wrap(s) for s in analysis["see_doctor_if"])
        lines.append(f"Recommended specialist : {analysis['recommended_specialist']}")
    section("FOLLOW-UP QUESTIONS")
    lines.extend(wrap(q, f"{i}. ", "   ") for i, q in enumerate(questions, 1))
    section("DISCLAIMER")
    lines.append(textwrap.fill(DISCLAIMER, 96))
    return lines


def assess_once():
    data = read_patient_input()
    try:
        profile = build_profile(data)
    except ValueError as error:
        print(f"\nInvalid input: {error}")
        return
    if not data["symptoms"]:
        print("\nPlease describe at least one symptom.")
        return

    context = build_context(data, profile)
    safety = assess(data, profile, context)
    if safety["level"] == "EMERGENCY":
        print("\n!!! EMERGENCY WARNING: " + "; ".join(safety["red_flags"]))
        print("!!! " + safety["advice"])

    print("\nAnalysing symptoms...")
    symptoms = extract_symptoms(data["symptoms"])
    analysis = analyze_symptoms(profile, symptoms, context)
    questions = generate_questions(profile, symptoms, context)
    lines = build_report(profile, symptoms, context, safety, analysis, questions)
    print("\n".join(lines))

    if input("\nAnswer the follow-up questions to refine the analysis? (y/n) : ").lower().startswith("y"):
        answers = ask_questions(questions)
        if answers:
            data["additional"] = f"{data['additional']}. Follow-up answers: " + " | ".join(answers)
            context = build_context(data, profile)
            safety = assess(data, profile, context)
            print("\nRefining the analysis with your answers...")
            analysis = analyze_symptoms(profile, symptoms, context)
            lines = build_report(profile, symptoms, context, safety, analysis, questions)
            print("\n".join(lines))

    if input("\nSave this report? (y/n) : ").strip().lower().startswith("y"):
        record = {"input": data, "profile": profile, "symptoms": symptoms, "context": context,
                  "triage": safety, "analysis": analysis, "follow_up_questions": questions,
                  "disclaimer": DISCLAIMER}
        txt, js = save_report(lines, record)
        print("Report saved successfully:")
        print("  reports/" + os.path.basename(txt))
        print("  reports/" + os.path.basename(js))


def main():
    print(BANNER)
    while True:
        assess_once()
        if not input("\nStart a new assessment? (y/n) : ").strip().lower().startswith("y"):
            print("\nTake care! Please consult a doctor for any health concern. Goodbye!")
            break
        print()


if __name__ == "__main__":
    main()
