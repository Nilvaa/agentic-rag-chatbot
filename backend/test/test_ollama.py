import ollama

response = ollama.chat(
    model="llama3.1:8b",
    messages=[
        {
            "role": "user",
            "content": "What is human rights?"
        }
    ]
)

print(response["message"]["content"])