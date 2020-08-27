from datetime import datetime
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from deliverywebapp import db, ma, login_manager, app


class OrganizationTb(db.Model):
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Name = db.Column(db.String(150), nullable=False)
    TelephoneNo = db.Column(db.String(150), nullable=False)
    Email = db.Column(db.String(150), nullable=False)
    PinNumber = db.Column(db.String(150), nullable=False)
    PostalAddress = db.Column(db.String(150), nullable=False)

    def __repr__(self):
        pass

    def __init__(self, name, telephone_no, email, pin_number, postal_address):
        self.Name = name
        self.TelephoneNo = telephone_no
        self.Email = email
        self.PinNumber = pin_number
        self.PostalAddress = postal_address


@login_manager.user_loader
def load_user(user_id):
    return UserAccountTb.query.get(int(user_id))


class UserAccountTb(db.Model, UserMixin):
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Name = db.Column(db.String(50), nullable=False)
    UserName = db.Column(db.String(50), nullable=False)
    Email = db.Column(db.String(50), nullable=False)
    PhoneNumber = db.Column(db.String(50), nullable=False)
    Password = db.Column(db.String(150), nullable=False)
    OrganizationID = db.Column(db.Integer, db.ForeignKey("organization_tb.ID"), nullable=False)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return UserAccountTb.query.get(user_id)

    def __repr__(self):
        pass

    def __init__(self, name, user_name, email, phone_number, password, organization_id):
        self.Name = name
        self.UserName = user_name
        self.Email = email
        self.PhoneNumber = phone_number
        self.Password = password
        self.OrganizationID = organization_id


class ProductTb(db.Model):
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    SKUNumber = db.Column(db.String(50), nullable=False)
    Description = db.Column(db.String(150), nullable=False)

    def __repr__(self):
        pass

    def __init__(self, sku_number, description):
        self.SKUNumber = sku_number
        self.Description = description


class ProductTbDropDownSchema(ma.Schema):
    class Meta:
        fields = ("ID", "Description", "Price")


class ProductPriceTb(db.Model):
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ProductTbID = db.Column(db.Integer, db.ForeignKey('product_tb.ID'), nullable=False)
    Category = db.Column(db.String(50), nullable=False)
    Method = db.Column(db.String(50), nullable=False)
    Price = db.Column(db.Float(20), nullable=False)

    def __repr__(self):
        pass

    def __init__(self, product_tb_id, category, method, price):
        self.ProductTbID = product_tb_id
        self.Category = category
        self.Method = method
        self.Price = price


class ProductPriceTbDropDownSchema(ma.Schema):
    class Meta:
        fields = ("ID", "ProductTbID", "Category", "Method", "Price")


class AreasTb(db.Model):
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Name = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        pass

    def __init__(self, name):
        self.Name = name


class AreaTbDropDownSchema(ma.Schema):
    class Meta:
        fields = ("ID", "Name")


class CustomerTb(db.Model):
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    FirstName = db.Column(db.String(50), nullable=False)
    LastName = db.Column(db.String(50), nullable=True)
    ContactPerson = db.Column(db.String(50), nullable=True, default='N/A')
    Type = db.Column(db.String(50), nullable=False)
    Email = db.Column(db.String(50), nullable=True, default='N/A')
    PhoneNumber = db.Column(db.String(50), nullable=False)
    PhoneNumber2 = db.Column(db.String(50), nullable=True)
    PhoneNumber3 = db.Column(db.String(50), nullable=True)
    AreaID = db.Column(db.Integer, db.ForeignKey('areas_tb.ID'), nullable=False)
    Location = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        pass

    def __init__(self, first_name, last_name, contact_person, type, email,
        phone_number, phone_number2, phone_number3, area_id, location):
        self.FirstName = first_name
        self.LastName = last_name
        self.ContactPerson = contact_person
        self.Type = type
        self.Email = email
        self.PhoneNumber = phone_number
        self.PhoneNumber2 = phone_number2
        self.PhoneNumber3 = phone_number3
        self.AreaID = area_id
        self.Location = location


class CustomerSchema(ma.Schema):
    class Meta:
        fields = ("FirstName", "LastName", "ContactPerson", 'Type', "Email", "PhoneNumber", "AreaID", "Location")


class OrdersTb(db.Model):
    OrderNo = db.Column(db.Integer, primary_key=True, autoincrement=True)
    CustomerName = db.Column(db.String(150), nullable=False)
    TelephoneNo = db.Column(db.String(50), nullable=False)
    DeliveryMethod = db.Column(db.String(50), nullable=False)
    Location = db.Column(db.String(50), nullable=False)
    OrderDate = db.Column(db.Date, default=datetime.now(), nullable=False)
    LPONo = db.Column(db.String(50), nullable=True, default='N/A')
    ProductID = db.Column(db.Integer, db.ForeignKey('product_price_tb.ID'), nullable=False)
    Price = db.Column(db.String(50), nullable=False)
    Quantity = db.Column(db.String(50), nullable=False)
    TotalAmount = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        pass

    def __init__(self, customer_name, telephone_no, delivery_method, location, order_date, lpo_no, product_id, price, quantity, total_amount):
        self.CustomerName = customer_name
        self.TelephoneNo = telephone_no
        self.DeliveryMethod = delivery_method
        self.Location = location
        self.OrderDate = order_date
        self.LPONo = lpo_no
        self.ProductID = product_id
        self.Price = price
        self.Quantity = quantity
        self.TotalAmount = total_amount


