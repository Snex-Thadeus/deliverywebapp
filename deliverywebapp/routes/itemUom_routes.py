from flask import render_template, flash, redirect, url_for, request, json
from deliverywebapp.forms.forms import DefineItemUomForm
from deliverywebapp import app
from deliverywebapp.utility import AlchemyEncoder
from deliverywebapp.models.models import *

unitOfMeasureDropDownSchema = UnitOfMeasureSchema(many=True)

rawMaterialDropDownSchema = MaterialItemSchema(many=True)


@app.route('/delivery_app/search-view-item-uom', methods=['GET', 'POST'])
def search_view_item_uom():
    searchbox = request.form.get('text')
    try:
        if searchbox != "":
            item_uom = db.session.execute('SELECT m.Description as MaterialItem , u.ShortDescription as UnitOfMeasure from item_uom_tb i INNER JOIN  material_items_tb m ON i.MaterialItemsTbID = m.ID INNER JOIN unit_of_measure_tb u ON i.UnitOfMeasureTbID  = u.ID'
                                         ' WHERE m.Description LIKE "%' + searchbox + '%"')
            item_uom_rows = [dict(row) for row in item_uom]
            return json.dump(item_uom_rows, cls=AlchemyEncoder)
        else:
            item_uom = db.session.execute('SELECT m.Description as MaterialItem , u.ShortDescription as UnitOfMeasure from item_uom_tb i INNER JOIN  material_items_tb m ON i.MaterialItemsTbID = m.ID INNER JOIN unit_of_measure_tb u ON i.UnitOfMeasureTbID  = u.ID;')
            item_uom_rows = [dict(row) for row in item_uom]
            return json.dump(item_uom_rows, cls=AlchemyEncoder)
    except Exception as ex:
        flash(ex, 'danger')


@app.route('/delivery_app/define-item-uom', methods=['GET', 'POST'])
def define_item_uom():
    form = DefineItemUomForm()
    try:
        if request.method == 'GET':
            raw_material_choices = [(-1, 'Choose raw material')]
            raw_materials = MaterialItemsTb.query.all()
            raw_material_dd = rawMaterialDropDownSchema.dump(raw_materials)
            for i in raw_material_dd:
                raw_material_choices.append((i['ID'], i['Description']))
            form.chooseRawMaterail.choices = raw_material_choices

            unit_of_measure_choices = [(-1, 'Choose unit of measure')]
            unit_of_measures = UnitOfMeasureTb.query.all()
            unit_of_measure_dd = unitOfMeasureDropDownSchema.dump(unit_of_measures)
            for i in unit_of_measure_dd:
                unit_of_measure_choices.append((int(i['ID']), i['Description']))
            form.chooseUnitOfMeasure.choices = unit_of_measure_choices
        elif request.method == "POST":
            item_uom = ItemUomTb(
                form.chooseRawMaterail.data,
                form.chooseUnitOfMeasure.data
            )
            db.session.add(item_uom)
            db.session.commit()

            flash(
                'Item Uom: "' + form.chooseUnitOfMeasure.data + '", "' + form.chooseUnitOfMeasure.data + '" is successfully added ',
                'success')
            return redirect(url_for('view_orders', form=form))

    except Exception as ex:
        flash(ex, 'danger')

    return render_template('./delivery_app/define-item-uom.html', form=form)


@app.route('/delivery_app/define-item-uom-edit/<string:id>', methods=['GET', 'POST'])
def edit_define_item_uom(id):
    form = DefineItemUomForm()
    if not form.validate_on_submit():
        try:
            item_uom = ItemUomTb.query.get(id)
            form.description.data = item_uom.Description
        except Exception as ex:
            flash(ex, 'danger')
    elif form.validate_on_submit():
        try:
            item_uom_tb_edit = db.session.query(UnitOfMeasureTb).filter(UnitOfMeasureTb.ID == id).one()
            before_item_uom = item_uom_tb_edit.Description

            item_uom_tb_edit.Description = form.description.data

            db.session.commit()

            if before_item_uom != form.description.data:
                flash(
                    '\n\t "' + before_item_uom + '" successfully edited to "' + form.description.data + '"',
                    'success')

        except Exception as ex:
            flash(ex, 'danger')

        return redirect(url_for('viewItemUom', form=form))

    return render_template('/delivery_app/define-item-uom.html', form=form)


@app.route('/delivery_app/view-item-uom')
def view_item_uom():
    return render_template('/delivery_app/view-item-uom.html')
