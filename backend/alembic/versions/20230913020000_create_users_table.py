"""Create users table"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "20230913020000"
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        "users",
        sa.Column("id", sa.Integer, primary_key=True, index=True),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False, unique=True, index=True),
        sa.Column("hashed_password", sa.String(length=255), nullable=False),
    )

def downgrade():
    op.drop_table("users")