class DeliveriesTb(db.Model):
    OrderNo = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    Invoice_Receipt = db.Column(db.String(150), nullable=True)
    InvoiceNo_ReceiptNo = db.Column(db.String(50), nullable=True)
    DeliveredDate = db.Column(db.String(50), nullable=True)
    PaymentMode = db.Column(db.String(50), nullable=True)
    ReferenceNo = db.Column(db.String(50), nullable=True)
    AmountPaid = db.Column(db.String(50), nullable=True)

    def __repr__(self):
        pass

    def __init__(self, order_no, invoice_receipt, invoice_no_receipt_no,
                     delivered_date, payment_mode, reference_no, amount_paid):
        self.OrderNo = order_no
        self.Invoice_Receipt = invoice_receipt
        self.InvoiceNo_ReceiptNo = invoice_no_receipt_no
        self.DeliveredDate = delivered_date
        self.PaymentMode = payment_mode
        self.ReferenceNo = reference_no
        self.AmountPaid = amount_paid


class MaterialItemsTb(db.Model):
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Description = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        pass

    def __init__(self, description):
        self.Description = description


class MaterialItemSchema(ma.Schema):
    class Meta:
        fields = ("ID", "Description")


class UnitOfMeasureTb(db.Model):
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Description = db.Column(db.String(50), nullable=False)
    ShortDescription = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        pass

    def __init__(self, description, short_description):
        self.Description = description
        self.ShortDescription = short_description


class UnitOfMeasureSchema(ma.Schema):
    class Meta:
        fields = ("ID", "Description")


class ExpenseCategoriesTb(db.Model):
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    CategoryDescription = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        pass

    def __init__(self, category_description):
        self.CategoryDescription = category_description


class PettyCashTb(db.Model):
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    AmountReceived = db.Column(db.String(50), nullable=False)
    DateReceived = db.Column(db.String(50), nullable=False)
    ReceivedFrom = db.Column(db.String(50), nullable=False)
    Account = db.Column(db.String(50), nullable=False, default="Petty Cash")

    def __repr__(self):
        pass

    def __init__(self, amount_received, date_received, received_from, account):
        self.AmountReceived = amount_received
        self.DateReceived = date_received
        self.ReceivedFrom = received_from
        self.Account = account


class SupplierTb(db.Model):
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Name = db.Column(db.String(50), nullable=False)
    Email = db.Column(db.String(50), nullable=False)
    TelephoneNo = db.Column(db.Integer, nullable=False)
    Location = db.Column(db.String(50), nullable=False)

    def __init__(self, name, email, telephone_no, location):
        self.Name = name
        self.Email = email
        self.TelephoneNo = telephone_no
        self.Location = location


class BillTb(db.Model):
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Name = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        pass

    def __init__(self, Name):
        self.Name = Name


class ItemUomTb(db.Model):
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    MaterialItemsTbID = db.Column(db.Integer, db.ForeignKey("material_items_tb.ID"), nullable=False)
    UnitOfMeasureTbID = db.Column(db.Integer, db.ForeignKey("unit_of_measure_tb.ID"), nullable=False)

    def __repr__(self):
        pass

    def __init__(self, material_items_tb_id, unit_of_measure_tb_id):
        self.MaterialItemsTbID = material_items_tb_id
        self.UnitOfMeasureTbID = unit_of_measure_tb_id


class ItemUomSchema(ma.Schema):
    class Meta:
        fields = ("ID", "MaterialItemsTbID", "UnitOfMeasureTbID")


class ConversionFactorTb(db.Model):
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    MaterialItems = db.Column(db.Integer, db.ForeignKey("material_items_tb.ID"), nullable=False)
    ItemUom = db.Column(db.Integer, db.ForeignKey("unit_of_measure_tb.ID"), nullable=False)
    MeasurementDescription = db.Column(db.String(50), nullable=False)
    DescribeQuantity = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        pass

    def __init__(self, material_items_tb_id, item_uom_tb_id, measurement_description, describe_quantity):
        self.MaterialItemsTbID = material_items_tb_id
        self.ItemUomTbID = item_uom_tb_id
        self.MeasurementDescription = measurement_description
        self.DescribeQuantity = describe_quantity


class ConversionFactorSchema(ma.Schema):
    class Meta:
        fields = ("ID", "MaterialItems", "ItemUom", "MeasurementDescription", "DescribeQuantity")


class ProductionActivitiesTb(db.Model):
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Activity = db.Column(db.String(50), nullable=False)

    def __init__(self, activity):
        self.Activity = activity


class ProductionActivitiesSchema(ma.Schema):
    class Meta:
        fields = ("ID", "Activity")


