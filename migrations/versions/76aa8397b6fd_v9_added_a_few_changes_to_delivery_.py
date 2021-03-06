"""v9 added a few changes to delivery table and meterialtb to material tb

Revision ID: 76aa8397b6fd
Revises: 7171446f8acd
Create Date: 2020-07-27 09:37:48.932234

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '76aa8397b6fd'
down_revision = '7171446f8acd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('material_items_tb',
    sa.Column('ID', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('Description', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('ID')
    )
    op.drop_table('meterial_items_tb')
    op.create_unique_constraint(None, 'deliveries_tb', ['OrderNo'])
    op.drop_constraint('deliveries_tb_ibfk_1', 'deliveries_tb', type_='foreignkey')
    op.drop_column('deliveries_tb', 'TotalAmount')
    op.drop_column('deliveries_tb', 'ID')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('deliveries_tb', sa.Column('ID', mysql.INTEGER(), autoincrement=True, nullable=False))
    op.add_column('deliveries_tb', sa.Column('TotalAmount', mysql.VARCHAR(length=50), nullable=False))
    op.create_foreign_key('deliveries_tb_ibfk_1', 'deliveries_tb', 'order_tb', ['OrderNo'], ['OrderNo'])
    op.drop_constraint(None, 'deliveries_tb', type_='unique')
    op.create_table('meterial_items_tb',
    sa.Column('ID', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('Description', mysql.VARCHAR(length=50), nullable=False),
    sa.PrimaryKeyConstraint('ID'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.drop_table('material_items_tb')
    # ### end Alembic commands ###
