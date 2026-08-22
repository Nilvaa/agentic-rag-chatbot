import ollama

class LLMService:
    def __init__(self):
        self.model="llama3.1:8b"

    def generate_answer(
            self,
            question:str,
            context:str,
            history:str= ""
    ):
        prompt=f"""
You are a helpful assistant that answers questions using the provided
document context and conversation history.

Use ONLY the information provided in the document context to answer
questions about the documents.

The conversation history is provided only to understand references
and follow-up questions.

If the answer cannot be found in the document context, say:
"I could not find the answer in the provided documents."

Do not make up information.

Conversation History:
{history}

Document Context:
{context}

Current Question:
{question}

Answer:
"""
        response=ollama.chat(
            model=self.model,messages=[
                {
                    "role":"user",
                    "content":prompt
                }
            ]
        )
        return response["message"]["content"]