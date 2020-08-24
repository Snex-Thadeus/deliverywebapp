from flask import render_template, request, flash, json
from deliverywebapp import app
from deliverywebapp.forms.forms import ViewDailyProductionForm
from deliverywebapp.models.models import *
from deliverywebapp.utility import AlchemyEncoder


@app.route('/search-daily-production', methods=['POST', 'GET'])
def search_view_daily_production():
    searchbox = request.form.get('text')
    try:
        if searchbox != "":
            daily_production = UpdateDailyProductionTb.query.filter(
                ProductionActivitiesTb.Description.like('%' + searchbox + '%')).all()
            return json.dumps(daily_production, cls=AlchemyEncoder)
        else:
            daily_production = UpdateDailyProductionTb.query.all()
            return json.dumps(daily_production, cls=AlchemyEncoder)
    except Exception as ex:
            flash(ex, 'danger')


@app.route('/delivery_app/view-daily-production', methods=['GET', 'POST'])
def view_daily_production():
    form = ViewDailyProductionForm()

    return render_template('/delivery_app/view-daily-production.html', form=form)

