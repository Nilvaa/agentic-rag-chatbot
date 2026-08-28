import ollama


class LLMService:

    def __init__(self):
        self.model = "llama3.1:8b"

    def generate_answer(
        self,
        question: str,
        context: str,
        history: str = "",
        source_type: str = "document"
    ):

        if source_type == "web":

            prompt = f"""
You are a helpful AI assistant.

Your task is to answer ONLY the CURRENT QUESTION.

The answer must be based on the provided WEB SEARCH RESULTS.

IMPORTANT RULES:

1. Answer ONLY the current question.
2. Do NOT answer or discuss previous questions.
3. Do NOT mention previous questions unless the current question
   explicitly refers to them.
4. Conversation history is provided ONLY to understand follow-up
   references such as:
   - "it"
   - "they"
   - "that"
   - "this"
   - "the company"
   - "the person"
5. Do NOT use unrelated information from the conversation history.
6. Use the web search results as the factual source for your answer.
7. Do not make up information.
8. If the web search results do not contain enough information,
   say exactly:

"I could not find enough reliable information."

CONVERSATION HISTORY:
{history}

WEB SEARCH RESULTS:
{context}

CURRENT QUESTION:
{question}

ANSWER:
"""

        else:

            prompt = f"""
You are a helpful document-based AI assistant.

Your task is to answer ONLY the CURRENT QUESTION.

The answer must be based on the provided DOCUMENT CONTEXT.

IMPORTANT RULES:

1. Answer ONLY the current question.
2. Do NOT answer or discuss previous questions.
3. Do NOT mention previous questions unless the current question
   explicitly refers to them.
4. Conversation history is provided ONLY to understand follow-up
   references such as:
   - "it"
   - "they"
   - "that"
   - "this"
   - "the company"
   - "the policy"
5. Do NOT use unrelated information from the conversation history.
6. Use ONLY the provided document context for factual information.
7. Do not make up information.
8. If the answer cannot be found in the document context,
   say exactly:

"I could not find the answer in the provided documents."

CONVERSATION HISTORY:
{history}

DOCUMENT CONTEXT:
{context}

CURRENT QUESTION:
{question}

ANSWER:
"""

        response = ollama.chat(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response["message"]["content"]