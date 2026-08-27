from fastapi import FastAPI

from app.db.database import Base, engine

#We're not directly using Product. Why import it?
#Because SQLAlchemy needs the model class to be loaded before:
from app.models.product import Product

from app.routers.products import router as products_router
from app.routers.documents import router as documents_router

#looks at all registered SQLAlchemy models and creates missing tables.
#remove beacuse use alembic to manage databse
#Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI Backend",
    version="1.0.0"
)

#Without it, FastAPI doesn't know about your product endpoints.
app.include_router(products_router)
app.include_router(documents_router)


@app.get("/health")
def health():
    return {"status": "ok"}
