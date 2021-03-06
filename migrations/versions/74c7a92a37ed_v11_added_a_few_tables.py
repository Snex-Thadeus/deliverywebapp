"""v11 added a few tables

Revision ID: 74c7a92a37ed
Revises: 7b91d042f109
Create Date: 2020-07-31 04:01:34.770144

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '74c7a92a37ed'
down_revision = '7b91d042f109'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('production_activities_tb',
    sa.Column('ID', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('Activity', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('ID')
    )
    op.create_table('item_uom_tb',
    sa.Column('ID', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('MaterialItemsTbID', sa.Integer(), nullable=False),
    sa.Column('UnitOfMeasureTbID', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['MaterialItemsTbID'], ['material_items_tb.ID'], ),
    sa.ForeignKeyConstraint(['UnitOfMeasureTbID'], ['unit_of_measure_tb.ID'], ),
    sa.PrimaryKeyConstraint('ID')
    )
    op.create_table('conversion_factor_tb',
    sa.Column('ID', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('MaterialItemsTbID', sa.Integer(), nullable=False),
    sa.Column('ItemUomTbID', sa.Integer(), nullable=False),
    sa.Column('MeasurementDescription', sa.String(length=50), nullable=False),
    sa.Column('DescribeQuantity', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['ItemUomTbID'], ['item_uom_tb.ID'], ),
    sa.ForeignKeyConstraint(['MaterialItemsTbID'], ['material_items_tb.ID'], ),
    sa.PrimaryKeyConstraint('ID')
    )
    op.create_table('update_material_quantities_tb',
    sa.Column('ID', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('ItemUomTbID', sa.Integer(), nullable=False),
    sa.Column('ReceivedDate', sa.String(length=20), nullable=False),
    sa.Column('Quantity', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['ItemUomTbID'], ['item_uom_tb.ID'], ),
    sa.PrimaryKeyConstraint('ID')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('update_material_quantities_tb')
    op.drop_table('conversion_factor_tb')
    op.drop_table('item_uom_tb')
    op.drop_table('production_activities_tb')
    # ### end Alembic commands ###
