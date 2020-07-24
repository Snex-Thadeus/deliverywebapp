from datetime import datetime
from flask_login import UserMixin
from deliverywebapp import login_manager
from deliverywebapp import db, ma


class OrganizationTb(db.Model):
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Name = db.Column(db.String(150), nullable=False)
    TelephoneNo = db.Column(db.String(150), nullable=False)
    Email = db.Column(db.String(150), nullable=False)
    PinNumber = db.Column(db.String(150), nullable=False)
    PostalAddress = db.Column(db.String(150), nullable=False)

    def __repr__(self):
        pass

    def __init__(self, Name, TelephoneNo, Email, PinNumber, PostalAddress):
        self.Name = Name
        self.TelephoneNo = TelephoneNo
        self.Email = Email
        self.PinNumber = PinNumber
        self.PostalAddress = PostalAddress


@login_manager.user_loader
def load_user(user_id):
    return UserAccountTb.query.get(int(user_id))


class UserAccountTb(db.Model,UserMixin):
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Name = db.Column(db.String(50), nullable=False)
    UserName = db.Column(db.String(50), nullable=False)
    Email = db.Column(db.String(50), nullable=False)
    PhoneNumber = db.Column(db.String(50), nullable=False)
    Password = db.Column(db.String(150), nullable=False)
    OrganizationID = db.Column(db.Integer, db.ForeignKey("organization_tb.ID"), nullable=False)

    def __repr__(self):
        pass

    def __init__(self, Name, UserName, Email, PhoneNumber, Password, OrganizationID):
        self.Name = Name
        self.UserName = UserName
        self.Email = Email
        self.PhoneNumber = PhoneNumber
        self.Password = Password
        self.OrganizationID = OrganizationID


class ProductTb(db.Model):
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    SKUNumber = db.Column(db.String(50), nullable=False)
    Description = db.Column(db.String(150), nullable=False)

    def __repr__(self):
        pass

    def __init__(self, SKUNumber, Description):
        self.SKUNumber = SKUNumber
        self.Description = Description


class ProductTbDropDownSchema(ma.Schema):
    class Meta:
        fields = ("ID", "Description", "Price")


class ProductPriceTb(db.Model):
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ProductTbID = db.Column(db.Integer, db.ForeignKey('product_tb.ID'), nullable=False)
    Category = db.Column(db.String(50), nullable=False)
    Method = db.Column(db.String(50), nullable=False)
    Price = db.Column(db.Float(.2), nullable=False)

    def __repr__(self):
        pass

    def __init__(self, ProductTbID, Category, Method, Price):
        self.ProductTbID = ProductTbID
        self.Category = Category
        self.Method = Method
        self.Price = Price


class AreasTb(db.Model):
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Name = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        pass

    def __init__(self, Name):
        self.Name = Name


class AreaTbDropDownSchema(ma.Schema):
    class Meta:
        fields = ("ID", "Name")


class CustomerTb(db.Model):
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    FirstName = db.Column(db.String(50), nullable=False)
    LastName = db.Column(db.String(50), nullable=True)
    ContactPerson = db.Column(db.String(50), nullable=True)
    Type = db.Column(db.String(50), nullable=False)
    Email = db.Column(db.String(50), nullable=True)
    PhoneNumber = db.Column(db.String(50), nullable=False)
    PhoneNumber2 = db.Column(db.String(50), nullable=True)
    PhoneNumber3 = db.Column(db.String(50), nullable=True)
    AreaID = db.Column(db.Integer, db.ForeignKey('areas_tb.ID'), nullable=False)
    Location = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        pass

    def __init__(self, FirstName, LastName, ContactPerson, Type, Email,
                 PhoneNumber, PhoneNumber2, PhoneNumber3, AreaID, Location):
        self.FirstName = FirstName
        self.LastName = LastName
        self.ContactPerson = ContactPerson
        self.Type = Type
        self.Email = Email
        self.PhoneNumber = PhoneNumber
        self.PhoneNumber2 = PhoneNumber2
        self.PhoneNumber3 = PhoneNumber3
        self.AreaID = AreaID
        self.Location = Location


class CustomerSchema(ma.Schema):
    class Meta:
        fields = ("FirstName", "LastName", "ContactPerson", 'Type', "Email", "PhoneNumber", "AreaID", "Location")


