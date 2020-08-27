from flask import render_template, flash, redirect, url_for, request, json
from deliverywebapp.forms.forms import UpdatePackagingMaterialsForm
from deliverywebapp import app
from deliverywebapp.utility import AlchemyEncoder
from deliverywebapp.models.models import *

packagingMaterialsDropDownSchema = PackagingMaterialsSchema(many=True)


@app.route('/search-packaging-materials', methods=['POST', 'GET'])
def search_packaging_materials():
    searchbox = request.form.get('text')
    try:
        if searchbox != "":
            packaging_materials = UpdatePackagingMaterialsTb.query.filter(
                ProductionActivitiesTb.Description.like('%' + searchbox + '%')).all()
            return json.dumps(packaging_materials, cls=AlchemyEncoder)
        else:
            packaging_materials = UpdatePackagingMaterialsTb.query.all()
            return json.dumps(packaging_materials, cls=AlchemyEncoder)
    except Exception as ex:
            flash(ex, 'danger')


@app.route('/delivery_app/define-packaging-materials', methods=['GET', 'POST'])
def define_packaging_materials():
    form = UpdatePackagingMaterialsForm()
    try:
        if request.method == 'GET':
            packaging_materials_choices = [(-1, 'Choose packaging materials')]
            packaging_materials = PackagingMaterialsTb.query.all()
            packaging_materials_dd = packagingMaterialsDropDownSchema.dump(packaging_materials)
            for i in packaging_materials_dd:
                packaging_materials_choices.append((i['ID'], i['Description']))
            form.choosePackagingMaterial.choices = packaging_materials_choices

        else:
            request.method == "POST"
            packaging_materials = UpdateDailyProductionTb(
                form.choosePackagingMaterial.data,
                form.quantity.data,
                form.date.data
            )
            db.session.add(packaging_materials)
            db.session.commit()

            flash(
                'Packaging materials: "' + form.choosePackagingMaterial.data + '" is successfully added ',
                'success')
            return redirect(url_for('view_packaging_materials', form=form))

    except Exception as ex:
        flash(ex, 'danger')

    return render_template('/delivery_app/define-packaging-materials.html', form=form)


@app.route('/delivery_app/view-packaging-materials')
def view_packaging_materials():
    form = UpdatePackagingMaterialsForm()
    return render_template('/delivery_app/view-packaging-materials.html', form=form)

