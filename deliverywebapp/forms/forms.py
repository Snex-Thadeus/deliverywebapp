import phonenumbers as phonenumbers
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, RadioField, SelectField, \
    ValidationError, DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, InputRequired, ValidationError
from flask import flash

CUSTOMER_TYPE = ['Hotel', 'Individual', 'Restaurant', 'School', 'Camp',
                 'Institution']


class LoginForm(FlaskForm):
    email = StringField('Email address', validators=[DataRequired(), Email()])
    password = StringField('Password', validators=[DataRequired()])
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
    lpoNo = StringField('LPO Number', validators=[DataRequired()])
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
    contactperson = StringField('Contact Person', validators=[DataRequired()])
    # fetch the list below from db
    customerType = SelectField('Customer Type', validators=[DataRequired()], choices=CUSTOMER_TYPE)
    email = StringField('Email', validators=[DataRequired(), Email(message='Not a valid email address')])
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
    account = SelectField('Account', default='Petty Cash', validators=[DataRequired()])
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


class DefineAccountInfo(FlaskForm):
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


class UpdateDeliveries(FlaskForm):
    invoice_receipt = SelectField('Choose Invoice/Receipt', validators=[DataRequired()])
    invoiceNo_receiptNo = StringField('Enter Invoice No/Receipt No', validators=[DataRequired()])
    deliveredDate = StringField('Enter Delivered Date', validators=[DataRequired()])
    paymentMode = SelectField('Choose payment mode', validators=[DataRequired()])
    referenceNo = StringField('Enter reference No')
    AmountPaid = StringField('Enter amount paid', validators=[DataRequired()])
    submit = SubmitField('Save Changes')


class DefineItemUom(FlaskForm):
    chooseRawMaterail = SelectField('Choose raw material', validators=[DataRequired()])
    chooseUnitOfMeasure = SelectField("Choose unit of measure", validators=[DataRequired()])
    submit = SubmitField("Submit")


class DefineConversionFactors(FlaskForm):
    chooseRawMaterail = SelectField('Choose raw material', validators=[DataRequired()])
    chooseItemUom = SelectField("Choose Item Uom", validators=[DataRequired()])
    measurementDescription = SelectField('Measurement Description', validators=[DataRequired()])
    quantity = SelectField('Quantity', validators=[DataRequired()])


class DefineProductionActivities(FlaskForm):
    activity = SelectField('Activity', validators=[DataRequired()])
