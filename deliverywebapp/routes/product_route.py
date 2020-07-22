from flask import render_template, flash, redirect, url_for, request, json
from deliverywebapp.forms.forms import  DefineProductsForm
from deliverywebapp import app
from flask_sqlalchemy import sqlalchemy
from deliverywebapp.utility import AlchemyEncoder
from deliverywebapp.models.models import *

# MANAGE PRODUCT
@app.route('/search_view_product', methods=['POST', 'GET'])
def searchViewProducts():
    searchbox = request.form.get('text')
    try:
        if searchbox != "":
            products = ProductTb.query.filter(ProductTb.Description.like('%' + searchbox + '%')).all()
            return json.dumps(products, cls=AlchemyEncoder)
        else:
            products = ProductTb.query.all()
            return json.dumps(products, cls=AlchemyEncoder)

    except Exception as ex:
            flash(ex, 'danger')


@app.route('/delivery_app/view-product')
def viewProduct():
    return render_template('./delivery_app/view-product.html')


@app.route('/delivery_app/define-product-edit/<string:id>', methods=['GET', 'POST'])
def editDefineProduct(id):
    form = DefineProductsForm()

    if request.method == 'GET':
        try:
            product = ProductTb.query.get(id)
            form.productSKU.data = product.SKUNumber
            form.productDescription.data = product.Description
        except sqlalchemy.exc.SQLAlchemyError as ex:
            flash(ex, ' danger')
    elif form.validate_on_submit():
        try:
            ProductTbEdit = db.session.query(ProductTb).filter(ProductTb.ID == id).one()
            BeforeSKUNumber = ProductTbEdit.SKUNumber
            BeforeDescription = ProductTbEdit.Description
            ProductTbEdit.SKUNumber = form.productSKU.data
            ProductTbEdit.Description = form.productDescription.data
            db.session.commit()

            if BeforeSKUNumber != form.productSKU.data:
                flash('\n\t ' + BeforeSKUNumber + ' successfully edited to ' + form.productSKU.data,
                      'success')
            if BeforeDescription != form.productDescription.data:
                flash('\n\t ' + BeforeDescription + ' successfully edited to ' + form.productDescription.data,
                      'success')
        except sqlalchemy.exc.SQLAlchemyError as ex:
            flash(ex, ' danger')

        return redirect(url_for('viewProduct', form=form))

    return render_template('./delivery_app/define-product.html', form=form)


@app.route('/delivery_app/define-product', methods=['GET', 'POST'])
def defineProduct():
    form = DefineProductsForm()

    if form.validate_on_submit():
        try:
            data = ProductTb(form.productSKU.data, form.productDescription.data)
            db.session.add(data)
            db.session.commit()
        except sqlalchemy.exc.SQLAlchemyError as ex:
            flash(ex, ' danger')

        flash('Product: "' + form.productSKU.data + '" successfully added', 'success')
        return redirect(url_for('viewProduct', form=form))

    return render_template('./delivery_app/define-product.html', form=form)