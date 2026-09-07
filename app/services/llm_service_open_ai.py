from openai import OpenAI

class LLMService:

    def __init__(self):
        self.client = OpenAI()

    def generate_answer(
        self,
        question: str,
        context: str
    ) -> str:

        prompt = f"""
           You are a support assistant.

           Answer the user's question using only the provided context.

           If the answer cannot be found in the context, say:
           "I do not have enough information to answer this question."

           Context:
           {context}

           Question:
           {question}
        """

        response = self.client.responses.create(
            model="gpt-5.6-luna",
            input=prompt
        )

        return response.output_text


'''
we can define rule ->
prompt = f"""
You are an assistant for internal company information.

Rules:
- Use only the information in CONTEXT.
- Do not use prior knowledge.
- Do not guess.
- Do not add facts that are not explicitly supported by CONTEXT.
- If CONTEXT does not contain the answer, respond exactly:
  "I do not have enough information in the internal documents."

CONTEXT:
{context}

QUESTION:
{question}

ANSWER:
"""
'''    