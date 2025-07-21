"""В таблице users сделал поле email уникальным

Revision ID: fafbf3f4be14
Revises: 559022fc1d77
Create Date: 2025-07-21 16:52:51.571760

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "fafbf3f4be14"
down_revision: Union[str, Sequence[str], None] = "559022fc1d77"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_unique_constraint(None, "users", ["email"])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(None, "users", type_="unique")
