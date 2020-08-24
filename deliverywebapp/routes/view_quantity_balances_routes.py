from flask import render_template, flash, json, request
from deliverywebapp import app
from deliverywebapp.forms.forms import ViewQuantityBalancesForm
from deliverywebapp.utility import AlchemyEncoder
from deliverywebapp.models.models import *


@app.route('/search_view_quantity_balances', methods=['POST', 'GET'])
def search_view_quantity_balances():
    searchbox = request.form.get('text')
    try:
        if searchbox != "":
            quantity_balances = ViewDailyProductionTb.query.filter(
                ViewDailyProductionTb.Material.like('%' + searchbox + '%')).all()
            return json.dumps(quantity_balances, cls=AlchemyEncoder)
        else:
            quantity_balances = ViewDailyProductionTb.query.all()
            return json.dumps(quantity_balances, cls=AlchemyEncoder)

    except Exception as ex:
            flash(ex, 'danger')


@app.route('/delivery_app/view-quantity-balances', methods=['GET', 'POST'])
def view_quantity_balances():
    form = ViewQuantityBalancesForm()

    return render_template('/delivery_app/view-quantity-balances.html', form=form)

