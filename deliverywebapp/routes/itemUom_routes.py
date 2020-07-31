from flask import render_template, flash, redirect, url_for, request, jsonify, json
from deliverywebapp.forms.forms import LoginForm, DefineProductsForm, DefineAreasForm, DefineBillsForm, \
    DefineExpenseCategoriesForm, DefineUnitOfMeasureForm, DefineItemUom
from deliverywebapp import app, db
from deliverywebapp.forms.search_forms import SearchViewProductsForm
from deliverywebapp.models.models import ProductTb
from flask_sqlalchemy import sqlalchemy
from sqlalchemy import update
from deliverywebapp.utility import AlchemyEncoder
from deliverywebapp.models.models import *

unitOfMeasureDropDownSchema = UnitOfMeasureSchema(many=True)

rawMaterialDropDownSchema = MaterailItemSchema(many=True)


@app.route('/delivery_app/search-view-item-uom', methods=['GET', 'POST'])
def searchViewItemUom():
    searchbox = request.form.get('text')
    try:
        if searchbox != "":
            itemUom = db.session.execute('SELECT m.Description as MaterialItem , u.ShortDescription as UnitOfMeasure from item_uom_tb i INNER JOIN  material_items_tb m ON i.MaterialItemsTbID = m.ID INNER JOIN unit_of_measure_tb u ON i.UnitOfMeasureTbID  = u.ID'
                                         ' WHERE m.Description LIKE "%' + searchbox + '%"')
            itemUomRows = [dict(row) for row in itemUom]
            return json.dump(itemUomRows, cls=AlchemyEncoder)
        else:
            itemUom = db.session.execute('SELECT m.Description as MaterialItem , u.ShortDescription as UnitOfMeasure from item_uom_tb i INNER JOIN  material_items_tb m ON i.MaterialItemsTbID = m.ID INNER JOIN unit_of_measure_tb u ON i.UnitOfMeasureTbID  = u.ID;')
            itemUomRows = [dict(row) for row in itemUom]
            return json.dump(itemUomRows, cls=AlchemyEncoder)
    except Exception as ex:
        flash(ex, 'danger')
@app.route('/delivery_app/define-item-uom', methods=['GET', 'POST'])
def defineItemUom():
    form = DefineItemUom()
    try:
        if request.method == 'GET':
            rawMaterialChoices = [(-1, 'Choose raw material')]
            rawMaterials = MaterialItemsTb.query.all()
            rawMaterialDD = rawMaterialDropDownSchema.dump(rawMaterials)
            for i in rawMaterialDD:
                rawMaterialChoices.append((i['ID'], i['Description']))
            form.chooseRawMaterail.choices = rawMaterialChoices

            unitOfMeasureChoices = [(-1, 'Choose unit of measure')]
            unitOfMeasures = UnitOfMeasureTb.query.all()
            unitOfMeasureDD = unitOfMeasureDropDownSchema.dump(unitOfMeasures)
            for i in unitOfMeasureDD:
                unitOfMeasureChoices.append((int(i['ID']), i['Description']))
            form.chooseUnitOfMeasure.choices = unitOfMeasureChoices
        elif request.method == "POST":
            itemUom = ItemUomTb(
                form.chooseRawMaterail.data,
                form.chooseUnitOfMeasure.data
            )
            db.session.add(itemUom)
            db.session.commit()

            flash(
                'Item Uom: "' + form.chooseUnitOfMeasure.data + '", "' + form.chooseUnitOfMeasure.data + '" is successfully added ',
                'success')
            return redirect(url_for('viewOrders', form=form))

    except Exception as ex:
        flash(ex, 'danger')

    return render_template('./delivery_app/define-item-uom.html', form=form)


@app.route('/delivery_app/view-item-uom')
def viewItemUom():
    return render_template('./delivery_app/view-item-uom.html')
