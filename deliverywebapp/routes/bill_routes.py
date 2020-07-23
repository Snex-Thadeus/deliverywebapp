from flask import render_template, flash, redirect, url_for, request, jsonify, json
from deliverywebapp.forms.forms import LoginForm, DefineProductsForm, DefineAreasForm, DefineBillsForm
from deliverywebapp import app, db
from deliverywebapp.forms.search_forms import SearchViewProductsForm
from deliverywebapp.models.models import ProductTb
from flask_sqlalchemy import sqlalchemy
from sqlalchemy import update
from deliverywebapp.utility import AlchemyEncoder
from deliverywebapp.models.models import *


@app.route('/search_view_bills', methods=['POST', 'GET'])
def searchViewBill():
    searchbox = request.form.get('text')
    try:
        if searchbox != "":
            bills = BillTb.query.filter(BillTb.Name.like('%' + searchbox + '%')).all()
            return json.dumps(bills, cls=AlchemyEncoder)
        else:
            bills = BillTb.query.all()
            return json.dumps(bills, cls=AlchemyEncoder)

    except Exception as ex:
            flash(ex, 'danger')


@app.route('/delivery_app/define-bills', methods=['GET', 'POST'])
def defineBills():
    form = DefineBillsForm()
    if form.validate_on_submit():
        try:
            bill = BillTb(form.name.data)
            db.session.add(bill)
            db.session.commit()

        except Exception as ex:
            flash(ex, 'danger')

        flash('Bill: "' + form.name.data + '" successfully added', 'success')
        return redirect(url_for('viewBills', form=form))

    return render_template('./delivery_app/define-bills.html', form=form)


@app.route('/delivery_app/define-bill-edit/<string:id>', methods=['GET', 'POST'])
def editDefineBills(id):
    form = DefineBillsForm()
    if not form.validate_on_submit():
        try:
            bill = BillTb.query.get(id)
            form.name.data = bill.Name
        except Exception as ex:
            flash(ex, 'danger')
    elif form.validate_on_submit():
        try:
            BillsTbEdit = db.session.query(BillTb).filter(BillTb.ID == id).one()
            BeforeBill = BillsTbEdit.Name

            BillsTbEdit.Name = form.name.data

            db.session.commit()

            if BeforeBill != form.name.data:
                flash('\n\t "' + BeforeBill + '" successfully edited to "' + form.name.data + '"',
                      'success')

        except sqlalchemy.exc.SQLAlchemyError as ex:
            flash(ex, 'danger')

        return redirect(url_for('viewBills', form=form))

    return render_template('./delivery_app/define-bills.html', form=form)


@app.route('/delivery_app/view-bills')
def viewBills():
    return render_template('./delivery_app/view-bills.html')
