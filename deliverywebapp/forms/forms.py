import phonenumbers as phonenumbers
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, IntegerField
from wtforms.validators import DataRequired, Email, ValidationError, Optional, EqualTo

from deliverywebapp.models.models import UserAccountTb

CUSTOMER_TYPE = ['Hotel', 'Individual', 'Restaurant', 'School', 'Camp',
                 'Institution']


class LoginForm(FlaskForm):
    email = StringField('Email address', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')


class DefineAreasForm(FlaskForm):
    area = StringField('Area', validators=[DataRequired()])
    submit = SubmitField('Submit')


class DefineOrdersForm(FlaskForm):
    # search with CustomerName/Phone Number (any of the phone numbers
    customer = StringField('Customer', id="autocomplete", validators=[DataRequired()])
    # when the above customer is selected, populate the customer location
    location = StringField('Location', id="location", render_kw={'readonly': True}, validators=[DataRequired()])
    # pick from calendar (dd/mm/yy). Default value is the system date
    orderdate = StringField('Order Date', validators=[DataRequired()])
    lpoNo = StringField('LPO Number', validators=[Optional()])
    category = SelectField('Category')
    deliveryMethod = SelectField('Delivery Method', validators=[DataRequired()])
    ddProducts = SelectField('Select Product', validators=[DataRequired()])
    price = StringField('Price', render_kw={'readonly': True}, validators=[DataRequired()])
    quantity = StringField('Quantity', validators=[DataRequired()])
    totalAmount = StringField('Total Amount', render_kw={'readonly': True}, validators=[DataRequired()])
    submit = SubmitField('Submit')


class DefineProductsForm(FlaskForm):
    productSKU = StringField('Product SKU', validators=[DataRequired()])
    productDescription = StringField('Product Description', validators=[DataRequired()])
    submit = SubmitField('Submit')


class DefineProductPricesForm(FlaskForm):
    chooseProduct = SelectField('Choose Product', validators=[DataRequired()])
    chooseCategory = SelectField('Choose Category', validators=[DataRequired()])
    chooseMethod = SelectField('Choose Method', validators=[DataRequired()])
    price = StringField('Price', validators=[DataRequired()])
    submit = SubmitField('Submit')


class DefineCustomerDetailsForm(FlaskForm):
    firstname = StringField('Firstname', validators=[DataRequired()])
    lastname = StringField('Lastname', validators=[DataRequired()])
    contactperson = StringField('Contact Person', validators=[Optional()])
    # fetch the list below from db
    customerType = SelectField('Customer Type', validators=[DataRequired()], choices=CUSTOMER_TYPE)
    email = StringField('Email', validators=[Optional(), Email(message='Not a valid email address')])
    phonenumber1 = StringField('Phone 1', validators=[DataRequired()])
    phonenumber2 = StringField('Phone 2', )
    phonenumber3 = StringField('Phone 3', )
    area = SelectField('Area', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    submit = SubmitField('Submit')

    def validate_phone(form, field):
        if len(field.data) > 16:
            raise ValidationError('Invalid phone number.')
        try:
            input_number = phonenumbers.parse(field.data)
            if not (phonenumbers.is_valid_number(input_number)):
                raise ValidationError('Invalid phone number.')
        except:
            input_number = phonenumbers.parse("+254" + field.data)
            if not (phonenumbers.is_valid_number(input_number)):
                raise ValidationError('Invalid phone number.')


class DefineRawMaterialItemsForm(FlaskForm):
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Submit')


class DefineUnitOfMeasureForm(FlaskForm):
    description = StringField('Description', validators=[DataRequired()])
    shortDescription = StringField('Short Description', validators=[DataRequired()])
    submit = SubmitField('Submit')


class DefineExpenseCategoriesForm(FlaskForm):
    categoryDescription = StringField('Category Description', validators=[DataRequired()])
    submit = SubmitField('Submit')


class DefinePettyCashForm(FlaskForm):
    amountReceived = StringField('Amount Received', validators=[DataRequired()])
    dateReceived = StringField('Date Received', validators=[DataRequired()])
    receivedFrom = StringField('Received From', validators=[DataRequired()])
    account = SelectField('Account', default='Petty Cash', validators=[Optional()])
    submit = SubmitField('Submit')


class DefineSupplierForm(FlaskForm):
    supplierName = StringField('Supplier Name', validators=[DataRequired()])
    email = StringField('Email', validators=[Email()])
    telephoneNo = StringField('Telephone No.', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    submit = SubmitField('Submit')


class DefineBillsForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Submit')


class DefineAccountInfoForm(FlaskForm):
    name = StringField('Enter Name', validators=[DataRequired()])
    username = StringField('Enter User Name', validators=[DataRequired()])
    email = StringField('Enter Email', validators=[DataRequired(), Email()])
    phonenumber = StringField('Enter Phone Number', validators=[DataRequired()])
    password = PasswordField("Enter Password",
                             validators=[DataRequired()
                                         ])  # '''EqualTo('confirmPassword', message='Passwords must match')'''
    confirmPassword = PasswordField("Confirm password entered", validators=[DataRequired()])
    edit = 0
    submit = SubmitField('Submit')


class UpdateDeliveriesForm(FlaskForm):
    invoice_receipt = SelectField('Choose Invoice/Receipt', validators=[DataRequired()])
    invoiceNo_receiptNo = StringField('Enter Invoice No/Receipt No', validators=[DataRequired()])
    deliveredDate = StringField('Enter Delivered Date', validators=[DataRequired()])
    paymentMode = SelectField('Choose payment mode', validators=[DataRequired()])
    referenceNo = StringField('Enter reference No')
    AmountPaid = StringField('Enter amount paid', validators=[DataRequired()])
    submit = SubmitField('Save Changes')


class DefineItemUomForm(FlaskForm):
    chooseRawMaterial = SelectField('Choose raw material', validators=[DataRequired()])
    chooseUnitOfMeasure = SelectField("Choose unit of measure", validators=[DataRequired()])
    submit = SubmitField("Submit")


class DefineConversionFactorsForm(FlaskForm):
    chooseRawMaterial = SelectField('Choose raw material', validators=[DataRequired()])
    chooseItemUom = SelectField("Choose Item Uom", validators=[DataRequired()])
    measurementDescription = StringField('Measurement Description', validators=[DataRequired()])
    quantity = StringField('Quantity', validators=[DataRequired()])
    submit = SubmitField("Submit")


class DefineProductionActivitiesForm(FlaskForm):
    activity = StringField('Activity', validators=[DataRequired()])
    submit = SubmitField("Add a new activity")


class ReceiveMaterialQuantitiesForm(FlaskForm):
    selectMaterial = SelectField('Select material', validators=[DataRequired()])
    selectReceivedDate = SelectField('Select received date', validators=[DataRequired()])
    unitofMeasure = StringField('Unit of Measure', validators=[DataRequired()])
    quantity = SelectField('Quantity', validators=[DataRequired()])
    submit = SubmitField("Add Quantity")


class ViewQuantityBalancesForm(FlaskForm):
    material = StringField('Raw Material', validators=[DataRequired()])
    unitofmeasure = StringField('Unit of Measure', validators=[DataRequired()])
    balance = StringField('Balance', validators=[DataRequired()])


class UpdateDailyProductionForm(FlaskForm):
    chooseProductionActivity = SelectField('Select Activity', validators=[DataRequired()])
    chooseMeasure = SelectField('Select Measure', validators=[DataRequired()])
    quantity = StringField('Enter Quantity', validators=[DataRequired()])
    date = StringField('Date', validators=[DataRequired()])
    submit = SubmitField('Submit')


class ViewDailyProductionForm(FlaskForm):
    activity = StringField('Activity', validators=[DataRequired()])
    measure = StringField('Measure', validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[DataRequired()])
    item = StringField('Item', validators=[DataRequired()])
    uom = StringField('UoM', validators=[DataRequired()])
    quantityUsed = IntegerField('Quantity Used', validators=[DataRequired()])
    productionDate = StringField('Production Date', validators=[DataRequired()])
    submit = SubmitField("Submit")


class DefinePackagingMaterialsForm(FlaskForm):
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Submit')


class UpdatePackagingMaterialsForm(FlaskForm):
    choosePackagingMaterial = SelectField('Select Packaging Material', validators=[DataRequired()])
    quantity = IntegerField('Enter Quantity', validators=[DataRequired()])
    date = StringField('Date', validators=[DataRequired()])
    submit = SubmitField("Add New")


class UpdateFinishedGoodsForm(FlaskForm):
    chooseProduct = SelectField('Select Product', validators=[DataRequired()])
    choosePackingMaterial = SelectField('Select Packing Material', validators=[DataRequired()])
    quantityUsed = IntegerField('Enter Quantity', validators=[DataRequired()])
    date = StringField('Date', validators=[DataRequired()])
    submit = SubmitField("Update Finished Goods")


class RequestResetForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = UserAccountTb.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You must register first.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')
