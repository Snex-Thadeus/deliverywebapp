from flask import render_template
from flask_wtf import FlaskForm
from wtforms import StringField
from deliverywebapp import app
from deliverywebapp.models.models import *

NAMES = ["abc", "abcd", "abcde", "abcdef"]


class SearchForm(FlaskForm):
    autocomp = StringField('autocomp', id='autocomplete')


customers_schema = CustomerSchema(many=True)

#
# @app.route('/autocomplete', methods=['GET'])
# def autocomplete():
#     # # TODO: CUSTOMER DATA
#     # customerTB = CustomerTb.query.all()
#     # return jsonify(customers_schema.dump(customerTB))
#     #search = request.args.get('term')
#     #app.logger.debug(search)
#     return Response(json.dumps(NAMES), mimetype='application/json')


@app.route('/example', methods=['GET', 'POST'])
def example():
    form = SearchForm()
    return render_template("/example_autocomplete.html", form=form)