class OrderTb(db.Model):
    OrderNo = db.Column(db.Integer, primary_key=True, autoincrement=True)
    CustomerName = db.Column(db.String(150), nullable=False)
    TelephoneNo = db.Column(db.String(50), nullable=False)
    DeliveryMethod = db.Column(db.String(50), nullable=False)
    Location = db.Column(db.String(50), nullable=False)
    OrderDate = db.Column(db.Date, default=datetime.now(), nullable=False, )
    LPONo = db.Column(db.String(50), nullable=False)
    ProductID = db.Column(db.Integer, db.ForeignKey('product_tb.ID'), nullable=False)
    Price = db.Column(db.String(50), nullable=False)
    Quantity = db.Column(db.String(50), nullable=False)
    TotalAmount = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        pass

    def __init__(self, CustomerName, TelephoneNo, DeliveryMethod,
                 Location, OrderDate, LPONo, ProductID, Price, Quantity, TotalAmount):
        self.CustomerName = CustomerName
        self.TelephoneNo = TelephoneNo
        self.DeliveryMethod = DeliveryMethod
        self.Location = Location
        self.OrderDate = OrderDate
        self.LPONo = LPONo
        self.ProductID = ProductID
        self.Price = Price
        self.Quantity = Quantity
        self.TotalAmount = TotalAmount


class DeliveriesTb(db.Model):
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    OrderNo = db.Column(db.Integer, db.ForeignKey("order_tb.OrderNo"), nullable=False)
    TotalAmount = db.Column(db.String(50), nullable=False)
    Invoice_Receipt = db.Column(db.String(150), nullable=True)
    InvoiceNo_ReceiptNo = db.Column(db.String(50), nullable=True)
    DeliveredDate = db.Column(db.String(50), nullable=True)
    PaymentMode = db.Column(db.String(50), nullable=True)
    ReferenceNo = db.Column(db.String(50), nullable=True)
    AmountPaid = db.Column(db.String(50), nullable=True)

    def __repr__(self):
        pass

    def __init__(self, OrderNo, TotalAmount, Invoice_Receipt, InvoiceNo_ReceiptNo,
                 DeliveredDate, PaymentMode, ReferenceNo, AmountPaid):
        self.OrderNo = OrderNo
        self.TotalAmount = TotalAmount
        self.Invoice_Receipt = Invoice_Receipt
        self.InvoiceNo_ReceiptNo = InvoiceNo_ReceiptNo
        self.DeliveredDate = DeliveredDate
        self.PaymentMode = PaymentMode
        self.ReferenceNo = ReferenceNo
        self.AmountPaid = AmountPaid


class MeterialItemsTb(db.Model):
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Description = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        pass

    def __init__(self, Description):
        self.Description = Description


class UnitOfMeasureTb(db.Model):
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Description = db.Column(db.String(50), nullable=False)
    ShortDescription = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        pass

    def __init__(self, Description, ShortDescription):
        self.Description = Description
        self.ShortDescription = ShortDescription


# Expenses/Purchases
class ExpenseCategoriesTb(db.Model):
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    CategoryDescription = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        pass

    def __init__(self, CategoryDescription):
        self.CategoryDescription = CategoryDescription


class PettyCashTb(db.Model):
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    AmountReceived = db.Column(db.String(50), nullable=False)
    DateReceived = db.Column(db.String(50), nullable=False)
    ReceivedFrom = db.Column(db.String(50), nullable=False)
    Account = db.Column(db.String(50), nullable=False, default="Petty Cash")

    def __repr__(self):
        pass

    def __init__(self, AmountReceived, DateReceived, ReceivedFrom, Account):
        self.AmountReceived = AmountReceived
        self.DateReceived = DateReceived
        self.ReceivedFrom = ReceivedFrom
        self.Account = Account


# class ExpensesTB(db.Model):
#     pass

class SupplierTb(db.Model):
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    SupplierName = db.Column(db.String(50), nullable=False)
    Email = db.Column(db.String(50), nullable=False)
    TelephoneNo = db.Column(db.String(50), nullable=False)
    Location = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        pass

    def __init__(self, SupplierName, Email, TelephoneNo, Location):
        self.SupplierName = SupplierName,
        self.Email = Email
        self.TelephoneNo = TelephoneNo
        self.Location = Location


# V4
class BillTb(db.Model):
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Name = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        pass

    def __init__(self, Name):
        self.Name = Name


