"""Add emplpoyee table

Revision ID: 4b764d30002d
Revises: 
Create Date: 2020-01-04 16:55:34.543585

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "4b764d30002d"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "employee",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("division", sa.String(), nullable=False),
        sa.Column("salary", sa.Float(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_employee_division"), "employee", ["division"], unique=False
    )
    op.create_index(op.f("ix_employee_name"), "employee", ["name"], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_employee_name"), table_name="employee")
    op.drop_index(op.f("ix_employee_division"), table_name="employee")
    op.drop_table("employee")
    # ### end Alembic commands ###
