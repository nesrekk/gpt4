"""Prompt module - builds the analysis prompt with safety guardrails and a JSON schema."""


def patient_summary(profile, symptoms, context):
    return (
        f"Age: {profile['age']} ({profile['age_group']}), Sex: {profile['sex']}\n"
        f"Symptoms: {', '.join(symptoms)}\n"
        f"Duration: {context['duration']}\n"
        f"Severity: {context['severity']}\n"
        f"Medical history: {context['history']}\n"
        f"Current medication: {context['medication']}\n"
        f"Allergies: {context['allergies']}\n"
        f"Additional information: {context['additional']}"
    )


def build_analysis_prompt(profile, symptoms, context):
    return (
        "Give a preliminary, educational analysis of these symptoms.\n"
        "Rules: this is not a diagnosis; list possible conditions only with their likelihood; "
        "mention uncertainty; do not name prescription drugs or doses; respect the allergies; "
        "say clearly when the person should see a doctor.\n\n"
        f"{patient_summary(profile, symptoms, context)}\n\n"
        "Return JSON:\n"
        '{"possible_conditions": [{"condition": "...", "likelihood": "High/Medium/Low", '
        '"reasoning": "one sentence linking it to the symptoms"}],\n'
        ' "self_care": ["tip 1", "tip 2", "tip 3"],\n'
        ' "see_doctor_if": ["warning sign 1", "warning sign 2", "warning sign 3"],\n'
        ' "recommended_specialist": "short name only, e.g. General Physician"}\n'
        "Give 3-4 possible conditions, most likely first. Write each self-care tip and each "
        "warning sign as its own short item."
    )


def build_question_prompt(profile, symptoms, context):
    return (
        "A doctor would ask follow-up questions to understand these symptoms better. Write 5 "
        "short, specific follow-up questions about information that is missing below.\n\n"
        f"{patient_summary(profile, symptoms, context)}\n\n"
        'Return JSON: {"questions": ["..."]}'
    )
