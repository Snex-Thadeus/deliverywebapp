from flask import render_template, flash, request, json
from deliverywebapp.forms.forms import ReceiveMaterialQuantitiesForm
from deliverywebapp import app
from deliverywebapp.utility import AlchemyEncoder
from deliverywebapp.models.models import *


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


MaterialDropDownSchema = MaterialItemSchema(many=True)


class MaterialQuantitiesSchema(ma.Schema):
    class Meta:
        fields = ("ID", "material")


MaterialQuantitiesSchema = MaterialQuantitiesSchema(many=True)


@app.route('/delivery_app/define-material_quantities', methods=['GET', 'POST'])
def define_material_quantities():
    form = ReceiveMaterialQuantitiesForm()
    if request.method == 'GET':
        material_choices = [(-1, 'Choose  material')]
        materials = ItemUomTb.query.all()
        material_id = MaterialDropDownSchema.dump(materials)
        for i in material_id:
            material_choices.append((i['ID'], i['Material']))
        form.chooseMaterail.choices = material_choices

    elif request.method == 'POST':
        update_material_quantities = UpdateMaterialQuantitiesTb(
            ItemUomTbID=form.chooseMaterail.data,
            ReceivedDate=form.receivedDate.data,
            Quantity=form.quantity.data

        )
        db.session.add(update_material_quantities)
        db.session.commit()
    render_template('/delivery_app/define-material_quantities.html', form=form)


@app.route('/delivery_app/view-material_quantities')
def view_material_quantities():
    render_template('/delivery_app/view-material_quantities.html')
