from app.services.document_service import DocumentService
from app.services.llm_service import LLMService


class RagService:
    def __init__(self, document_service: DocumentService, llm_service: LLMService):
        self.document_service = document_service
        self.llm_service = llm_service

    def answer(self, question: str):
        search_results = self.document_service.search_chunks(query=question, limit=5)
        context_parts = []

        for result in search_results:
            chunk = result["chunk"]

            context_parts.append(
                f"[Document {chunk.document_id}, Chunk {chunk.id}]\n{chunk.content}"
            )

        context = "\n\n".join(context_parts)
        answer = self.llm_service.generate_answer(question=question, context=context)
        sources = [
            {
                "chunk_id": result["chunk"].id,
                "document_id": result["chunk"].document_id,
                "content": result["chunk"].content,
                "similarity": result["similarity"]
            }
        for result in search_results
        ]

        return {
            "answer": answer,
            "sources": sources
        }
