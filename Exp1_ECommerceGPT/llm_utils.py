"""Shared helpers for talking to the local Ollama model."""
import ollama

# qwen2.5:0.5b (from the sample code) gave wrong answers in testing, so the
# slightly larger qwen2.5:1.5b from the same family is used.
MODEL = "qwen2.5:1.5b"

client = ollama.Client()


def ask_llm(system_prompt, user_prompt, temperature=0.3):
    """Send one system + user message to Ollama and return the reply text."""
    response = client.chat(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        options={"temperature": temperature},
    )
    return response["message"]["content"].strip()
