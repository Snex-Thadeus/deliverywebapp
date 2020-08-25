from flask import render_template, flash, redirect, url_for, request, jsonify, json
from deliverywebapp.forms.forms import DefineConversionFactorsForm
from deliverywebapp import app
from deliverywebapp.utility import AlchemyEncoder
from deliverywebapp.models.models import *


@app.route('/delivery_app/search-view-conversion-factors', methods=['GET', 'POST'])
def search_view_conversion_factors():
    searchbox = request.form.get('text')
    try:
        if searchbox != "":
            conversion_factor = db.session.execute('SELECT c.ID ,m.Description as MaterialItem ,CONCAT( m.Description + u.ShortDescription) AS ItemUom, c.MeasurementDescription,c.DescribeQuantity from conversion_factor_tb c INNER JOIN item_uom_tb i ON c.ItemUomTbID = i.ID  INNER JOIN  material_items_tb m ON m.ID = c.MaterialItemsTbID INNER JOIN unit_of_measure_tb u ON i.UnitOfMeasureTbID  = u.ID;')
            conversion_factor_rows = [dict(row) for row in conversion_factor]
            return json.dump(conversion_factor_rows, cls=AlchemyEncoder)
        else:
            conversion_factor = db.session.execute('SELECT c.ID ,m.Description as MaterialItem ,CONCAT( m.Description + u.ShortDescription) AS ItemUom, c.MeasurementDescription,c.DescribeQuantity from conversion_factor_tb c INNER JOIN item_uom_tb i ON c.ItemUomTbID = i.ID  INNER JOIN  material_items_tb m ON m.ID = c.MaterialItemsTbID INNER JOIN unit_of_measure_tb u ON i.UnitOfMeasureTbID  = u.ID;')
            conversion_factor_rows = [dict(row) for row in conversion_factor]
            return json.dump(conversion_factor_rows, cls=AlchemyEncoder)

    except Exception as ex:
        flash(ex, 'danger')


rawMaterialDropDownSchema = MaterialItemSchema(many=True)


UnitOfMeasureDropDownSchema = UnitOfMeasureSchema(many=True)


@app.route('/delivery_app/define-conversion-factors', methods=['GET', 'POST'])
def define_conversion_factors():
    form = DefineConversionFactorsForm()
    try:
        if request.method == 'GET':
            raw_material_choices = [(-1, 'Choose raw material')]
            raw_materials = MaterialItemsTb.query.all()
            raw_material_dd = rawMaterialDropDownSchema.dump(raw_materials)
            for i in raw_material_dd:
                raw_material_choices.append((i['ID'], i['Description']))
            form.chooseRawMaterial.choices = raw_material_choices

            item_uom_choices = [(-1, 'Choose conversion factors')]
            item_uoms = UnitOfMeasureTb.query.all()
            item_uoms_dd = UnitOfMeasureDropDownSchema.dump(item_uoms)
            for i in item_uoms_dd:
                item_uom_choices.append((i['ID'], i['Description']))
            form.chooseItemUom.choices = item_uom_choices
        #item_uoms = db.session.execute(
            #'SELECT i.ID ,CONCAT( m.Description + u.ShortDescription) AS ItemUom from item_uom_tb i INNER JOIN  material_items_tb m ON i.MaterialItemsTbID = m.ID INNER JOIN unit_of_measure_tb u ON i.UnitOfMeasureTbID  = u.ID')
        # itemUomsRaw = [dict(row) for row in itemUoms]

        elif request.method == 'POST':
            conversion_factor = ConversionFactorTb(
             form.chooseRawMaterial.data,
             form.chooseItemUom.data,
             form.measurementDescription.data,
             form.quantity.data
             )
            db.session.add(conversion_factor)
            db.session.commit()
            flash(
                'Item Uom: "' + form.chooseRawMaterial.data + '", "' + form.chooseItemUom.data + '" is successfully added ',
                'success')
            return redirect(url_for('view_conversion_factors', form=form))

    except Exception as ex:
        flash(ex, 'danger')

    return render_template('/delivery_app/define-conversion_factors.html', form=form)


@app.route('/delivery_app/view-conversion-factors')
def view_conversion_factors():
    return render_template('./delivery_app/view-conversion-factors.html')
