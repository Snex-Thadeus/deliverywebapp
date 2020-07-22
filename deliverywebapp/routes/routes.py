from flask import render_template, flash, redirect, url_for, request, jsonify, json
from deliverywebapp.forms.forms import LoginForm, DefineProductsForm
from deliverywebapp import app
from sqlalchemy import update
from deliverywebapp.utility import AlchemyEncoder
from deliverywebapp.models.models import *
from flask_sqlalchemy import sqlalchemy


# def home():
#     return render_template("./analytic/analytic-index.html")
@app.route('/')
@app.route('/delivery_app/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login success', 'success')
        return redirect(url_for('viewProduct'))

    return render_template('./delivery_app/login.html', form=form)


@app.route('/pages/pages-settings')
def account():
    return render_template('./pages/pages-settings.html')
