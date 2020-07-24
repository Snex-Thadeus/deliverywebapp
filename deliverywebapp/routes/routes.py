from flask import render_template, flash, redirect, url_for, request, jsonify, json
from flask_login import login_user

from deliverywebapp.forms.forms import LoginForm, DefineProductsForm
from deliverywebapp import app, bcrypt
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
        useraccount = UserAccountTb.query.filter_by(Email=form.email.data).first()
        print("user_data", useraccount)

        if useraccount and bcrypt.check_password_hash(useraccount.password, form.password.data):
            next_page = request.args.get("next")
            login_user(useraccount)
            #return redirect(next_page) if next_page else redirect(url_for('viewProduct'))
            return redirect(url_for('viewProduct'))
        else:
            flash("Login unsuccessful Please Check Email and Password", "danger")

    return render_template('./delivery_app/login.html', form=form)


@app.route('/pages/pages-settings')
def account():
    return render_template('./pages/pages-settings.html')
