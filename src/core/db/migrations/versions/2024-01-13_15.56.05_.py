"""empty message

Revision ID: cffc8d26a0c4
Revises: fe9ed9252c2b
Create Date: 2024-01-13 15:56:05.427406

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "cffc8d26a0c4"
down_revision = "fe9ed9252c2b"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint("admin_token_requests_email_key", "admin_token_requests", type_="unique")
    op.create_unique_constraint(None, "external_site_users", ["email"])
    op.alter_column("unsubscribe_reason", "user_id", existing_type=sa.INTEGER(), nullable=False)
    op.drop_constraint("users_id_key", "users", type_="unique")
    op.alter_column("users_categories", "user_id", existing_type=sa.INTEGER(), nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column("users_categories", "user_id", existing_type=sa.INTEGER(), nullable=True)
    op.create_unique_constraint("users_id_key", "users", ["id"])
    op.alter_column("unsubscribe_reason", "user_id", existing_type=sa.INTEGER(), nullable=True)
    op.drop_constraint(None, "external_site_users", type_="unique")
    op.create_unique_constraint("admin_token_requests_email_key", "admin_token_requests", ["email"])
    # ### end Alembic commands ###
