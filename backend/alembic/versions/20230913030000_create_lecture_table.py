# backend/alembic/versions/20230913030000_create_lecture_table.py
"""Create lectures table with foreign key to users.

Revision ID: 20230913030000
Revises: 20230913020000
Create Date: 2023-09-13 03:00:00
"""

from alembic import op
import sqlalchemy as sa
import enum

# revision identifiers, used by Alembic.
revision = "20230913030000"
down_revision = "20230913020000"
branch_labels = None
depends_on = None

class LectureStatus(enum.Enum):
    UPLOADED = "UPLOADED"
    QUEUED = "QUEUED"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

def upgrade():
    op.create_table(
        "lectures",
        sa.Column("id", sa.Integer, primary_key=True, index=True),
        sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("original_filename", sa.String(length=255), nullable=False),
        sa.Column("stored_filename", sa.String(length=255), nullable=False, unique=True),
        sa.Column("file_path", sa.String(length=500), nullable=False),
        sa.Column("file_type", sa.String(length=100), nullable=False),
        sa.Column("file_size", sa.BigInteger, nullable=False),
        sa.Column("status", sa.Enum(LectureStatus), nullable=False, server_default=sa.text("'UPLOADED'")),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now(), nullable=False),
    )

def downgrade():
    op.drop_table("lectures")
