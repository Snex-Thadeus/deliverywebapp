from flask import render_template, flash, request, json, redirect, url_for, jsonify
from deliverywebapp.forms.forms import ReceiveMaterialQuantitiesForm
from deliverywebapp import app
from deliverywebapp.utility import AlchemyEncoder
from deliverywebapp.models.models import *

item_uom_schema = ItemUomSchema(many=True)


@app.route('/item-uom-autocomplete', methods=['GET'])
def auto_complete():
    item_uom_tb = ItemUomTb.query.all()
    return jsonify(item_uom_schema.dump(item_uom_tb))


@app.route('/delivery_app/search_material_quantities', methods=['GET', 'POST'])
def search_material_quantities():
    searchbox = request.form.get('text')
    try:
        if searchbox != "":
            material_quantities = db.session.execute('SELECT c.ID ,m.Description as Material ,CONCAT( m.Description) AS ItemUom, c.MaterialDescription from update_material_quantities_tb INNER JOIN  item_uom_tb m ON m.ID = c.MaterialItemsTbID INNER JOIN unit_of_measure_tb u ON i.UnitOfMeasureTbID  = u.ID;')
            material_quantities_rows = [dict(row) for row in material_quantities]
            return json.dump(material_quantities_rows, cls=AlchemyEncoder)
        else:
            material_quantities = db.session.execute('SELECT c.ID ,m.Description as Material ,CONCAT( m.Description) AS ItemUom, c.MaterialDescription from update_material_quantities_tb INNER JOIN  item_uom_tb m ON m.ID = c.MaterialItemsTbID INNER JOIN unit_of_measure_tb u ON i.UnitOfMeasureTbID  = u.ID;')
            material_quantities_rows = [dict(row) for row in material_quantities]
            return json.dump(material_quantities_rows, cls=AlchemyEncoder)

    except Exception as ex:
        flash(ex, 'danger')


ItemUomDropDownSchema = ItemUomSchema(many=True)


@app.route('/delivery_app/define-material-quantities', methods=['GET', 'POST'])
def define_material_quantities():
    form = ReceiveMaterialQuantitiesForm()
    try:
        if request.method == 'GET':
            material_choices = [(-1, 'Choose  material')]
            materials = ItemUomTb.query.all()
            material_id = ItemUomDropDownSchema.dump(materials)
            for i in material_id:
                material_choices.append((i['ID'], i['MaterialItemsTbID'],  i['UnitOfMeasureTbID']))
            form.selectMaterial.choices = material_choices

        elif request.method == 'POST':
            update_material_quantities = UpdateMaterialQuantitiesTb(
                form.selectMaterial.data,
                form.selectReceivedDate.data,
                form.unitofMeasure.data,
                form.quantity.data

            )
            db.session.add(update_material_quantities)
            db.session.commit()
            flash(
                'Item Uom: "' + form.selectMaterial.data + '", "' + form.quantity.data + '" is successfully added ',
                'success')
            return redirect(url_for('view_material_quantities', form=form))

    except Exception as ex:
        flash(ex, 'danger')
        return render_template('/delivery_app/define-material-quantities.html', form=form)


@app.route('/delivery_app/view-material-quantities')
def view_material_quantities():
    return render_template('/delivery_app/view-material-quantities.html')
