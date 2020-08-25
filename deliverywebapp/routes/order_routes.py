from flask import render_template, flash, redirect, url_for, request, jsonify, json
from deliverywebapp.forms.forms import DefineOrdersForm
from deliverywebapp import app
from deliverywebapp.utility import AlchemyEncoder, get_clean_price_value
from deliverywebapp.models.models import *


@app.route('/search_view_orders', methods=['GET', 'POST'])
def search_view_orders():
    return json.dumps(OrdersTb.query.all(), cls=AlchemyEncoder)


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
def filter_products_prices_by_delivery_method(filter):
    delivery = filter.split(" ")[0]
    category = filter.split(" ")[1]

    products = db.session.execute("SELECT product_price_tb.ID, product_tb.Description, product_price_tb.Category,"
                                  "product_price_tb.Method, product_price_tb.Price FROM product_tb INNER JOIN "
                                  "product_price_tb ON product_tb.ID = product_price_tb.ProductTbID "
                                  "WHERE product_price_tb.Method = '" + delivery + "' AND product_price_tb.Category = '" + category + "'")

    product_rows = [dict(row) for row in products]

    return json.dumps(product_rows, cls=AlchemyEncoder)


CATEGORY = [(-1, "Choose Category"), ("Wholesale", "Wholesale"), ("Retail", "Retail")]


@app.route('/delivery_app/define-orders', methods=['GET', 'POST'])
def define_orders():
    form = DefineOrdersForm()
    if request.method == "GET":
        try:
            product_tb = ProductTb.query.all()
            product_drop_down_list = productTbDropDownSchema.dump(product_tb)

            choices = [(-1, "Choose Product")]
            for i in product_drop_down_list:
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
                return redirect(url_for('define_orders', form=form))
            if form.deliveryMethod.data == "-1":
                flash("Please select delivery method", "warning")
                return redirect(url_for('define_orders', form=form))
            if form.ddProducts.data == "-1":
                flash("Please select product", "warning")
                return redirect(url_for('defineOrders', form=form))

            phone_number = None
            if form.customer.data:
                for isPhonenumber in form.customer.data.split(" "):
                    if "254" in isPhonenumber or "07" in isPhonenumber:
                        phone_number = isPhonenumber
                        break

            price = form.ddProducts.data  # .split(" ")[0]

            orders = OrdersTb(form.customer.data,
                             phone_number,
                             form.deliveryMethod.data,
                             form.location.data,
                             form.orderdate.data,
                             form.lpoNo.data,
                             price,
                             get_clean_price_value(form.price.data),
                             form.quantity.data,
                             get_clean_price_value(form.totalAmount.data)
                             )
            db.session.add(orders)
            db.session.commit()

            flash(
                'Order: "' + form.lpoNo.data + '" is successfully added ',
                'success')
            return redirect(url_for('view_orders', form=form))
        except Exception as ex:
            flash(ex, 'danger')

    return render_template('/delivery_app/define-orders.html', form=form)


@app.route('/delivery_app/define-order-edit/<string:id>', methods=['GET', 'POST'])
def edit_define_orders(id):
    pass


@app.route('/orders/<int:page_num>')
def orders(page_num):
    orders = OrdersTb.query.paginate(per_page=50, page=page_num, error_out=True)
    return render_template('pagination.html', orders=orders)


@app.route('/delivery_app/view-order')
def view_orders():
    return render_template('/delivery_app/view-orders.html')
