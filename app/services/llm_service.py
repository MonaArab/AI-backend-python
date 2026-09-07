import httpx


class LLMService:

    def __init__(self):
        self.base_url = "http://localhost:11434"
        self.model = "llama3"

    def generate_answer(
        self,
        question: str,
        context: str
    ) -> str:

        prompt = f"""
You are a support assistant.

Answer the user's question using only the provided context.

If the context does not contain enough information,
say that you do not have enough information.

Context:
{context}

Question:
{question}

Answer:
"""

        response = httpx.post(
            f"{self.base_url}/api/generate",
            json={
                "model": self.model,
                "prompt": prompt,
                "stream": False
            },
            timeout=300.0
        )

        response.raise_for_status()

        data = response.json()

        return data["response"]