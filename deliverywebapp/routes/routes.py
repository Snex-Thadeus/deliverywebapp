from flask import render_template, flash, redirect, url_for, request, jsonify, json
from flask_login import login_user
from flask_mail import Message

from deliverywebapp.forms.forms import LoginForm, DefineProductsForm
from deliverywebapp import app, mail
from sqlalchemy import update
from deliverywebapp.utility import AlchemyEncoder
from deliverywebapp.models.models import *
from flask_sqlalchemy import sqlalchemy
from flask_bcrypt import Bcrypt


# def home():
#     return render_template("./analytic/analytic-index.html")
@app.route('/', methods=['GET', 'POST'])
@app.route('/delivery_app/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        useraccount = UserAccountTb.query.filter_by(Email=form.email.data).first()
        # print("user_data", useraccount)

        if useraccount and Bcrypt(app).check_password_hash(useraccount.Password, form.password.data):
            # next_page = request.args.get("next")
            # login_user(useraccount)
            # return redirect(next_page) if next_page else redirect(url_for('viewProduct'))
            return redirect(url_for('viewOrders'))
        else:
            flash("Login unsuccessful Please Check Email and Password", "danger")

    return render_template('./delivery_app/login.html', form=form)


@app.route('/pages/pages-settings')
def account():
    return render_template('./pages/pages-settings.html')


@app.route("/send-mail")
def sendEmail():
   msg = Message('Hello', sender = 'jamesgituma9961@gmail.com', recipients = ['ultratude.mobile@gmail.com'])
   msg.body = "This is the email body"
   mail.send(msg)
   return "Sent"
