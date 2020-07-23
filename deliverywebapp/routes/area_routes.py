from flask import render_template, flash, redirect, url_for, request, jsonify, json
from deliverywebapp.forms.forms import LoginForm, DefineProductsForm, DefineAreasForm
from deliverywebapp import app, db
from deliverywebapp.forms.search_forms import SearchViewProductsForm
from deliverywebapp.models.models import ProductTb
from flask_sqlalchemy import sqlalchemy
from sqlalchemy import update
from deliverywebapp.utility import AlchemyEncoder
from deliverywebapp.models.models import *


@app.route('/search_view_areas', methods=['POST', 'GET'])
def searchViewArea():
    searchbox = request.form.get('text')
    try:
        if searchbox != "":
            areas = AreasTb.query.filter(AreasTb.Name.like('%' + searchbox + '%')).all()
            return json.dumps(areas, cls=AlchemyEncoder)
        else:
            areas = AreasTb.query.all()
            return json.dumps(areas, cls=AlchemyEncoder)

    except Exception as ex:
        flash(ex, 'danger')


@app.route('/delivery_app/define-areas', methods=['GET', 'POST'])
def defineAreas():
    form = DefineAreasForm()
    if form.validate_on_submit():
        try:
            data = AreasTb(form.area.data)
            db.session.add(data)
            db.session.commit()
        except Exception as ex:
            flash(ex, 'danger')

        flash('Area: "' + form.area.data + '" successfully added', 'success')
        return redirect(url_for('viewAreas', form=form))
    return render_template('./delivery_app/define-areas.html', form=form)


@app.route('/delivery_app/view-areas')
def viewAreas():
    return render_template('./delivery_app/view-areas.html')


@app.route('/delivery_app/define-areas-edit/<string:id>', methods=['GET', 'POST'])
def editDefineAreas(id):
    form = DefineAreasForm()
    if not form.validate_on_submit():
        try:
            area = AreasTb.query.get(id)
            form.area.data = area.Name

        except Exception as ex:
            flash(ex, 'danger')
    elif form.validate_on_submit():
        try:
            AreasTbEdit = db.session.query(AreasTb).filter(AreasTb.ID == id).one()
            BeforeArea = AreasTbEdit.Name
            AreasTbEdit.Name = form.area.data

            db.session.commit()

            if BeforeArea != form.area.data:
                flash('\n\t "' + BeforeArea + '" successfully edited to "' + form.area.data + '"',
                      'success')

        except Exception as ex:
            flash(ex, 'danger')

        return redirect(url_for('viewAreas', form=form))

    return render_template('./delivery_app/define-areas.html', form=form)
