from flask import render_template, flash, request, json
from deliverywebapp.forms.forms import UpdatePackagingMaterialsForm
from deliverywebapp import app
from deliverywebapp.utility import AlchemyEncoder
from deliverywebapp.models.models import *


#@app.route('/search-packaging-materials', methods=['POST', 'GET'])
#def search_packaging_materials():
 #   searchbox = request.form.get('text')
  #  try:
   #     if searchbox != "":
    #        packaging_materials = UpdatePackagingMaterialsTb.query.filter(
     #           ProductionActivitiesTb.Description.like('%' + searchbox + '%')).all()
      # #     return json.dumps(packaging_materials, cls=AlchemyEncoder)
        #else:
         #   packaging_materials = UpdatePackagingMaterialsTb.query.all()
          #  return json.dumps(packaging_materials, cls=AlchemyEncoder)
    #except Exception as ex:
     #       flash(ex, 'danger')


@app.route('/delivery_app/view-packaging_materials')
def view_packaging_materials():
    form = UpdatePackagingMaterialsForm()
    return render_template('/delivery_app/view-packaging-materials.html', form=form)

