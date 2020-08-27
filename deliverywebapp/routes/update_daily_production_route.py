from flask import render_template, flash, redirect, url_for, request, json
from deliverywebapp.forms.forms import UpdateDailyProductionForm
from deliverywebapp import app
from deliverywebapp.utility import AlchemyEncoder
from deliverywebapp.models.models import *

productionActivitiesDropDownSchema = ProductionActivitiesSchema(many=True)

conversionFactorDropDownSchema = ConversionFactorSchema(many=True)


@app.route('/search-daily-production', methods=['POST', 'GET'])
def search_daily_production():
    searchbox = request.form.get('text')
    try:
        if searchbox != "":
            daily_production = UpdateDailyProductionTb.query.filter(
                UpdateDailyProductionTb.Description.like('%' + searchbox + '%')).all()
            return json.dumps(daily_production, cls=AlchemyEncoder)
        else:
            daily_production = UpdateDailyProductionTb.query.all()
            return json.dumps(daily_production, cls=AlchemyEncoder)
    except Exception as ex:
            flash(ex, 'danger')


@app.route('/delivery_app/define-daily-production', methods=['GET', 'POST'])
def define_daily_production():
    form = UpdateDailyProductionForm()
    try:
        if request.method == 'GET':
            production_activities_choices = [(-1, 'Choose production activity')]
            production_activities = ProductionActivitiesTb.query.all()
            production_activities_dd = productionActivitiesDropDownSchema.dump(production_activities)
            for i in production_activities_dd:
                production_activities_choices.append((i['ID'], i['Activity']))
            form.chooseProductionActivity.choices = production_activities_choices

            measure_choices = [(-1, 'Choose Measure')]
            measure = ConversionFactorTb.query.all()
            measure_dd = conversionFactorDropDownSchema.dump(measure)
            for i in measure_dd:
                measure_choices.append((int(i['ID']), i['MeasurementDescription']))
            form.chooseMeasure.choices = measure_choices
        elif request.method == "POST":
            item_uom = UpdateDailyProductionTb(
                form.chooseProductionActivity.data,
                form.chooseMeasure.data,
                form.quantity.data,
                form.date.data
            )
            db.session.add(item_uom)
            db.session.commit()

            flash(
                'Item Uom: "' + form.chooseProductionActivity.data + '", "' + form.chooseMeasure.data + '" is successfully added ',
                'success')
            return redirect(url_for('define_daily_production', form=form))

    except Exception as ex:
        flash(ex, 'danger')

    return render_template('/delivery_app/define-daily-production.html', form=form)

