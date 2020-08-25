from flask import render_template, flash, redirect, url_for, request, jsonify, json
from deliverywebapp.forms.forms import DefineUnitOfMeasureForm
from deliverywebapp import app
from deliverywebapp.utility import AlchemyEncoder
from deliverywebapp.models.models import *


@app.route('/search_view_unit_of_measure', methods=['POST', 'GET'])
def search_view_unit_of_measure():
    searchbox = request.form.get('text')
    try:
        if searchbox != "":
            unit_of_measure = UnitOfMeasureTb.query.filter(
                UnitOfMeasureTb.Description.like('%' + searchbox + '%')).all()
            return json.dumps(unit_of_measure, cls=AlchemyEncoder)
        else:
            unit_of_measure = UnitOfMeasureTb.query.all()
            return json.dumps(unit_of_measure, cls=AlchemyEncoder)
    except Exception as ex:
        flash(ex, 'danger')


@app.route('/delivery_app/define-unit-of-measure', methods=['GET', 'POST'])
def define_unit_of_measure():
    form = DefineUnitOfMeasureForm()
    if form.validate_on_submit():
        try:
            unit_of_measure = UnitOfMeasureTb(form.description.data, form.shortDescription.data)
            db.session.add(unit_of_measure)
            db.session.commit()

            flash('Unit of Measure: "' + form.description.data + '" successfully added', 'success')
            return redirect(url_for('view_unit_of_measure', form=form))

        except Exception as ex:
            flash(ex, 'danger')

    return render_template('./delivery_app/define-unit-of-measure.html', form=form)


@app.route('/delivery_app/define-unit-of-measure-edit/<string:id>', methods=['POST', 'GET'])
def edit_unit_of_measure(id):
    form = DefineUnitOfMeasureForm()
    if not form.validate_on_submit():
        try:
            unit_of_measure = UnitOfMeasureTb.query.get(id)
            form.description.data = unit_of_measure.Description
            form.shortDescription.data = unit_of_measure.ShortDescription
        except Exception as ex:
            flash(ex, 'danger')
    elif form.validate_on_submit():
        try:
            unit_of_measure_tb_edit = db.session.query(UnitOfMeasureTb).filter(UnitOfMeasureTb.ID == id).one()
            before_description = unit_of_measure_tb_edit.Description
            before_short_description = unit_of_measure_tb_edit.ShortDescription

            unit_of_measure_tb_edit.Description = form.description.data
            unit_of_measure_tb_edit.ShortDescription = form.shortDescription.data

            db.session.commit()

            if before_description != form.description.data:
                flash(
                    '\n\t "' + before_description + '" successfully edited to "' + form.description.data + '"',
                    'success')

            if before_short_description != form.shortDescription.data:
                flash(
                    '\n\t "' + before_short_description + '" successfully edited to "' + form.shortDescription.data + '"',
                    'success')
        except Exception as ex:
            flash(ex, 'danger')

        return redirect(url_for('view_unit_of_measure', form=form))

    return render_template('./delivery_app/define-unit-of-measure.html', form=form)


@app.route('/delivery_app/view-unit-of-measure')
def view_unit_of_measure():
    return render_template('./delivery_app/view-unit-of-measure.html')
