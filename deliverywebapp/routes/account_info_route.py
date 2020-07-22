from flask import render_template, flash, redirect, url_for, request, jsonify, json
from deliverywebapp.forms.forms import LoginForm, DefineProductsForm, DefineAreasForm
from deliverywebapp import app, db
from deliverywebapp.forms.search_forms import SearchViewProductsForm
from deliverywebapp.models.models import ProductTb
from flask_sqlalchemy import sqlalchemy
from sqlalchemy import update
from deliverywebapp.utility import AlchemyEncoder
from deliverywebapp.models.models import *


@app.route('/delivery_app/account-info', methods=['GET', 'POST'])
def defineAccountInfo():
    return render_template('./delivery_app/account_info.html')
