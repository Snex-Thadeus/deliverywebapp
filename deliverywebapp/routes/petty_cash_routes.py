from flask import render_template, flash, redirect, url_for, request, jsonify, json
from deliverywebapp.forms.forms import DefinePettyCashForm
from deliverywebapp import app
from flask_sqlalchemy import sqlalchemy
from deliverywebapp.utility import AlchemyEncoder, get_clean_price_value
from deliverywebapp.models.models import *

ACCOUNT = ['Petty Cash']


@app.route('/search_view_petty_cash', methods=['POST', 'GET'])
def search_view_petty_cash():
    searchbox = request.form.get('text')
    try:
        if searchbox != "":
            petty_cash = PettyCashTb.query.filter(PettyCashTb.ReceivedFrom.like('%' + searchbox + '%')).all()
            return json.dumps(petty_cash, cls=AlchemyEncoder)
        else:
            petty_cash = PettyCashTb.query.all()
            return json.dumps(petty_cash, cls=AlchemyEncoder)

    except sqlalchemy.exc.SQLAlchemyError as ex:
        flash(ex, ' danger')


@app.route('/delivery_app/define-petty-cash', methods=['GET', 'POST'])
def define_petty_cash():
    form = DefinePettyCashForm()
    if request.method == "POST":
        try:

            date_time = request.form.get('datepicker')

            petty_cash = PettyCashTb(form.amountReceived.data, form.dateReceived.data, form.receivedFrom.data,
                                    form.account.data)
            db.session.add(petty_cash)
            db.session.commit()

            flash(
                'Petty Cash: An amount of "' + form.amountReceived.data + '" is successfully added and was received '
                                                                          'from "' + form.receivedFrom.data + '"',
                'success')
            return redirect(url_for('view_petty_cash', form=form))
        except sqlalchemy.exc.SQLAlchemyError as ex:
            flash(ex, 'danger')
    elif request.method == 'GET':
        form.account.choices = ACCOUNT

    return render_template('./delivery_app/define-petty-cash.html', form=form)


@app.route('/delivery_app/define-petty-cash-edit/<string:id>', methods=['GET', 'POST'])
def edit_petty_cash(id):
    form = DefinePettyCashForm()
    if not form.validate_on_submit():

        try:
            petty_cash = PettyCashTb.query.get(id)
            form.amountReceived.data = petty_cash.AmountReceived
            form.dateReceived.data = petty_cash.DateReceived
            form.receivedFrom.data = petty_cash.ReceivedFrom
            form.account.data = petty_cash.Account
            form.account.default = petty_cash.Account
        except Exception as ex:
            flash(ex, ' danger')
    elif form.validate_on_submit():
        try:
            petty_cash_tb_edit = db.session.query(PettyCashTb).filter(PettyCashTb.ID == id).one()

            before_amount_received = petty_cash_tb_edit.AmountReceived
            before_date_received = petty_cash_tb_edit.DateReceived
            before_received_from = petty_cash_tb_edit.ReceivedFrom
            before_account = petty_cash_tb_edit.Account

            petty_cash_tb_edit.AmountReceived = get_clean_price_value(form.amountReceived.data)
            petty_cash_tb_edit.DateReceived = form.dateReceived.data
            petty_cash_tb_edit.ReceivedFrom = form.receivedFrom.data
            petty_cash_tb_edit.Account = form.account.data

            db.session.commit()

            if before_amount_received != get_clean_price_value(form.amountReceived.data):
                flash('\n\t "' + before_amount_received + '" successfully edited to "' + form.amountReceived.data + '"',
                      'success')
            if before_date_received != form.dateReceived.data:
                flash('\n\t "' + before_date_received + '" successfully edited to "' + form.dateReceived.data + '"',
                      'success')
            if before_received_from != form.receivedFrom.data:
                flash('\n\t "' + before_received_from + '" successfully edited to "' + form.receivedFrom.data + '"',
                      'success')
            if before_account != form.account.data:
                flash('\n\t "' + before_account + '" successfully edited to "' + form.account.data + '"',
                      'success')

        except Exception as ex:
            flash(ex, 'danger')

        return redirect(url_for('viewBills', form=form))

    return render_template('./delivery_app/define-petty-cash.html', form=form)


@app.route('/delivery_app/view-petty-cash')
def view_petty_cash():
    return render_template('./delivery_app/view-petty-cash.html')
