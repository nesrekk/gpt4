import ollama

# Initialize Ollama client
client = ollama.Client()

# Specify the model
model = "qwen2.5:0.5b"

# Example user query
user_input = input("Ask something: ")

# Send the user query to Qwen
response = client.chat(
    model=model,
    messages=[
        {"role": "system", "content": "You are a helpful assistant for e-commerce."},
        {"role": "user", "content": user_input},
    ],
)

# Display Qwen's response
print("\n Qwen says:\n", response["message"]["content"])
