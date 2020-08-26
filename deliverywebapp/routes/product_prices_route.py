from flask import render_template, flash, redirect, url_for, request, json, jsonify
from deliverywebapp.forms.forms import DefineProductPricesForm
from deliverywebapp import app
from deliverywebapp.utility import AlchemyEncoder, get_id_for_choose_category, get_id_for_choose_method, get_clean_price_value
from deliverywebapp.models.models import *

productTbDropDownSchema = ProductTbDropDownSchema(many=True)


@app.route('/search_view_product_prices', methods=['POST', 'GET'])
def search_view_product_prices():
    searchbox = request.form.get('text')
    try:
        if searchbox != "":

            product = db.session.execute(
                'SELECT product_price_tb.ID, product_tb.Description, product_price_tb.Category, '
                'product_price_tb.Method, product_price_tb.Price FROM product_tb INNER JOIN product_price_tb ON '
                'product_tb.ID = product_price_tb.ProductTbID WHERE product_tb.Description like "%' + searchbox + '%"')

            product_rows = [dict(row) for row in product]

            return json.dumps(product_rows, cls=AlchemyEncoder)
        else:
            # products = ProductPriceTb.query.all()
            product = db.session.execute(
                'SELECT product_price_tb.ID, product_tb.Description, product_price_tb.Category, '
                'product_price_tb.Method, product_price_tb.Price FROM product_tb INNER JOIN product_price_tb ON '
                'product_tb.ID = product_price_tb.ProductTbID;')

            product_rows = [dict(row) for row in product]
            return json.dumps(product_rows, cls=AlchemyEncoder)

    except Exception as ex:
        flash(ex, 'danger')


# MANAGE PRODUCT PRICE

productTbDropDownSchema = ProductTbDropDownSchema(many=True)


@app.route('/delivery_app/define-product-prices', methods=['POST', 'GET'])
def define_product_prices():
    form = DefineProductPricesForm()
    # use request.method when you have SelectField in your Form.
    if request.method == 'GET':
        try:
            product_tb = ProductTb.query.all()
            product_drop_down_list = productTbDropDownSchema.dump(product_tb)
            form.chooseProduct.choices = [(i['ID'], i['Description']) for i in product_drop_down_list]
            form.chooseCategory.choices = PRODUCT_PRICE_CATEGORY
            form.chooseMethod.choices = PRODUCT_PRICE_METHOD
        except Exception as ex:
            flash(ex, 'danger')

    elif request.method == 'POST':
        try:
            price = get_clean_price_value(form.price.data)

            product = ProductPriceTb(form.chooseProduct.data,
                                  form.chooseCategory.data,
                                  form.chooseMethod.data,
                                  price)
            db.session.add(product)
            db.session.commit()

            flash(
                'Product Price: "' + form.chooseCategory.data + '", "' + form.chooseMethod.data + '", "' + form.price.data + '" is successfully added ',
                'success')
            return redirect(url_for('view_product_prices', form=form))

        except Exception as ex:
            flash(ex, 'danger')

    return render_template('/delivery_app/define-product-prices.html', form=form)


PRODUCT_PRICE_CATEGORY = ["Wholesale", "Retail"]
PRODUCT_PRICE_METHOD = ["Factory", "Delivery"]


@app.route('/delivery_app/define-product-prices-edit/<string:id>', methods=['GET', 'POST'])
def edit_define_product_prices(id):
    form = DefineProductPricesForm()
    if request.method == "GET":
        try:

            product_prices = ProductPriceTb.query.get(id)

            # first populate the drop downs, this will be modularized since its duplicated
            product_tb = ProductTb.query.all()

            product_drop_down_list = productTbDropDownSchema.dump(product_tb)
            form.chooseProduct.choices = [(i['ID'], i['Description']) for i in product_drop_down_list]
            form.chooseCategory.choices = PRODUCT_PRICE_CATEGORY
            form.chooseMethod.choices = PRODUCT_PRICE_METHOD

            # must specify the default value and the data for EACH FORM SelectField
            # product = ProductTb.query.get(
            #    productPrices.ProductTbID)
            # this wasted my time, tyring to supply data for choose-product with product.Description
            form.chooseProduct.data = str(product_prices.ProductTbID)
            form.chooseMethod.data = product_prices.Method
            form.chooseCategory.data = product_prices.Category

            form.chooseProduct.default = product_prices.ProductTbID
            form.chooseCategory.default = get_id_for_choose_category(PRODUCT_PRICE_CATEGORY, product_prices.Category)
            form.chooseMethod.default = get_id_for_choose_method(PRODUCT_PRICE_METHOD, product_prices.Method)
            form.price.data = product_prices.Price

        except Exception as ex:
            flash(ex, 'danger')

    elif form.validate_on_submit():
        try:
            product_price_tb_edit = db.session.query(ProductPriceTb).filter(ProductPriceTb.ID == id).one()

            before_product = product_price_tb_edit.ProductTbID
            before_category = product_price_tb_edit.Category
            before_method = product_price_tb_edit.Method
            before_price = product_price_tb_edit.Price

            product_price_tb_edit.ProductTbID = form.chooseProduct.data
            product_price_tb_edit.Category = form.chooseCategory.data
            product_price_tb_edit.Method = form.chooseMethod.data
            product_price_tb_edit.Price = get_clean_price_value(form.price.data)

            db.session.commit()

            if before_product != form.chooseProduct.data:
                product = db.session.execute(
                    'SELECT product_tb.ID, product_tb.Description FROM product_tb INNER JOIN product_price_tb ON '
                    'product_tb.ID = product_price_tb.ProductTbID WHERE product_tb.ID = ' + form.chooseProduct.data)

                product_rows = [dict(row) for row in product]
                before_product = product_rows[0][
                    'Description']
                flash('\n\t ' + before_product + ' successfully edited to ' + form.chooseProduct.data,
                      'success')
            if before_category != form.chooseCategory.data:
                flash('\n\t ' + before_category + ' successfully edited to ' + form.chooseCategory.data,
                      'success')
            if before_method != form.chooseMethod.data:
                flash('\n\t ' + before_method + ' successfully edited to ' + form.chooseMethod.data,
                      'success')
            if before_price != form.productDescription.data:
                flash('\n\t ' + before_price + ' successfully edited to ' + form.price.data,
                      'success')
        except Exception as ex:
            flash(ex, 'danger')

        return redirect(url_for('view_product_prices', form=form))

    return render_template('./delivery_app/define-product-prices.html', form=form)


@app.route('/delivery_app/view-product-prices')
def view_product_prices():
    return render_template('/delivery_app/view-product-prices.html')


