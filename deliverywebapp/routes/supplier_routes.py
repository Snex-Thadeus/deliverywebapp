from flask import render_template, flash, redirect, url_for, request, jsonify, json
from deliverywebapp.forms.forms import LoginForm, DefineProductsForm, DefineAreasForm, DefineBillsForm, \
    DefineExpenseCategoriesForm, DefineSupplierForm
from deliverywebapp import app, db
from deliverywebapp.forms.search_forms import SearchViewProductsForm
from deliverywebapp.models.models import ProductTb
from flask_sqlalchemy import sqlalchemy
from sqlalchemy import update
from deliverywebapp.utility import AlchemyEncoder
from deliverywebapp.models.models import *


@app.route('/search_view_suppliers', methods=['POST', 'GET'])
def searchViewSupplier():
    searchbox = request.form.get('text')
    try:
        if searchbox != "":
            suppliers = SupplierTb.query.filter(
                SupplierTb.SupplierName.like('%' + searchbox + '%')).all()
            return json.dumps(suppliers, cls=AlchemyEncoder)
        else:
            suppliers = SupplierTb.query.all()
            return json.dumps(suppliers, cls=AlchemyEncoder)
    except sqlalchemy.exc.SQLAlchemyError as ex:
        flash(ex, ' danger')


@app.route('/delivery_app/define-suppliers', methods=['POST', 'GET'])
def defineSuppliers():
    form = DefineSupplierForm()
    if form.validate_on_submit():
        try:
            suppliername = form.supplierName.data
            email = form.email.data
            telephone = form.telephoneNo.data
            location = form.location.data
            # TODO:
            supplier = SupplierTb(
                Name=suppliername,
                Email=email,
                TelephoneNo=telephone,
                Location=location
            )

            db.session.add(supplier)
            db.session.commit()

            flash('Supplier: "' + form.supplierName.data + '" successfully added', 'success')
            return redirect(url_for('viewSupplies', form=form))
        except Exception as ex:
            flash(ex, 'danger')

    return render_template('./delivery_app/define-suppliers.html', form=form)


@app.route('/delivery_app/view-suppliers')
def viewSupplies():
    return render_template('./delivery_app/view-suppliers.html')


@app.route('/delivery_app/define-supplier-edit/<string:id>', methods=['GET', 'POST'])
def editDefineSupplier(id):
    form = DefineSupplierForm()
    if not form.validate_on_submit():
        try:
            supplier = ExpenseCategoriesTb.query.get(id)
            form.supplierName.data = supplier.Name
            form.email.data = supplier.Email
            form.telephoneNo = supplier.TelephoneNo
            form.location = supplier.Location
        except Exception as ex:
            flash(ex, 'danger')
    elif form.validate_on_submit():
        try:
            SupplierTbEdit = db.session.query(SupplierTb).filter(SupplierTb.ID == id).one()

            BeforeSupplierName = SupplierTbEdit.Name
            BeforeEmail = SupplierTbEdit.Email
            BeforeTelephone = SupplierTbEdit.TelephoneNo
            BeforeLocation = SupplierTbEdit.Location

            SupplierTbEdit.SupplierName = form.supplierName.data
            SupplierTbEdit.Email = form.email.data
            SupplierTbEdit.TelephoneNo = form.telephoneNo.data
            SupplierTbEdit.Location = form.location.data

            db.session.commit()

            if BeforeSupplierName != form.supplierName.data:
                flash(
                    '\n\t "' + BeforeSupplierName + '" successfully edited to "' + form.supplierName.data + '"',
                    'success')
            if BeforeEmail != form.email.data:
                flash(
                    '\n\t "' + BeforeEmail + '" successfully edited to "' + form.email.data + '"',
                    'success')
            if BeforeTelephone != form.telephoneNo.data:
                flash(
                    '\n\t "' + BeforeTelephone + '" successfully edited to "' + form.telephoneNo.data + '"',
                    'success')
            if BeforeLocation != form.location.data:
                flash(
                    '\n\t "' + BeforeLocation + '" successfully edited to "' + form.location.data + '"',
                    'success')
        except sqlalchemy.exc.SQLAlchemyError as ex:
            flash(ex, ' danger')

        return redirect(url_for('viewSupplies', form=form))

    return render_template('./delivery_app/define-suppliers.html', form=form)
