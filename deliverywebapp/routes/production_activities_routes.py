from flask import render_template, flash, redirect, url_for, request, json
from deliverywebapp.forms.forms import DefineProductionActivitiesForm
from deliverywebapp import app
from deliverywebapp.utility import AlchemyEncoder
from deliverywebapp.models.models import *


@app.route('/search-view-production-activities-item', methods=['POST', 'GET'])
def search_view_production_activities():
    searchbox = request.form.get('text')
    try:
        if searchbox != "":
            production_activities = ProductionActivitiesTb.query.filter(
                ProductionActivitiesTb.Description.like('%' + searchbox + '%')).all()
            return json.dumps(production_activities, cls=AlchemyEncoder)
        else:
            production_activities = ProductionActivitiesTb.query.all()
            return json.dumps(production_activities, cls=AlchemyEncoder)
    except Exception as ex:
            flash(ex, 'danger')


@app.route('/delivery_app/define-production-activities_item', methods=['GET', 'POST'])
def define_production_activities():
    form = DefineProductionActivitiesForm()
    if form.validate_on_submit():
        try:
            production_activity = ProductionActivitiesTb(form.activity.data)
            db.session.add(production_activity)
            db.session.commit()

            flash('Production Activity: "' + form.activity.data + '" successfully added', 'success')
            return redirect(url_for('view_production_activities', form=form))
        except Exception as ex:
            flash(ex, 'danger')

    return render_template('/delivery_app/define-production-activities.html', form=form)


@app.route('/delivery_app/define-production-activities-edit/<string:id>', methods=['GET', 'POST'])
def edit_define_production_activities(id):
    form = DefineProductionActivitiesForm()
    if not form.validate_on_submit():
        try:
            production_activities = ProductionActivitiesTb.query.get(id)
            form.description.data = production_activities.Description
        except Exception as ex:
            flash(ex, 'danger')
    elif form.validate_on_submit():
        try:
            production_activities_tb_edit = db.session.query(ProductionActivitiesTb).filter(ProductionActivitiesTb.ID == id).one()
            before_production_activities = production_activities_tb_edit.Description

            production_activities_tb_edit.Description = form.activity.data

            db.session.commit()

            if before_production_activities != form.activity.data:
                flash(
                    '\n\t "' + before_production_activities + '" successfully edited to "' + form.activity.data + '"',
                    'success')

        except Exception as ex:
            flash(ex, 'danger')

        return redirect(url_for('view_production_activities', form=form))

    return render_template('/delivery_app/define-production-activities.html', form=form)


@app.route('/delivery_app/view-production-activities')
def view_production_activities():
    return render_template('/delivery_app/view-production-activities.html')
