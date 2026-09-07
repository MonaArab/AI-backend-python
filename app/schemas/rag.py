from pydantic import BaseModel


class RagRequest(BaseModel):
    question: str


class RagSource(BaseModel):
    chunk_id: int
    document_id: int
    content: str
    similarity: float


class RagResponse(BaseModel):
    answer: str
    sources: list[RagSource]