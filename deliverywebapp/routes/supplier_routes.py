from flask import render_template, flash, redirect, url_for, request, jsonify, json
from deliverywebapp.forms.forms import DefineSupplierForm
from deliverywebapp import app
from flask_sqlalchemy import sqlalchemy
from deliverywebapp.utility import AlchemyEncoder
from deliverywebapp.models.models import *


@app.route('/search_view_suppliers', methods=['POST', 'GET'])
def search_view_supplier():
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
def define_suppliers():
    form = DefineSupplierForm()
    if form.validate_on_submit():
        try:
            supplier_name = form.supplierName.data
            email = form.email.data
            telephone = form.telephoneNo.data
            location = form.location.data
            # TODO:
            supplier = SupplierTb(
                Name=supplier_name,
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

    return render_template('/delivery_app/define-suppliers.html', form=form)


@app.route('/delivery_app/define-supplier-edit/<string:id>', methods=['GET', 'POST'])
def edit_define_supplier(id):
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
            supplier_tb_edit = db.session.query(SupplierTb).filter(SupplierTb.ID == id).one()

            before_supplier_name = supplier_tb_edit.Name
            before_email = supplier_tb_edit.Email
            before_telephone = supplier_tb_edit.TelephoneNo
            before_location = supplier_tb_edit.Location

            supplier_tb_edit.SupplierName = form.supplierName.data
            supplier_tb_edit.Email = form.email.data
            supplier_tb_edit.TelephoneNo = form.telephoneNo.data
            supplier_tb_edit.Location = form.location.data

            db.session.commit()

            if before_supplier_name != form.supplierName.data:
                flash(
                    '\n\t "' + before_supplier_name + '" successfully edited to "' + form.supplierName.data + '"',
                    'success')
            if before_email != form.email.data:
                flash(
                    '\n\t "' + before_email + '" successfully edited to "' + form.email.data + '"',
                    'success')
            if before_telephone != form.telephoneNo.data:
                flash(
                    '\n\t "' + before_telephone + '" successfully edited to "' + form.telephoneNo.data + '"',
                    'success')
            if before_location != form.location.data:
                flash(
                    '\n\t "' + before_location + '" successfully edited to "' + form.location.data + '"',
                    'success')
        except sqlalchemy.exc.SQLAlchemyError as ex:
            flash(ex, ' danger')

        return redirect(url_for('viewSupplies', form=form))

    return render_template('/delivery_app/define-suppliers.html', form=form)


@app.route('/delivery_app/view-suppliers')
def view_suppliers():
    return render_template('/delivery_app/view-suppliers.html')