class UpdateMaterialQuantitiesTb(db.Model):
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ItemUomTbID = db.Column(db.Integer, db.ForeignKey("item_uom_tb.ID"), nullable=False)
    ReceivedDate = db.Column(db.String(20), nullable=False)
    Quantity = db.Column(db.Integer, nullable=False)

    def __init__(self, item_uom_tb_id, received_date, quantity):
        self.ItemUomTbID = item_uom_tb_id
        self.ReceivedDate = received_date
        self.Quantity = quantity


class UpdateDailyProductionTb(db.Model):
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    DefineProductionActivitiesTbID = db.Column(db.Integer, db.ForeignKey("production_activities_tb.ID"), nullable=False)
    ConversionFactorTbID = db.Column(db.Integer, db.ForeignKey("conversion_factor_tb.ID"), nullable=False)
    Quantity = db.Column(db.Integer, nullable=False)
    EntryDate = db.Column(db.Date, default=datetime.now(), nullable=False)

    def __init__(self, define_production_activities_tb_id, conversion_factors_tb_id, quantity, entry_date):
        self.DefineProductionActivitiesTbID = define_production_activities_tb_id
        self.ConversionFactorTbID = conversion_factors_tb_id
        self.Quantity = quantity
        self.EntryDate = entry_date


class DailyProductionTb(db.Model):
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Activity = db.Column(db.String(50), nullable=False)
    Measure = db.Column(db.String(30), nullable=False)
    Quantity = db.Column(db.Integer, primart_key=True, nullable=False)
    Item = db.Column(db.String(20), nullable=False)
    UoM = db.Column(db.String(10), nullable=False)
    ProductionDate = db.Column(db.Date, nullable=False, default=datetime.now())

    def __init__(self, activity, measure, quantity, item, uom, production_date):
        self.Activity = activity
        self.Measure = measure
        self.Quantity = quantity
        self.Item = item
        self.UoM = uom
        self.ProductionDate = production_date


class PackagingMaterialsTb(db.Model):
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Description = db.Column(db.String(50), nullable=False)

    def __init__(self, description):
        self.Description = description


class PackagingMaterialsSchema(ma.Schema):
    class Meta:
        fields = ("ID", "Description")


class UpdatePackagingMaterialsTb(db.Model):
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    PackagingMaterialsTbID = db.Column(db.Integer, db.ForeignKey("packaging_materials_tb.ID"), nullable=False)
    Number = db.Column(db.Integer, nullable=False)
    EntryDate = db.Column(db.Date, default=datetime.now(), nullable=False)

    def __init__(self, packaging_materials_tb_id, number, entry_date):
        self.PackagingMaterialsTbID = packaging_materials_tb_id
        self.Number = number
        self.EntryDate = entry_date


class UpdateFinishedGoodsTb(db.Model):
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ProductTbID = db.Column(db.Integer, db.ForeignKey("product_tb.ID"), nullable=False)
    PackagingMaterialsTbID = db.Column(db.Integer, db.ForeignKey("packaging_materials_tb.ID"), nullable=False)
    QuantityUsed = db.Column(db.String(50), nullable=False)
    EntryDate = db.Column(db.Date, default=datetime.now(), nullable=False)

    def __init__(self, product_tb_id, packaging_materials_tb_id, quantity_used, entry_date):
        self.ProductTbID = product_tb_id
        self.PackagingMaterialsTbID = packaging_materials_tb_id
        self.QuantityUsed = quantity_used
        self.EntryDate = entry_date


class ViewQuantityBalancesTb(db.Model):
    ID = db.Column(db.Integer,  primary_key=True, autoincrement=True)
    Material = db.Column(db.String(50), nullable=False)
    UnitOfMeasure = db.Column(db.String(10), nullable=False)
    Balance = db.Column(db.Integer, nullable=False)

    def __init__(self, material, unit_of_measure, balance):
        self.Material = material
        self.UnitOfMeasure = unit_of_measure
        self.Balance = balance


class ViewFinishedGoodsBalancesTb(db.Model):
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Product = db.Column(db.Integer, db.ForeignKey("product_price_tb.ID"), nullable=False)
    P_In = db.Column(db.Integer, nullable=False)
    Out = db.Column(db.Integer, nullable=False)
    Balance = db.Column(db.Integer, nullable=False)
    Date = db.Column(db.Date, default=datetime.now(), nullable=False)

    def __init__(self, product, p_in, out, balance, date):
        self.Product = product
        self.P_In = p_in
        self.Out = out
        self.Balance = balance
        self.Date = date


class ViewPackingMaterialBalancesTb(db.Model):
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Product = db.Column(db.Integer, db.ForeignKey("packaging_materials_tb.ID"), nullable=False)
    P_In = db.Column(db.Integer, nullable=False)
    Out = db.Column(db.Integer, nullable=False)
    Balance = db.Column(db.Integer, nullable=False)
    Date = db.Column(db.Date, default=datetime.now(), nullable=False)

    def __init__(self, product, p_in, out, balance, date):
        self.Product = product
        self.P_In = p_in
        self.Out = out
        self.Balance = balance
        self.Date = date

