from flask import render_template, flash, redirect, url_for, request, json
from deliverywebapp.forms.forms import DefinePackagingMaterialsForm
from deliverywebapp import app
from deliverywebapp.utility import AlchemyEncoder
from deliverywebapp.models.models import *


@app.route('/search-view-packing-materials', methods=['POST', 'GET'])
def search_view_packing_materials():
    searchbox = request.form.get('text')
    try:
        if searchbox != "":
            packing_materials = PackagingMaterialsTb.query.filter(
                PackagingMaterialsTb.Description.like('%' + searchbox + '%')).all()
            return json.dumps(packing_materials, cls=AlchemyEncoder)
        else:
            packing_materials = PackagingMaterialsTb.query.all()
            return json.dumps(packing_materials, cls=AlchemyEncoder)
    except Exception as ex:
            flash(ex, 'danger')


@app.route('/delivery_app/define-packing-materials', methods=['GET', 'POST'])
def define_packing_materials():
    form = DefinePackagingMaterialsForm()
    if form.validate_on_submit():
        try:
            packing_materials = PackagingMaterialsTb(form.description.data)
            db.session.add(packing_materials)
            db.session.commit()

            flash('Packing Material: "' + form.description.data + '" successfully added', 'success')
            return redirect(url_for('define_packing_materials', form=form))
        except Exception as ex:
            flash(ex, 'danger')

    return render_template('/delivery_app/define-packing-materials.html', form=form)


@app.route('/delivery_app/define-packing-materials-edit/<string:id>', methods=['GET', 'POST'])
def edit_define_packing_materials(id):
    form = DefinePackagingMaterialsForm()
    if not form.validate_on_submit():
        try:
            packing_materials = PackagingMaterialsTb.query.get(id)
            form.description.data = packing_materials.Description
        except Exception as ex:
            flash(ex, 'danger')
    elif form.validate_on_submit():
        try:
            packaging_materials_tb_edit = db.session.query(PackagingMaterialsTb).filter(PackagingMaterialsTb.ID == id).one()
            before_packing_materials = packaging_materials_tb_edit.Description

            packaging_materials_tb_edit.Description = form.description.data

            db.session.commit()

            if before_packing_materials != form.description.data:
                flash(
                    '\n\t "' + before_packing_materials + '" successfully edited to "' + form.description.data + '"',
                    'success')
                return redirect(url_for('view_packing_materials', form=form))
        except Exception as ex:
            flash(ex, 'danger')

    return render_template('/delivery_app/define-packing-materials.html', form=form)


@app.route('/delivery_app/view-packing-materials')
def view_packing_materials():
    return render_template('/delivery_app/view-packing-materials.html')
