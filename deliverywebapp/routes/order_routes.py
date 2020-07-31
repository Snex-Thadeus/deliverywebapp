from flask import render_template, flash, redirect, url_for, request, jsonify, json, Response
from deliverywebapp.forms.forms import LoginForm, DefineProductsForm, DefineAreasForm, DefineBillsForm, \
    DefineCustomerDetailsForm, DefineOrdersForm
from deliverywebapp import app, db
from deliverywebapp.forms.search_forms import SearchViewProductsForm
from deliverywebapp.models.models import ProductTb
from flask_sqlalchemy import sqlalchemy
from sqlalchemy import update, or_
from deliverywebapp.utility import AlchemyEncoder, getCleanPriceValue
from deliverywebapp.models.models import *


@app.route('/search_view_orders', methods=['GET', 'POST'])
def searchViewOrders():
    return json.dumps(OrderTb.query.all(), cls=AlchemyEncoder)


productTbDropDownSchema = ProductTbDropDownSchema(many=True)

customers_schema = CustomerSchema(many=True)


@app.route('/customer-autocomplete', methods=['GET'])
def autocomplete():
    # TODO: CUSTOMER DATA
    customerTB = CustomerTb.query.all()
    return jsonify(customers_schema.dump(customerTB))
    # custumer_schema.dump()
    # customers = json.dumps(customerTB)
    # return Response(customers, mimetype='application/json')


DELIVERY_METHOD = [(-1, 'Choose Delivery Method'), ('Factory', 'Factory'), ('Delivery', 'Delivery')]


@app.route('/product_prices/<string:filter>', methods=['POST', 'GET'])
def filterProductsPricesByDeliveryMethod(filter):
    delivery = filter.split(" ")[0]
    category = filter.split(" ")[1]

    products = db.session.execute("SELECT product_price_tb.ID, product_tb.Description, product_price_tb.Category,"
                                  "product_price_tb.Method, product_price_tb.Price FROM product_tb INNER JOIN "
                                  "product_price_tb ON product_tb.ID = product_price_tb.ProductTbID "
                                  "WHERE product_price_tb.Method = '" + delivery + "' AND product_price_tb.Category = '" + category + "'")

    productRows = [dict(row) for row in products]

    return json.dumps(productRows, cls=AlchemyEncoder)


CATEGORY = [(-1, "Choose Category"), ("Wholesale", "Wholesale"), ("Retail", "Retail")]


@app.route('/delivery_app/define-orders', methods=['GET', 'POST'])
def defineOrders():
    form = DefineOrdersForm()
    if request.method == "GET":
        try:
            productTB = ProductTb.query.all()
            productDropDownList = productTbDropDownSchema.dump(productTB)

            choices = [(-1, "Choose Product")]
            for i in productDropDownList:
                choices.append((i['ID'], i['Description']))

            form.ddProducts.choices = choices
            form.category.choices = CATEGORY
            form.deliveryMethod.choices = DELIVERY_METHOD
        except Exception as ex:
            flash(ex, "danger")

    elif request.method == "POST":
        try:
            if form.category.data == "-1":
                flash("Please select category", "warning")
                return redirect(url_for('defineOrders', form=form))
            if form.deliveryMethod.data == "-1":
                flash("Please select delivery method", "warning")
                return redirect(url_for('defineOrders', form=form))
            if form.ddProducts.data == "-1":
                flash("Please select product", "warning")
                return redirect(url_for('defineOrders', form=form))


            phoneNumber = None
            if form.customer.data:
                for isPhonenumber in form.customer.data.split(" "):
                    if "254" in isPhonenumber or "07" in isPhonenumber:
                        phoneNumber = isPhonenumber
                        break

            price = form.ddProducts.data  # .split(" ")[0]

            orders = OrderTb(CustomerName=form.customer.data,
                             TelephoneNo=phoneNumber,
                             DeliveryMethod=form.deliveryMethod.data,
                             Location=form.location.data,
                             OrderDate=form.orderdate.data,
                             LPONo=form.lpoNo.data,
                             ProductID=price,
                             Price=getCleanPriceValue(form.price.data),
                             Quantity=form.quantity.data,
                             TotalAmount=getCleanPriceValue(form.totalAmount.data)
                             )
            db.session.add(orders)
            db.session.commit()

            flash(
                'Order: "' + form.lpoNo.data + '" is successfully added ',
                'success')
            return redirect(url_for('viewOrders', form=form))
        except Exception as ex:
            flash(ex, 'danger')

    return render_template('./delivery_app/define-orders.html', form=form)


@app.route('/delivery_app/define-order-edit/<string:id>', methods=['GET', 'POST'])
def editDefineOrders(id):
    pass


@app.route('/delivery_app/view-order')
def viewOrders():
    return render_template('./delivery_app/view-orders.html')
