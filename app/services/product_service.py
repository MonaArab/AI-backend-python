from sqlalchemy import select
from sqlalchemy.orm import Session
from app.services.embedding_service import EmbeddingService
from app.models.product import Product
from app.schemas.product import *

class ProductService:

    def __init__(
        self,
        db: Session,
        embedding_service: EmbeddingService
    ):
        self.db = db
        self.embedding_service = embedding_service

    
    def create_product(self, product: ProductCreate) -> Product:
       searchable_text = f"""
       Product: {product.name}
       Manufacturer: {product.manufacturer or ""}
       Description: {product.description or ""}
       """
       embedding = (
          self.embedding_service
          .generate_embedding(searchable_text)
       )
       
       
       try:
          db_product = Product(
              name=product.name,
              manufacturer=product.manufacturer,
              price=product.price,
              stock=product.stock,
              embedding=embedding
          )

          self.db.add(db_product)
          self.db.commit()
          self.db.refresh(db_product)

          return db_product

       except SQLAlchemyError:
          self.db.rollback()
          raise

    def get_products(self) -> list[Product]:
        statement = select(Product)

        return list(
            self.db.scalars(statement).all()
        )


    def get_product(self, product_id: int) -> Product | None:
        statement = (
            select(Product)
            .where(Product.id == product_id)
        )

        return self.db.scalar(statement)

    def update_product(
        self,
        product_id: int,
        product: ProductUpdate
    ) -> Product | None:

        db_product = self.get_product(product_id)

        if db_product is None:
            return None

        db_product.name = product.name
        db_product.manufacturer = product.manufacturer
        db_product.price = product.price
        db_product.stock = product.stock

        self.db.commit()
        self.db.refresh(db_product)

        return db_product
    

    def delete_product(self, product_id: int) -> bool:

        db_product = self.get_product(product_id)

        if db_product is None:
           return False

        self.db.delete(db_product)
        self.db.commit()

        return True

    def patch_product(
        self,
        product_id: int,
        product: ProductUpdate
       ) -> Product | None:

        db_product = self.get_product(product_id)

        if db_product is None:
           return None

        # update only fields explicitly present in the request JSON.
        # JSON: {}   → stock UNSET → excluded
        # JSON: {"stock": null}       → stock SET to None → included
        # JSON: {"stock": 10}         → stock SET to 10 → included
        update_data = product.model_dump(exclude_unset=True)#exclude it if it is not in json

        for field, value in update_data.items():
           setattr(db_product, field, value)

        self.db.commit()
        self.db.refresh(db_product)

        return db_product

    def semantic_search(
        self,
        query: str,
        limit: int = 5,
        min_similarity: float = 0.60
    ):

        query_embedding = (
           self.embedding_service
           .generate_embedding(query)
        )
        distance = Product.embedding.cosine_distance(
           query_embedding
        )
        max_distance = 1 - min_similarity
        # SELECT *
        # FROM products
        # WHERE embedding IS NOT NULL
        # ORDER BY embedding <=> :query_embedding -> <=> means cosine distance
        # LIMIT :limit;
        statement = (
           select(
              Product,
              distance.label("distance")
           )
           .where(Product.embedding.is_not(None))
           .where(distance <= max_distance) # distance≤0.40
           .order_by(distance)
           .limit(limit)# Top-5 nearest-neighbor search
        )

        rows = self.db.execute(statement).all()
        
        return [
           {
            "product": product,
            "similarity": 1 - distance_value
        }
        for product, distance_value in rows
        ]
