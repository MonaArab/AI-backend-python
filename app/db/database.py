from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

#database://username:password@host/database
DATABASE_URL = "postgresql://ai_user:ai@localhost/ai_backend"

#SQLAlchemy Engine
#      │
#      ├── database dialect
#      ├── connection configuration
#      └── connection pool
#             │
#             ├── DB connection
              
engine = create_engine(DATABASE_URL)


SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)

#Our database models will inherit from it:
#class Product(Base):
class Base(DeclarativeBase):
    pass

#yield is a Python language feature.
#It is similar to return, but the function is paused rather than completely finished.
def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
