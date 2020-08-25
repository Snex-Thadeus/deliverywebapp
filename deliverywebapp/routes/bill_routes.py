from flask import render_template, flash, redirect, url_for, request, jsonify, json
from deliverywebapp.forms.forms import DefineBillsForm
from deliverywebapp import app
from flask_sqlalchemy import sqlalchemy
from deliverywebapp.utility import AlchemyEncoder
from deliverywebapp.models.models import *


@app.route('/search_view_bills', methods=['POST', 'GET'])
def search_view_bill():
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
def define_bills():
    form = DefineBillsForm()
    if form.validate_on_submit():
        try:
            bill = BillTb(form.name.data)
            db.session.add(bill)
            db.session.commit()

        except Exception as ex:
            flash(ex, 'danger')

        flash('Bill: "' + form.name.data + '" successfully added', 'success')
        return redirect(url_for('view_bills', form=form))

    return render_template('/delivery_app/define-bills.html', form=form)


@app.route('/delivery_app/define-bill-edit/<string:id>', methods=['GET', 'POST'])
def edit_define_bills(id):
    form = DefineBillsForm()
    if not form.validate_on_submit():
        try:
            bill = BillTb.query.get(id)
            form.name.data = bill.Name
        except Exception as ex:
            flash(ex, 'danger')
    elif form.validate_on_submit():
        try:
            bills_tb_edit = db.session.query(BillTb).filter(BillTb.ID == id).one()
            before_bill = bills_tb_edit.Name

            bills_tb_edit.Name = form.name.data

            db.session.commit()

            if before_bill != form.name.data:
                flash('\n\t "' + before_bill + '" successfully edited to "' + form.name.data + '"',
                      'success')

        except sqlalchemy.exc.SQLAlchemyError as ex:
            flash(ex, 'danger')

        return redirect(url_for('view_bills', form=form))

    return render_template('/delivery_app/define-bills.html', form=form)


@app.route('/delivery_app/view-bills')
def view_bills():
    return render_template('/delivery_app/view-bills.html')
