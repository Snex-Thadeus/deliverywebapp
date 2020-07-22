"""first update

Revision ID: 4e600f5ea5ba
Revises: 
Create Date: 2020-07-14 09:45:00.578689

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4e600f5ea5ba'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('customer_tb',
    sa.Column('ID', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('FirstName', sa.String(length=50), nullable=False),
    sa.Column('LastName', sa.String(length=50), nullable=True),
    sa.Column('ContactPerson', sa.String(length=50), nullable=True),
    sa.Column('Type', sa.String(length=50), nullable=False),
    sa.Column('Email', sa.String(length=50), nullable=True),
    sa.Column('PhoneNumber', sa.String(length=50), nullable=False),
    sa.Column('PhoneNumber2', sa.String(length=50), nullable=True),
    sa.Column('PhoneNumber3', sa.String(length=50), nullable=True),
    sa.Column('Area', sa.String(length=50), nullable=False),
    sa.Column('Location', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('ID')
    )
    op.create_table('expense_categories_tb',
    sa.Column('ID', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('CategoryDescription', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('ID')
    )
    op.create_table('meterial_items_tb',
    sa.Column('ID', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('Description', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('ID')
    )
    op.create_table('order_tb',
    sa.Column('OrderNo', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('CustomerName', sa.String(length=150), nullable=False),
    sa.Column('TelephoneNo', sa.String(length=50), nullable=False),
    sa.Column('DeliveryMethod', sa.String(length=50), nullable=False),
    sa.Column('Location', sa.String(length=50), nullable=False),
    sa.Column('OrderDate', sa.String(length=50), nullable=False),
    sa.Column('LPONo', sa.String(length=50), nullable=False),
    sa.Column('Product', sa.String(length=50), nullable=False),
    sa.Column('Price', sa.String(length=50), nullable=False),
    sa.Column('Quantity', sa.String(length=50), nullable=False),
    sa.Column('TotalAmount', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('OrderNo')
    )
    op.create_table('organization_tb',
    sa.Column('ID', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('Name', sa.String(length=150), nullable=False),
    sa.Column('TelephoneNo', sa.String(length=150), nullable=False),
    sa.Column('Email', sa.String(length=150), nullable=False),
    sa.Column('PinNumber', sa.String(length=150), nullable=False),
    sa.Column('PostalAddress', sa.String(length=150), nullable=False),
    sa.PrimaryKeyConstraint('ID')
    )
    op.create_table('petty_cash_tb',
    sa.Column('ID', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('AmountReceived', sa.String(length=50), nullable=False),
    sa.Column('DateReceived', sa.String(length=50), nullable=False),
    sa.Column('ReceivedFrom', sa.String(length=50), nullable=False),
    sa.Column('Account', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('ID')
    )
    op.create_table('product_price_tb',
    sa.Column('ID', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('Description', sa.String(length=50), nullable=False),
    sa.Column('Category', sa.String(length=50), nullable=False),
    sa.Column('Method', sa.String(length=50), nullable=False),
    sa.Column('Price', sa.Float(precision=0.2), nullable=False),
    sa.PrimaryKeyConstraint('ID')
    )
    op.create_table('product_tb',
    sa.Column('ID', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('SKUNumber', sa.String(length=50), nullable=False),
    sa.Column('Description', sa.String(length=150), nullable=False),
    sa.PrimaryKeyConstraint('ID')
    )
    op.create_table('supplier_tb',
    sa.Column('ID', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('SupplierName', sa.String(length=50), nullable=False),
    sa.Column('Email', sa.String(length=50), nullable=False),
    sa.Column('TelephoneNo', sa.String(length=50), nullable=False),
    sa.Column('Location', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('ID')
    )
    op.create_table('unit_of_measure_tb',
    sa.Column('ID', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('Description', sa.String(length=50), nullable=False),
    sa.Column('ShortDescription', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('ID')
    )
    op.create_table('deliveries_tb',
    sa.Column('ID', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('OrderNo', sa.Integer(), nullable=False),
    sa.Column('TotalAmount', sa.String(length=50), nullable=False),
    sa.Column('Invoice_Receipt', sa.String(length=150), nullable=True),
    sa.Column('InvoiceNo_ReceiptNo', sa.String(length=50), nullable=True),
    sa.Column('DeliveredDate', sa.String(length=50), nullable=True),
    sa.Column('PaymentMode', sa.String(length=50), nullable=True),
    sa.Column('ReferenceNo', sa.String(length=50), nullable=True),
    sa.Column('AmountPaid', sa.String(length=50), nullable=True),
    sa.ForeignKeyConstraint(['OrderNo'], ['order_tb.OrderNo'], ),
    sa.PrimaryKeyConstraint('ID')
    )
    op.create_table('user_account_tb',
    sa.Column('ID', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('Name', sa.String(length=50), nullable=False),
    sa.Column('UserName', sa.String(length=50), nullable=False),
    sa.Column('Email', sa.String(length=50), nullable=False),
    sa.Column('PhoneNumber', sa.String(length=50), nullable=False),
    sa.Column('Password', sa.String(length=150), nullable=False),
    sa.Column('OrganizationID', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['OrganizationID'], ['organization_tb.ID'], ),
    sa.PrimaryKeyConstraint('ID')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_account_tb')
    op.drop_table('deliveries_tb')
    op.drop_table('unit_of_measure_tb')
    op.drop_table('supplier_tb')
    op.drop_table('product_tb')
    op.drop_table('product_price_tb')
    op.drop_table('petty_cash_tb')
    op.drop_table('organization_tb')
    op.drop_table('order_tb')
    op.drop_table('meterial_items_tb')
    op.drop_table('expense_categories_tb')
    op.drop_table('customer_tb')
    # ### end Alembic commands ###
