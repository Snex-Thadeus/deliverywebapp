from flask import render_template, flash, redirect, url_for, request, json, jsonify
from deliverywebapp.forms.forms import DefineProductPricesForm
from deliverywebapp import app
from flask_sqlalchemy import sqlalchemy
from deliverywebapp.utility import AlchemyEncoder, getIDForChooseCategory, getIDForChooseMethod, getCleanPriceValue
from deliverywebapp.models.models import *

productTbDropDownSchema = ProductTbDropDownSchema(many=True)


@app.route('/search_view_product_prices', methods=['POST', 'GET'])
def searchViewProductPrices():
    searchbox = request.form.get('text')
    try:
        if searchbox != "":

            product = db.session.execute(
                'SELECT product_price_tb.ID, product_tb.Description, product_price_tb.Category, '
                'product_price_tb.Method, product_price_tb.Price FROM product_tb INNER JOIN product_price_tb ON '
                'product_tb.ID = product_price_tb.ProductTbID WHERE product_tb.Description like "%' + searchbox + '%"')

            productRows = [dict(row) for row in product]

            return json.dumps(productRows, cls=AlchemyEncoder)
        else:
            # products = ProductPriceTb.query.all()
            product = db.session.execute(
                'SELECT product_price_tb.ID, product_tb.Description, product_price_tb.Category, '
                'product_price_tb.Method, product_price_tb.Price FROM product_tb INNER JOIN product_price_tb ON '
                'product_tb.ID = product_price_tb.ProductTbID;')

            productRows = [dict(row) for row in product]
            return json.dumps(productRows, cls=AlchemyEncoder)

    except Exception as ex:
        flash(ex, 'danger')


PRODUCT_PRICE_CATEGORY = ["Wholesale", "Retail"]
PRODUCT_PRICE_METHOD = ["Factory", "Delivery"]


@app.route('/delivery_app/define-product-prices-edit/<string:id>', methods=['GET', 'POST'])
def editDefineProductPrices(id):
    form = DefineProductPricesForm()
    if request.method == "GET":
        try:

            productPrices = ProductPriceTb.query.get(id)

            # first populate the drop downs, this will be modularized since its duplicated
            productTB = ProductTb.query.all()

            productDropDownList = productTbDropDownSchema.dump(productTB)
            form.chooseProduct.choices = [(i['ID'], i['Description']) for i in productDropDownList]
            form.chooseCategory.choices = PRODUCT_PRICE_CATEGORY
            form.chooseMethod.choices = PRODUCT_PRICE_METHOD

            # must specify the default value and the data for EACH FORM SelectField
            # product = ProductTb.query.get(
            #    productPrices.ProductTbID)
            # this wasted my time, tyring to supply data for choose-product with product.Description
            form.chooseProduct.data = str(productPrices.ProductTbID)
            form.chooseMethod.data = productPrices.Method
            form.chooseCategory.data = productPrices.Category

            form.chooseProduct.default = productPrices.ProductTbID
            form.chooseCategory.default = getIDForChooseCategory(PRODUCT_PRICE_CATEGORY, productPrices.Category)
            form.chooseMethod.default = getIDForChooseMethod(PRODUCT_PRICE_METHOD, productPrices.Method)
            form.price.data = productPrices.Price

        except Exception as ex:
            flash(ex, 'danger')

    elif form.validate_on_submit():
        try:
            ProductPriceTbEdit = db.session.query(ProductPriceTb).filter(ProductPriceTb.ID == id).one()

            BeforeProduct = ProductPriceTbEdit.ProductTbID
            BeforeCategory = ProductPriceTbEdit.Category
            BeforeMethod = ProductPriceTbEdit.Method
            BeforePrice = ProductPriceTbEdit.Price

            ProductPriceTbEdit.ProductTbID = form.chooseProduct.data
            ProductPriceTbEdit.Category = form.chooseCategory.data
            ProductPriceTbEdit.Method = form.chooseMethod.data
            ProductPriceTbEdit.Price = getCleanPriceValue(form.price.data)

            db.session.commit()

            if BeforeProduct != form.chooseProduct.data:
                product = db.session.execute(
                    'SELECT product_tb.ID, product_tb.Description FROM product_tb INNER JOIN product_price_tb ON '
                    'product_tb.ID = product_price_tb.ProductTbID WHERE product_tb.ID = ' + form.chooseProduct.data)

                productRows = [dict(row) for row in product]
                BeforeProduct = productRows[0][
                    'Description']
                flash('\n\t ' + BeforeProduct + ' successfully edited to ' + form.chooseProduct.data,
                      'success')
            if BeforeCategory != form.chooseCategory.data:
                flash('\n\t ' + BeforeCategory + ' successfully edited to ' + form.chooseCategory.data,
                      'success')
            if BeforeMethod != form.chooseMethod.data:
                flash('\n\t ' + BeforeMethod + ' successfully edited to ' + form.chooseMethod.data,
                      'success')
            if BeforePrice != form.productDescription.data:
                flash('\n\t ' + BeforePrice + ' successfully edited to ' + form.price.data,
                      'success')
        except Exception as ex:
            flash(ex, 'danger')

        return redirect(url_for('viewProductPrices', form=form))

    return render_template('./delivery_app/define-product-prices.html', form=form)


# MANAGE PRODUCT PRICE

productTbDropDownSchema = ProductTbDropDownSchema(many=True)


@app.route('/delivery_app/view-product-prices')
def viewProductPrices():
    return render_template('./delivery_app/view-product-prices.html')


@app.route('/delivery_app/define-product-prices', methods=['POST', 'GET'])
def defineProductPrices():
    form = DefineProductPricesForm()
    # use request.method when you have SelectField in your Form.
    if request.method == 'GET':
        try:
            productTB = ProductTb.query.all()
            productDropDownList = productTbDropDownSchema.dump(productTB)
            form.chooseProduct.choices = [(i['ID'], i['Description']) for i in productDropDownList]
            form.chooseCategory.choices = PRODUCT_PRICE_CATEGORY
            form.chooseMethod.choices = PRODUCT_PRICE_METHOD
        except Exception as ex:
            flash(ex, 'danger')

    elif request.method == 'POST':
        try:
            price = getCleanPriceValue(form.price.data)

            data = ProductPriceTb(form.chooseProduct.data, form.chooseCategory.data,
                                  form.chooseMethod.data, price)
            db.session.add(data)
            db.session.commit()

        except Exception as ex:
            flash(ex, 'danger')

        try:
            product = db.session.execute(
                'SELECT product_tb.ID, product_tb.Description FROM product_tb INNER JOIN product_price_tb ON '
                'product_tb.ID = product_price_tb.ProductTbID WHERE product_tb.ID = ' + form.chooseProduct.data)

            productRows = [dict(row) for row in product]

            if len(productRows) > 0:
                flash('Product: "' + productRows[0][
                    'Description'] + '" successfully set to price of ' + form.price.data,
                      'success')
            else:
                flash("Product price was not added, try again", ' danger')

            return redirect(url_for('viewProductPrices'))

        except Exception as ex:
            flash(ex, 'danger')
            return redirect(url_for('viewProductPrices'))

    return render_template('./delivery_app/define-product-prices.html', form=form)
