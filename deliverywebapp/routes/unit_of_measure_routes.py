from flask import render_template, flash, redirect, url_for, request, jsonify, json
from deliverywebapp.forms.forms import LoginForm, DefineProductsForm, DefineAreasForm, DefineBillsForm, \
    DefineExpenseCategoriesForm, DefineUnitOfMeasureForm
from deliverywebapp import app, db
from deliverywebapp.forms.search_forms import SearchViewProductsForm
from deliverywebapp.models.models import ProductTb
from flask_sqlalchemy import sqlalchemy
from sqlalchemy import update
from deliverywebapp.utility import AlchemyEncoder
from deliverywebapp.models.models import *


@app.route('/search_view_unit_of_measure', methods=['POST', 'GET'])
def sarchViewUnitOfMeasure():
    searchbox = request.form.get('text')
    try:
        if searchbox != "":
            unitOfMeasure = UnitOfMeasureTb.query.filter(
                UnitOfMeasureTb.Description.like('%' + searchbox + '%')).all()
            return json.dumps(unitOfMeasure, cls=AlchemyEncoder)
        else:
            unitOfMeasure = UnitOfMeasureTb.query.all()
            return json.dumps(unitOfMeasure, cls=AlchemyEncoder)
    except sqlalchemy.exc.SQLAlchemyError as ex:
        flash(ex, ' danger')


@app.route('/delivery_app/define-unit-of-measure', methods=['GET', 'POST'])
def defineUnitOfMeasure():
    form = DefineUnitOfMeasureForm()
    if form.validate_on_submit():
        try:
            unitOfMeasure = UnitOfMeasureTb(form.description.data, form.shortDescription.data)
            db.session.add(unitOfMeasure)
            db.session.commit()

            flash('Unit of Measure: "' + form.description.data + '" successfully added', 'success')
            return redirect(url_for('viewUnitofMeasure', form=form))

        except sqlalchemy.exc.SQLAlchemyError as ex:
            flash(ex, ' danger')

    return render_template('./delivery_app/define-unit-of-measure.html', form=form)


@app.route('/delivery_app/define-unit-of-measure-edit/<string:id>', methods=['POST', 'GET'])
def editDefineUnitOfMeasure(id):
    form = DefineUnitOfMeasureForm()
    if not form.validate_on_submit():
        try:
            unitOfMeasure = UnitOfMeasureTb.query.get(id)
            form.description.data = unitOfMeasure.Description
            form.shortDescription.data = unitOfMeasure.ShortDescription
        except Exception as ex:
            flash(ex, 'danger')
    elif form.validate_on_submit():
        try:
            UnitOfMeasureTbEdit = db.session.query(UnitOfMeasureTb).filter(UnitOfMeasureTb.ID == id).one()
            BeforeDescription = UnitOfMeasureTbEdit.Description
            BeforeShortDescription = UnitOfMeasureTbEdit.ShortDescription

            UnitOfMeasureTbEdit.Description = form.description.data
            UnitOfMeasureTbEdit.ShortDescription = form.shortDescription.data

            db.session.commit()

            if BeforeDescription != form.description.data:
                flash(
                    '\n\t "' + BeforeDescription + '" successfully edited to "' + form.description.data + '"',
                    'success')

            if BeforeShortDescription != form.shortDescription.data:
                flash(
                    '\n\t "' + BeforeShortDescription + '" successfully edited to "' + form.shortDescription.data + '"',
                    'success')
        except sqlalchemy.exc.SQLAlchemyError as ex:
            flash(ex, ' danger')

        return redirect(url_for('viewUnitofMeasure', form=form))

    return render_template('./delivery_app/define-unit-of-measure.html', form=form)


@app.route('/delivery_app/view-unit-of-measure')
def viewUnitofMeasure():
    return render_template('./delivery_app/view-unit-of-measure.html')
