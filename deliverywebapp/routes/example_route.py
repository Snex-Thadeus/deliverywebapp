from flask import render_template, flash, redirect, url_for, request, jsonify, json, Response
from flask_wtf import FlaskForm
from wtforms import SelectField, StringField

from deliverywebapp.forms.forms import LoginForm, DefineProductsForm, DefineAreasForm, DefineBillsForm, \
    DefineCustomerDetailsForm, DefineOrdersForm
from deliverywebapp import app, db
from deliverywebapp.forms.search_forms import SearchViewProductsForm
from deliverywebapp.models.models import ProductTb
from flask_sqlalchemy import sqlalchemy
from sqlalchemy import update, or_
from deliverywebapp.utility import AlchemyEncoder
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
    return render_template("./example_autocomplete.html", form=form)
