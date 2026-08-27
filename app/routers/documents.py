from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.document import *
from app.models.document import *
from app.services.embedding_service import EmbeddingService
from app.services.document_service import DocumentService

router = APIRouter(
    prefix="/documents", # HTTP routing
    tags=["Documents"]   #API documentation grouping
)

embedding_service = EmbeddingService()

# Dependency injection
def get_document_service(
    db: Session = Depends(get_db)
) -> DocumentService:
    return DocumentService(
        db=db,
        embedding_service=embedding_service
    )


@router.post("", response_model=DocumentResponse)
def create_document(
    document: DocumentCreate,
    service: DocumentService = Depends(get_document_service)
):
    return service.create_document(document.title, document.text)

# GET /documents/123
@router.get("/{document_id}", response_model=DocumentResponse)
def get_product(
    document_id: int,
    service: DocumentService = Depends(get_document_service)
):
    document = service.get_document(document_id)

    if document is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    return document

@router.get("/rag/search", response_model=list[RagSearchResponse])
def search(
    query: str,
    service: DocumentService = Depends(get_document_service)
):
    return service.search_chunks(query=query)