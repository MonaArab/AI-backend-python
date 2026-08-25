"""change embedding dimension to 384

Revision ID: 2c2cc4274286
Revises: de6583eaa116
Create Date: 2026-08-24 10:13:11.273892

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import pgvector


# revision identifiers, used by Alembic.
revision: str = '2c2cc4274286'
down_revision: Union[str, Sequence[str], None] = 'de6583eaa116'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_column(
        "products",
        "embedding"
    )

    op.add_column(
        "products",
        sa.Column(
            "embedding",
            pgvector.sqlalchemy.vector.VECTOR(dim=384),
            nullable=True
        )
    )
