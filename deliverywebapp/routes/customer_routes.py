from flask import render_template, flash, redirect, url_for, request, jsonify, json
from deliverywebapp.forms.forms import DefineCustomerDetailsForm
from deliverywebapp import app
from deliverywebapp.utility import AlchemyEncoder
from deliverywebapp.models.models import *


@app.route('/search_view_customers', methods=['GET', 'POST'])
def search_view_customers():
    searchbox = request.form.get('text')
    try:
        count = len(searchbox)
        if len(searchbox) > 0:

            customers = db.session.execute(
                "SELECT c.ID,c.FirstName, c.LastName,c.ContactPerson, c.Type, c.Email, c.PhoneNumber,"
                " c.PhoneNumber2,c.PhoneNumber3,a.Name, c.Location "
                "FROM customer_tb c INNER JOIN areas_tb a ON "
                "c.AreaID = a.ID"
                " WHERE c.FirstName LIKE '%" + searchbox + "%' OR c.LastName LIKE '%" + searchbox + "%'"
            )

            # customers = CustomerTb.query.filter(
            #     or_(CustomerTb.FirstName.like('%' + searchbox + '%'), CustomerTb.LastName.like('%' + searchbox + '%')))
            return json.dumps([dict(row) for row in customers], cls=AlchemyEncoder)
        else:
            customers = db.session.execute(
                "SELECT c.ID,c.FirstName, c.LastName,c.ContactPerson, c.Type, c.Email, c.PhoneNumber,"
                " c.PhoneNumber2,c.PhoneNumber3,a.Name, c.Location "
                "FROM customer_tb c INNER JOIN areas_tb a ON "
                "c.AreaID = a.ID"
            )
            customers2 = [dict(row) for row in customers]
            return json.dumps(customers2, cls=AlchemyEncoder)

    except Exception as ex:
        flash(ex, 'danger')


areasTbDropDownSchema = AreaTbDropDownSchema(many=True)


@app.route('/delivery_app/define-customer', methods=['GET', 'POST'])
def define_customer_details():
    form = DefineCustomerDetailsForm()
    if request.method == "POST":
        try:

            customer = CustomerTb(
                FirstName=form.firstname.data,
                LastName=form.lastname.data,
                ContactPerson=form.contactperson.data,
                Type=form.customerType.data,
                Email=form.email.data,
                PhoneNumber=form.phonenumber1.data,
                PhoneNumber2=form.phonenumber2.data,
                PhoneNumber3=form.phonenumber3.data,
                AreaID=form.area.data,
                Location=form.location.data)

            db.session.add(customer)
            db.session.commit()

        except Exception as ex:
            flash(ex, 'danger')

        flash('Customer: "' + form.firstname.data + '  ' + form.lastname.data + '" successfully added', 'success')
        return redirect(url_for('view_customers_details'))

    elif request.method == "GET":
        try:
            areas_drop_down_list = areasTbDropDownSchema.dump(AreasTb.query.all())
            form.area.choices = [(i['ID'], i['Name']) for i in areas_drop_down_list]

        except Exception as ex:
            flash(ex, "danger")

    return render_template('/delivery_app/define-customers.html', form=form)


@app.route('/delivery_app/define-customer-edit/<string:id>', methods=['GET', 'POST'])
def edit_define_customers_details():
    pass


@app.route('/delivery_app/view-customer', methods=['GET', 'POST'])
def view_customers_details():
    return render_template('/delivery_app/view-customers.html')
