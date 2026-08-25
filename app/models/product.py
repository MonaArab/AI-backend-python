from sqlalchemy import Float, Identity, String
from sqlalchemy.orm import Mapped, mapped_column
from pgvector.sqlalchemy import Vector

from app.db.database import Base


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(
        Identity(),
        primary_key=True
    )

    name: Mapped[str] = mapped_column(
        String(200),
        nullable=False
    )

    manufacturer: Mapped[str | None] = mapped_column(
        String(200),
        nullable=True
    )

    price: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )

    stock: Mapped[int] = mapped_column(
        default=0,
        nullable=False
    )
#Vector(384) means the database column accepts list[float] with size 384
    embedding: Mapped[list[float] | None] = mapped_column(
        Vector(384),
        nullable=True
    )

    description: Mapped[str | None] = mapped_column(
        String(2000),
        nullable=True
    )
