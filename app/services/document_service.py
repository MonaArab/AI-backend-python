from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.services.embedding_service import EmbeddingService
from app.models.document import *
import re

'''
it is ald method that chunk text based on characters. chunk_size is the count of characters
def chunk_text(text: str, chunk_size: int = 1000):
    """Split text into non-empty chunks suitable for embedding."""
    return [
        text[index : index + chunk_size]
        for index in range(0, len(text), chunk_size)
        if text[index : index + chunk_size].strip()
    ]

This method chunk text based on words it has a problem that can still cut a sentence in the middle.


def chunk_text_dep(
    text: str,
    chunk_size: int = 50,
    overlap: int = 20
) -> list[str]:
    
    #Split based on spaces. It automatically ignores extra spaces
    words = text.split()

    chunks = []
    start = 0

    while start < len(words):
        end = start + chunk_size

        chunk_words = words[start:end]
        chunk = " ".join(chunk_words)

        chunks.append(chunk)

        start += chunk_size - overlap

    return chunks

'''
def chunk_text(
    text: str,
    max_words: int = 120,
    overlap_sentences: int = 1
) -> list[str]:
    '''
    sentence-aware chunking with a maximum word count
    (?<=[.!?])   → position after . or ! or ? +  → one or more whitespace characters
    max_words is a target maximum, while preserving sentence boundaries is more important.
    re stands for regular expressions. Regular expressions are patterns used to search, split, validate, or replace text.
    re.split() is similar to normal Python split(), but instead of splitting on one fixed string, it can split using a pattern.
    '''
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())

    chunks = []
    current_sentences = []
    current_word_count = 0

    for sentence in sentences:

        sentence_words = sentence.split()
        sentence_word_count = len(sentence_words)

        if (
            current_sentences
            and current_word_count + sentence_word_count > max_words
        ):
            chunks.append(" ".join(current_sentences))
            #we preserve the last sentence of the previous chunk
            overlap = current_sentences[-overlap_sentences:]
            current_sentences = overlap.copy()

            current_word_count =  sum(
                len(s.split())
                for s in current_sentences
            )

        current_sentences.append(sentence)
        current_word_count += sentence_word_count

    if current_sentences:
        chunks.append(" ".join(current_sentences))

    return chunks

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
