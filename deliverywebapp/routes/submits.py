from flask import render_template, flash, redirect, url_for
from deliverywebapp.forms.forms import LoginForm, DefineProductsForm
from deliverywebapp import app,db
from deliverywebapp.models.models import ProductTb
from flask_sqlalchemy import sqlalchemy

#
# @app.route('/define_product/Submit', methods=['POST'])
# def DefineProductSubmit():
#     form = DefineProductsForm()
#     if form.validate_on_submit():
#
#         try:
#             data = ProductTb(form.productSKU.data, form.productDescription.data)
#             db.session.add(data)
#             db.session.commit()
#         except sqlalchemy.exc.IntegrityError:
#             flash('An error occured when adding product','error')
#
#         flash('Product successfully added', 'success')
#         redirect(url_for('viewProduct'))
#
#     return render_template(url_for('defineProduct'))
