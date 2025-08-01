"""empty message

Revision ID: 2c70b1033d4b
Revises: 11d6e28f75fa
Create Date: 2025-08-01 13:47:54.028455

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "2c70b1033d4b"
down_revision: Union[str, Sequence[str], None] = "11d6e28f75fa"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("bookings", sa.Column("user_id", sa.Integer(), nullable=False))
    op.create_foreign_key(None, "bookings", "users", ["user_id"], ["id"])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(None, "bookings", type_="foreignkey")
    op.drop_column("bookings", "user_id")
