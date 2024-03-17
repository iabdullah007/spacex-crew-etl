"""Create SpaceX Crew Table

Revision ID: b0d72d5f16e7
Revises:
Create Date: 2024-03-13 23:50:47.396702

"""
from __future__ import annotations

from collections.abc import Sequence
from enum import Enum as PythonEnum
from typing import Union

import sqlalchemy as sa

from alembic import op


# revision identifiers, used by Alembic.
revision: str = 'b0d72d5f16e7'
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

class CrewStatus(PythonEnum):
    ACTIVE = 'active'
    INACTIVE = 'inactive'
    RETIRED = 'retired'
    UNKNOWN = 'unknown'


def upgrade() -> None:
    op.create_table(
        'crew',
        sa.Column('id', sa.String(), primary_key=True, nullable=True),
        sa.Column('name', sa.String(), nullable=True),
        sa.Column('status', sa.Enum(CrewStatus), nullable=False),
        sa.Column('agency', sa.String(), nullable=True),
        sa.Column('wikipedia', sa.String(), nullable=True),
        sa.Column('launches', sa.ARRAY(sa.String), nullable=False),
    )


def downgrade() -> None:
    pass
