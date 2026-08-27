from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.services.embedding_service import EmbeddingService
from app.models.document import *


def chunk_text(text: str, chunk_size: int = 1000):
    """Split text into non-empty chunks suitable for embedding."""
    return [
        text[index : index + chunk_size]
        for index in range(0, len(text), chunk_size)
        if text[index : index + chunk_size].strip()
    ]


class DocumentService:

    def __init__(self, db: Session, embedding_service: EmbeddingService):
        self.db = db
        self.embedding_service = embedding_service

    def create_document(self, title: str, text: str):
        document = Document(title=title, content=text)

        self.db.add(document)
        self.db.flush()

        chunks = chunk_text(text)

        for chunk in chunks:
            embedding = self.embedding_service.generate_embedding(chunk)

            db_chunk = DocumentChunk(
                document_id=document.id, content=chunk, embedding=embedding
            )

            self.db.add(db_chunk)

        self.db.commit()

        return document


    def search_chunks(self, query: str, limit: int = 5):
        query_embedding = self.embedding_service.generate_embedding(query)

        distance = DocumentChunk.embedding.cosine_distance(query_embedding)

        statement = (
           select(DocumentChunk, distance.label("distance"))
           .order_by(distance)
           .limit(limit)
        )

        rows = self.db.execute(statement).all()

        return [
           {
            "chunk": chunk,
            "similarity": 1 - distance_value
           }
           for chunk, distance_value in rows
        ]

    def get_document(self, document_id: int) -> Document | None:
       statement = select(Document).where(Document.id == document_id)

       return self.db.scalar(statement)
