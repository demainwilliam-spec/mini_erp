"""feat: ajout enum OrderStatus

Revision ID: 5076d9514f62
Revises: 29b456c9603c
Create Date: 2026-06-15 19:51:36.114818

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5076d9514f62'
down_revision: Union[str, Sequence[str], None] = '29b456c9603c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("UPDATE orders SET status = LOWER(status)")
    
    orderstatus_enum = sa.Enum('draft', 'confirmed', 'closed', name='orderstatus')
    orderstatus_enum.create(op.get_bind())
    
    op.alter_column('orders', 'status',
        existing_type=sa.VARCHAR(length=20),
        type_=orderstatus_enum,
        existing_nullable=False,
        postgresql_using='status::orderstatus'
    )


def downgrade() -> None:
    op.alter_column('orders', 'status',
        existing_type=sa.Enum('draft', 'confirmed', 'closed', name='orderstatus'),
        type_=sa.VARCHAR(length=20),
        existing_nullable=False
    )
    sa.Enum(name='orderstatus').drop(op.get_bind())
