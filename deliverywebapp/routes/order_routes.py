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
    customer_tb = CustomerTb.query.all()
    return jsonify(customers_schema.dump(customer_tb))
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
                'Order: "' + form.customer.data + '", "' + form.lpoNo.data + '", "' + form.price.data + '" is successfully added ',
                'success')
            return redirect(url_for('view_orders', form=form))
        except Exception as ex:
            flash(ex, 'danger')

    return render_template('/delivery_app/define-orders.html', form=form)


@app.route('/delivery_app/define-order-edit/<string:id>', methods=['GET', 'POST'])
def edit_define_orders(id):
    form = DefineOrdersForm()

    if not form.validate_on_submit():
        try:
            order = OrdersTb.query.get(id)
            form.customer.data = order.customer
            phone_number = order.phone_number
            form.deliveryMethod.data = order.deliveryMethod
            form.location.data = order.location
            form.orderdate.data = order.orderdate
            form.lpoNo.data = order.lpoNo
            form.ddProducts.data = order.ddProducts
            order.get_clean_price_value(form.price.data)
            form.quantity.data = order.quantity
            order.get_clean_price_value(form.totalAmount.data)

        except Exception as ex:
            flash(ex, 'danger')
    elif form.validate_on_submit():
        try:
            order_tb_edit = db.session.query(OrdersTb).filter(OrdersTb.ID == id).one()
            before_customer = order_tb_edit.customer
            before_phone_number = order_tb_edit.phone_number
            before_delivery_method = order_tb_edit.deliveryMethod
            before_location = order_tb_edit.location
            before_orderdate = order_tb_edit.orderdate
            before_lpo_no = order_tb_edit.lpoNo
            before_dd_products = order_tb_edit.ddProducts
            before_price = order_tb_edit.get_clean_price_value(form.price.data)
            before_quantity = order_tb_edit.quantity
            before_total_amount = order_tb_edit.get_clean_price_value(form.totalAmount.data)

            order_tb_edit.customer = form.customer.data
            order_tb_edit.phone_number = form.phone_number.data
            order_tb_edit.deliveryMethod = form.deliveryMethod.data
            order_tb_edit.location = form.location.data
            order_tb_edit.orderdate = form.orderdate.data
            order_tb_edit.lpoNo = form.lpoNo.data
            order_tb_edit.ddProducts = form.ddProducts.data
            order_tb_edit.get_clean_price_value(form.price.data)
            order_tb_edit.quantity = form.quantity.data
            order_tb_edit.get_clean_price_value(form.totalAmount.data)

            db.session.commit()

            if before_customer != form.customer.data:
                flash(
                    '\n\t "' + before_customer + '" successfully edited to "' + form.customer.data + '"',
                    'success')

            if before_phone_number != form.phone_number.data:
                flash(
                    '\n\t "' + before_phone_number + '" successfully edited to "' + form.phone_number.data + '"',
                    'success')

            if before_delivery_method != form.delivery_method.data:
                flash(
                    '\n\t "' + before_delivery_method + '" successfully edited to "' + form.delivery_method.data + '"',
                    'success')

            if before_location != form.location.data:
                flash(
                    '\n\t "' + before_location + '" successfully edited to "' + form.location.data + '"',
                    'success')

            if before_orderdate != form.orderdate.data:
                flash(
                    '\n\t "' + before_orderdate + '" successfully edited to "' + form.orderdate.data + '"',
                    'success')

            if before_lpo_no != form.lpoNo.data:
                flash(
                    '\n\t "' + before_lpo_no + '" successfully edited to "' + form.lpoNo.data + '"',
                    'success')

            if before_dd_products != form.ddproducts.data:
                flash(
                    '\n\t "' + before_dd_products + '" successfully edited to "' + form.ddproducts.data + '"',
                    'success')

            if before_price != form.price.data:
                flash(
                    '\n\t "' + before_price + '" successfully edited to "' + form.price.data + '"',
                    'success')

            if before_quantity != form.quantity.data:
                flash(
                    '\n\t "' + before_quantity + '" successfully edited to "' + form.quantity.data + '"',
                    'success')

            if before_total_amount != form.totalAmount.data:
                flash(
                    '\n\t "' + before_total_amount + '" successfully edited to "' + form.totalAmount.data + '"',
                    'success')
        except Exception as ex:
            flash(ex, 'danger')

        return redirect(url_for('view_orders', form=form))

    return render_template('./delivery_app/define-orders.html', form=form)


@app.route('/orders/<int:page_num>')
def orders(page_num):
    orders = OrdersTb.query.paginate(per_page=50, page=page_num, error_out=True)
    return render_template('pagination.html', orders=orders)


@app.route('/delivery_app/view-order')
def view_orders():
    return render_template('/delivery_app/view-orders.html')
