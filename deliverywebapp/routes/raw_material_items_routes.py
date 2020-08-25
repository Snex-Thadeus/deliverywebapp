from flask import render_template, flash, redirect, url_for, request, jsonify, json
from deliverywebapp.forms.forms import DefineRawMaterialItemsForm
from deliverywebapp import app
from deliverywebapp.utility import AlchemyEncoder
from deliverywebapp.models.models import *


@app.route('/search-view-raw-material-item', methods=['POST', 'GET'])
def search_view_raw_material_items():
    searchbox = request.form.get('text')
    try:
        if searchbox != "":
            raw_materials = MaterialItemsTb.query.filter(
                MaterialItemsTb.Description.like('%' + searchbox + '%')).all()
            return json.dumps(raw_materials, cls=AlchemyEncoder)
        else:
            raw_materials = MaterialItemsTb.query.all()
            return json.dumps(raw_materials, cls=AlchemyEncoder)
    except Exception as ex:
            flash(ex, 'danger')


@app.route('/delivery_app/define-raw-material_item', methods=['GET', 'POST'])
def define_raw_material_items():
    form = DefineRawMaterialItemsForm()
    if form.validate_on_submit():
        try:
            raw_material = MaterialItemsTb(form.description.data)
            db.session.add(raw_material)
            db.session.commit()

            flash('Raw material item: "' + form.description.data + '" successfully added', 'success')
            return redirect(url_for('view_raw_material_items', form=form))
        except Exception as ex:
            flash(ex, 'danger')

    return render_template('./delivery_app/define-raw-material-items.html', form=form)


@app.route('/delivery_app/define-raw-material-item-edit/<string:id>', methods=['GET', 'POST'])
def edit_define_raw_material_items(id):
    form = DefineRawMaterialItemsForm()
    if not form.validate_on_submit():
        try:
            raw_material = MaterialItemsTb.query.get(id)
            form.description.data = raw_material.Description
        except Exception as ex:
            flash(ex, 'danger')
    elif form.validate_on_submit():
        try:
            raw_material_tb_edit = db.session.query(MaterialItemsTb).filter(MaterialItemsTb.ID == id).one()
            before_raw_material = raw_material_tb_edit.Description

            raw_material_tb_edit.Description = form.description.data

            db.session.commit()

            if before_raw_material != form.description.data:
                flash(
                    '\n\t "' + before_raw_material + '" successfully edited to "' + form.description.data + '"',
                    'success')

        except Exception as ex:
            flash(ex, 'danger')

        return redirect(url_for('viewRawMaterialItems', form=form))

    return render_template('/delivery_app/define-raw-material-items.html', form=form)


@app.route('/delivery_app/view-raw-material_items')
def view_raw_material_items():
    return render_template('/delivery_app/view-raw-material-items.html')
