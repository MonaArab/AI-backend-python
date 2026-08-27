from pydantic import BaseModel, ConfigDict, Field


class DocumentCreate(BaseModel):
    title: str
    text: str


class DocumentResponse(BaseModel):
    #build this schema from object attributes.
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    content: str

class DocumentChunkResponse(BaseModel):
    #build this schema from object attributes.
    model_config = ConfigDict(from_attributes=True)
    id: int
    document_id: int
    content: str
    
    
class RagSearchResponse(BaseModel):
    chunk: DocumentChunkResponse
    similarity: float
