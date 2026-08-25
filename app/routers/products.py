from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.product import *
from app.services.embedding_service import EmbeddingService
from app.services.product_service import ProductService

router = APIRouter(
    prefix="/products", # HTTP routing
    tags=["Products"]   #API documentation grouping
)

embedding_service = EmbeddingService()

# Dependency injection
def get_product_service(
    db: Session = Depends(get_db)
) -> ProductService:
    return ProductService(
        db=db,
        embedding_service=embedding_service
    )


@router.post("", response_model=ProductResponse)
def create_product(
    product: ProductCreate,
    service: ProductService = Depends(get_product_service)
):
    return service.create_product(product)

# GET /products
@router.get("", response_model=list[ProductResponse])
def get_products(
    service: ProductService = Depends(get_product_service)
):
    return service.get_products()


# GET /products/123
@router.get("/{product_id}", response_model=ProductResponse)
def get_product(
    product_id: int,
    service: ProductService = Depends(get_product_service)
):
    product = service.get_product(product_id)

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    return product

@router.put("/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int,
    product: ProductUpdate,
    service: ProductService = Depends(get_product_service)
):
    updated_product = service.update_product(
        product_id,
        product
    )

    if updated_product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    return updated_product

@router.delete("/{product_id}", status_code=204)
def delete_product(
    product_id: int,
    service: ProductService = Depends(get_product_service)
):
    deleted = service.delete_product(product_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )


@router.patch("/{product_id}", response_model=ProductResponse)
def patch_product(
    product_id: int,
    product: ProductPatch,
    service: ProductService = Depends(get_product_service)
):
    updated_product = service.patch_product(
        product_id,
        product
    )

    if updated_product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    return updated_product

@router.get("/search/semantic", response_model=list[SemanticSearchResponse])
def semantic_search(
    query: str,
    limit: int = 5,
    min_similarity: float = 0.60,
    service: ProductService = Depends(get_product_service)
):
    return service.semantic_search(
        query=query,
        limit=limit,
        min_similarity=min_similarity
    )
