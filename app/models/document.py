from sqlalchemy import ForeignKey, Identity, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from pgvector.sqlalchemy import Vector

from app.db.database import Base


class Document(Base):
    __tablename__ = "documents"

    id: Mapped[int] = mapped_column(
        Identity(),
        primary_key=True
    )

    title: Mapped[str] = mapped_column(
        String(500),
        nullable=False
    )

    content: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )


class DocumentChunk(Base):
    __tablename__ = "document_chunks"

    id: Mapped[int] = mapped_column(
        Identity(),
        primary_key=True
    )

    document_id: Mapped[int] = mapped_column(
        ForeignKey("documents.id"),
        nullable=False
    )

    content: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    embedding: Mapped[list[float]] = mapped_column(
        Vector(384),
        nullable=False
    )