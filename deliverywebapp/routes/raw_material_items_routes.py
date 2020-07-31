from flask import render_template, flash, redirect, url_for, request, jsonify, json
from deliverywebapp.forms.forms import LoginForm, DefineProductsForm, DefineAreasForm, DefineBillsForm, \
    DefineRawMaterialItemsForm
from deliverywebapp import app, db
from deliverywebapp.forms.search_forms import SearchViewProductsForm
from deliverywebapp.models.models import ProductTb
from flask_sqlalchemy import sqlalchemy
from sqlalchemy import update
from deliverywebapp.utility import AlchemyEncoder
from deliverywebapp.models.models import *


@app.route('/search-view-raw-material-item', methods=['POST', 'GET'])
def searchViewRawMeterialItems():
    searchbox = request.form.get('text')
    try:
        if searchbox != "":
            rawMaterials = MaterialItemsTb.query.filter(
                MaterialItemsTb.Description.like('%' + searchbox + '%')).all()
            return json.dumps(rawMaterials, cls=AlchemyEncoder)
        else:
            rawMaterials = MaterialItemsTb.query.all()
            return json.dumps(rawMaterials, cls=AlchemyEncoder)
    except Exception as ex:
            flash(ex, 'danger')


@app.route('/delivery_app/define-raw-material_item', methods=['GET', 'POST'])
def defineRawMaterialItem():
    form = DefineRawMaterialItemsForm()
    if form.validate_on_submit():
        try:
            rawMaterial = MaterialItemsTb(form.description.data)
            db.session.add(rawMaterial)
            db.session.commit()

            flash('Raw material item: "' + form.description.data + '" successfully added', 'success')
            return redirect(url_for('viewRawMaterialItems', form=form))
        except Exception as ex:
            flash(ex, 'danger')

    return render_template('./delivery_app/define-raw-material-items.html', form=form)


@app.route('/delivery_app/define-raw-material-item-edit/<string:id>', methods=['GET', 'POST'])
def editDefineRawMeterialItem(id):
    form = DefineRawMaterialItemsForm()
    if not form.validate_on_submit():
        try:
            rawMaterial = MaterialItemsTb.query.get(id)
            form.description.data = rawMaterial.Description
        except Exception as ex:
            flash(ex, 'danger')
    elif form.validate_on_submit():
        try:
            rawMaterialTbEdit = db.session.query(MaterialItemsTb).filter(MaterialItemsTb.ID == id).one()
            BeforerawMaterial = rawMaterialTbEdit.Description

            rawMaterialTbEdit.Description = form.description.data

            db.session.commit()

            if BeforerawMaterial != form.description.data:
                flash(
                    '\n\t "' + BeforerawMaterial + '" successfully edited to "' + form.description.data + '"',
                    'success')

        except Exception as ex:
            flash(ex, 'danger')

        return redirect(url_for('viewRawMaterialItems', form=form))

    return render_template('./delivery_app/define-raw-material-items.html', form=form)


@app.route('/delivery_app/view-raw-material_items')
def viewRawMaterialItems():
    return render_template('./delivery_app/view-raw-material-items.html')
