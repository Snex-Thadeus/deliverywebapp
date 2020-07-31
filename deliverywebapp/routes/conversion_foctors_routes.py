from flask import render_template, flash, redirect, url_for, request, jsonify, json
from deliverywebapp.forms.forms import LoginForm, DefineProductsForm, DefineAreasForm, DefineBillsForm, \
    DefineExpenseCategoriesForm, DefineUnitOfMeasureForm, DefineItemUom, DefineConversionFactors
from deliverywebapp import app, db
from deliverywebapp.forms.search_forms import SearchViewProductsForm
from deliverywebapp.models.models import ProductTb
from flask_sqlalchemy import sqlalchemy
from sqlalchemy import update
from deliverywebapp.utility import AlchemyEncoder
from deliverywebapp.models.models import *


@app.route('/delivery_app/search-view-conversion-factors', methods=['GET', 'POST'])
def searchViewConversionFactors():
    searchbox = request.form.get('text')
    try:
        if searchbox != "":
            conversionFactor = db.session.execute('SELECT c.ID ,m.Description as MaterialItem ,CONCAT( m.Description + u.ShortDescription) AS ItemUom, c.MeasurementDescription,c.DescribeQuantity from conversion_factor_tb c INNER JOIN item_uom_tb i ON c.ItemUomTbID = i.ID  INNER JOIN  material_items_tb m ON m.ID = c.MaterialItemsTbID INNER JOIN unit_of_measure_tb u ON i.UnitOfMeasureTbID  = u.ID;')
            conversionFactorRows = [dict(row) for row in conversionFactor]
            return json.dump(conversionFactorRows, cls=AlchemyEncoder)
        else:
            conversionFactor = db.session.execute('SELECT c.ID ,m.Description as MaterialItem ,CONCAT( m.Description + u.ShortDescription) AS ItemUom, c.MeasurementDescription,c.DescribeQuantity from conversion_factor_tb c INNER JOIN item_uom_tb i ON c.ItemUomTbID = i.ID  INNER JOIN  material_items_tb m ON m.ID = c.MaterialItemsTbID INNER JOIN unit_of_measure_tb u ON i.UnitOfMeasureTbID  = u.ID;')
            conversionFactorRows = [dict(row) for row in conversionFactor]
            return json.dump(conversionFactorRows, cls=AlchemyEncoder)

    except Exception as ex:
        flash(ex, 'danger')

rawMaterialDropDownSchema = MaterailItemSchema(many=True)


class ConversionFactorsSchema(ma.Schema):
    class Meta:
        fields = ("ID", "ItemUom")


conversionFactorsSchema = ConversionFactorsSchema(many=True)


@app.route('/delivery_app/define-conversion-factors', methods=['GET', 'POST'])
def defineConversionFactors():
    form = DefineConversionFactors()
    if request.method == 'GET':
        rawMaterialChoices = [(-1, 'Choose raw material')]
        rawMaterials = MaterialItemsTb.query.all()
        rawMaterialDD = rawMaterialDropDownSchema.dump(rawMaterials)
        for i in rawMaterialDD:
            rawMaterialChoices.append((i['ID'], i['Description']))
        form.chooseRawMaterail.choices = rawMaterialChoices

        itemUomChoices = [(-1, 'Choose conversion factors')]
        itemUoms = db.session.execute(
            'SELECT i.ID ,CONCAT( m.Description + u.ShortDescription) AS ItemUom from item_uom_tb i INNER JOIN  material_items_tb m ON i.MaterialItemsTbID = m.ID INNER JOIN unit_of_measure_tb u ON i.UnitOfMeasureTbID  = u.ID')
        # itemUomsRaw = [dict(row) for row in itemUoms]
        itemUomsDD = conversionFactorsSchema.dump(itemUoms)
        for i in itemUomsDD:
            itemUomChoices.append((i['ID'], i['ItemUom']))
        form.chooseItemUom.choices = itemUomChoices

    elif request.method == 'POST':
        conversionFactor = ConversionFactorTb(
            MaterialItemsTbID=form.chooseRawMaterail.data,
            ItemUomTbID=form.chooseItemUom.data,
            MeasurementDescription=form.measurementDescription.data,
            DescribeQuantity=form.quantity.data
        )
        db.session.add(conversionFactor)
        db.session.commit()
    render_template('./delivery_app/define-conversion_factors.html', form=form)


@app.route('/delivery_app/view-conversion-factors')
def viewConversionFactors():
    render_template('./delivery_app/view-conversion-factors.html')
