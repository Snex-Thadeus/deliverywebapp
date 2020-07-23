from flask import render_template, flash, redirect, url_for, request, jsonify, json
from deliverywebapp.forms.forms import LoginForm, DefineProductsForm, DefineAreasForm, DefineBillsForm, \
    DefinePettyCashForm
from deliverywebapp import app, db
from deliverywebapp.forms.search_forms import SearchViewProductsForm
from deliverywebapp.models.models import ProductTb
from flask_sqlalchemy import sqlalchemy
from sqlalchemy import update
from deliverywebapp.utility import AlchemyEncoder, getCleanPriceValue
from deliverywebapp.models.models import *

ACCOUNT = ['Petty Cash']


@app.route('/search_view_petty_cash', methods=['POST', 'GET'])
def searchViewPettyCash():
    searchbox = request.form.get('text')
    try:
        if searchbox != "":
            pettycash = PettyCashTb.query.filter(PettyCashTb.ReceivedFrom.like('%' + searchbox + '%')).all()
            return json.dumps(pettycash, cls=AlchemyEncoder)
        else:
            pettycash = PettyCashTb.query.all()
            return json.dumps(pettycash, cls=AlchemyEncoder)

    except sqlalchemy.exc.SQLAlchemyError as ex:
        flash(ex, ' danger')


@app.route('/delivery_app/define-petty-cash', methods=['GET', 'POST'])
def definePettyCash():
    form = DefinePettyCashForm()
    if request.method == "POST":
        try:

            dateTime = request.form.get('datepicker')

            pettycash = PettyCashTb(form.amountReceived.data, form.dateReceived.data, form.receivedFrom.data,
                                    form.account.data)
            db.session.add(pettycash)
            db.session.commit()

            flash(
                'Petty Cash: An amount of "' + form.amountReceived.data + '" is successfully added and was received '
                                                                          'from "' + form.receivedFrom.data + '"',
                'success')
            return redirect(url_for('viewPettyCash', form=form))
        except sqlalchemy.exc.SQLAlchemyError as ex:
            flash(ex, 'danger')
    elif request.method == 'GET':
        form.account.choices = ACCOUNT

    return render_template('./delivery_app/define-petty-cash.html', form=form)


@app.route('/delivery_app/define-petty-cash-edit/<string:id>', methods=['GET', 'POST'])
def editPettyCash(id):
    form = DefinePettyCashForm()
    if not form.validate_on_submit():

        try:
            pettycash = PettyCashTb.query.get(id)
            form.amountReceived.data = pettycash.AmountReceived
            form.dateReceived.data = pettycash.DateReceived
            form.receivedFrom.data = pettycash.ReceivedFrom
            form.account.data = pettycash.Account
            form.account.default = pettycash.Account
        except Exception as ex:
            flash(ex, ' danger')
    elif form.validate_on_submit():
        try:
            PettyCashTbEdit = db.session.query(PettyCashTb).filter(PettyCashTb.ID == id).one()

            BeforeAmountReceived = PettyCashTbEdit.AmountReceived
            BeforeDateReceived = PettyCashTbEdit.DateReceived
            BeforeReceivedFrom = PettyCashTbEdit.ReceivedFrom
            BeforeAccount = PettyCashTbEdit.Account

            PettyCashTbEdit.AmountReceived = getCleanPriceValue(form.amountReceived.data)
            PettyCashTbEdit.DateReceived = form.dateReceived.data
            PettyCashTbEdit.ReceivedFrom = form.receivedFrom.data
            PettyCashTbEdit.Account = form.account.data

            db.session.commit()

            if BeforeAmountReceived != getCleanPriceValue(form.amountReceived.data):
                flash('\n\t "' + BeforeAmountReceived + '" successfully edited to "' + form.amountReceived.data + '"',
                      'success')
            if BeforeDateReceived != form.dateReceived.data:
                flash('\n\t "' + BeforeDateReceived + '" successfully edited to "' + form.dateReceived.data + '"',
                      'success')
            if BeforeReceivedFrom != form.receivedFrom.data:
                flash('\n\t "' + BeforeReceivedFrom + '" successfully edited to "' + form.receivedFrom.data + '"',
                      'success')
            if BeforeAccount != form.account.data:
                flash('\n\t "' + BeforeAccount + '" successfully edited to "' + form.account.data + '"',
                      'success')

        except Exception as ex:
            flash(ex, 'danger')

        return redirect(url_for('viewBills', form=form))

    return render_template('./delivery_app/define-petty-cash.html', form=form)


@app.route('/delivery_app/view-petty-cash')
def viewPettyCash():
    return render_template('./delivery_app/view-petty-cash.html')