# v8
# class ItemIomTb(db.Model):
#     ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     MaterialItemsTbID = db.Column(db.Integer, db.ForeignKey("material_items_tb.ID"), nullable=False)
#     UnitOfMeasureTbID = db.Column(db.Integer, db.ForeignKey("unit_of_measure_tb.ID"), nullable=False)
#
#     def __repr__(self):
#         pass
#
#     def __init__(self, MaterialItemsTbID, UnitOfMeasureTbID):
#         self.MaterialItemsTbID = MaterialItemsTbID
#         self.UnitOfMeasureTbID = UnitOfMeasureTbID
#
#
# class ConversionFactorTb(db.Model):
#     ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     MaterialItemsTbID = db.Column(db.Integer, db.ForeignKey("material_items_tb.ID"), nullable=False)
#     ItemIomTbID = db.Column(db.Integer, db.ForeignKey("item_iom_tb_id.ID"), nullable=False)
#     MeasurementDescription = db.Column(db.String(50), nullable=False)
#     DescribeQuantity = db.Column(db.Integer, nullable=False)
#
#     def __repr__(self):
#         pass
#
#     def __init__(self, MaterialItemsTbID, ItemIomTbID, MeasurementDescription, DescribeQuantity):
#         self.MaterialItemsTbID = MaterialItemsTbID
#         self.ItemIomTbID = ItemIomTbID
#         self.MeasurementDescription = MeasurementDescription
#         self.DescribeQuantity = DescribeQuantity
#
#
# class ProductionActivitiesTb(db.Model):
#     ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     Activity = db.Column(db.String(50), nullable=False)
#
#     def __init__(self, Activity):
#         self.Activity = Activity
#
#
# class UpdateMaterialQuantitiesTb(db.Model):
#     ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     ItemIomTbID = db.Column(db.Integer, db.ForeignKey("item_iom_tb_id.ID"), nullable=False)
#     ReceivedDate = db.Column(db.String(20), nullable=False)
#     Quantity = db.Column(db.Integer, nullable=False)
#
#     def __init__(self, ItemIomTbID, ReceivedDate, Quantity):
#         self.ItemIomTbID = ItemIomTbID
#         self.ReceivedDate = ReceivedDate
#         self.Quantity = Quantity
#
#
# class ViewQuantityBalancesTb(db.Model):
#     ID = db.Column(db.Integer)
#
#
# class UpdateDailyProductionTb(db.Model):
#     ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     DefineProductionActivitiesTbID = db.Column(db.Integer, db.ForeignKey("item_iom_tb_id.ID"), nullable=False)
#     ConversionFactorTbID = db.Column(db.Integer, db.ForeignKey("item_iom_tb_id.ID"), nullable=False)
#     Quantity = db.Column(db.Integer, nullable=False)
#     QuantityUsed = db.Column(db.Float,
#                              nullable=False)  # Populate the Quantity used = Quantity above * Conversion Factor Quantity
#     EntryDate = db.Column(db.Date, nullable=False, default=datetime.now())
#
#     def __init__(self, DefineProductionActivitiesTbID, ConversionFactorTbID, Quantity, QuantityUsed):
#         self.DefineProductionActivitiesTbID = DefineProductionActivitiesTbID
#         self.ConversionFactorTbID = ConversionFactorTbID
#         self.Quantity = Quantity
#         self.QuantityUsed = QuantityUsed
#
#
# # class DailyProductionTb(db.Model):
# #     ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
# #     Activity = db.Column(db.String(50), nullable=False)
# #     Measure = db.Column()
#
# class PackagingMaterialsTb(db.Model):
#     ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     Description = db.Column(db.String(50), nullable=False)
#
#     def __init__(self, Description):
#         self.Description = Description
#
#
# class UpdatePackingMaterialsTb(db.Model):
#     ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     PackagingMaterialsTbID = db.Column(db.Integer, db.ForeignKey("item_iom_tb_id.ID"), nullable=False)
#     Number = db.Column(db.Integer, nullable=False)
#     EntryDate = db.Column(db.Integer, nullable=False)
#
#     def __init__(self, PackagingMaterialsTbID, Number, EntryDate):
#         self.PackagingMaterialsTbID = PackagingMaterialsTbID
#         self.Number = Number
#         self.EntryDate = EntryDate
#
#
# class UpdateFinishedGoodsTb(db.Model):
#     ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     ProductTbID = db.Column(db.Integer, db.ForeignKey(""), nullable=False)
#     PackagingMaterialsTbID = db.Column(db.Integer, db.ForeignKey(""), nullable=False)
#     QuantityUsed = db.Column(db.String(50), nullable=False)
#     EntryDate = db.Column(db.Date, default=datetime.now(), nullable=False)
#
# # class ViewFinishedGoodsBalancesTb(db.Model):
# #     ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
#
# # class ViewPackingMaterialBalancesTb(db.Model):
# #
