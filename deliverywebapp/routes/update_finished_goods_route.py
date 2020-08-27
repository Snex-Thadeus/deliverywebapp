from flask import render_template, flash, redirect, url_for, request, json
from deliverywebapp.forms.forms import UpdateFinishedGoodsForm
from deliverywebapp import app
from deliverywebapp.utility import AlchemyEncoder
from deliverywebapp.models.models import *

packagingMaterialsDropDownSchema = PackagingMaterialsSchema(many=True)

productTbDropDownSchema = ProductTbDropDownSchema(many=True)


@app.route('/search-finished-goods', methods=['POST', 'GET'])
def search_finished_goods():
    searchbox = request.form.get('text')
    try:
        if searchbox != "":
            finished_goods = UpdateFinishedGoodsTb.query.filter(
                UpdateFinishedGoodsTb.Description.like('%' + searchbox + '%')).all()
            return json.dumps(finished_goods, cls=AlchemyEncoder)
        else:
            finished_goods = UpdateDailyProductionTb.query.all()
            return json.dumps(finished_goods, cls=AlchemyEncoder)
    except Exception as ex:
            flash(ex, 'danger')


@app.route('/delivery_app/define-finished-goods', methods=['GET', 'POST'])
def define_finished_goods():
    form = UpdateFinishedGoodsForm()
    try:
        if request.method == 'GET':
            product_choices = [(-1, 'Choose product')]
            product = ProductTb.query.all()
            product_dd = productTbDropDownSchema.dump(product)
            for i in product_dd:
                product_choices.append((i['ID'], i['Description']))
            form.chooseProduct.choices = product_choices

            packing_material_choices = [(-1, 'Choose Packing Material')]
            packing_material = PackagingMaterialsTb.query.all()
            packing_material_dd = packagingMaterialsDropDownSchema.dump(packing_material)
            for i in packing_material_dd:
                packing_material_choices.append((int(i['ID']), i['Description']))
            form.choosePackingMaterial.choices = packing_material_choices
        elif request.method == "POST":
            finished_goods = UpdateFinishedGoodsTb(
                form.chooseProduct.data,
                form.choosePackingMaterial.data,
                form.quantityUsed.data,
                form.date.data
            )
            db.session.add(finished_goods)
            db.session.commit()

            flash(
                'Item Uom: "' + form.chooseProduct.data + '", "' + form.choosePackingMaterial.data + '" is successfully added ',
                'success')
            return redirect(url_for('update_finished_goods', form=form))

    except Exception as ex:
        flash(ex, 'danger')

    return render_template('/delivery_app/define-finished-goods.html', form=form)


@app.route('/delivery_app/update-finished-goods')
def update_finished_goods():
    form = UpdateFinishedGoodsForm()
    return render_template('/delivery_app/update-finished-goods.html', form=form)

