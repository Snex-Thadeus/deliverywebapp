import mail
from flask import render_template, flash, redirect, url_for
from flask_login import login_user, current_user
from deliverywebapp import bcrypt
from flask_mail import Message
from deliverywebapp.forms.forms import LoginForm
from flask_bcrypt import Bcrypt
from deliverywebapp.models.models import *

# def home():
#     return render_template("./analytic/analytic-index.html")


@app.route('/', methods=['GET', 'POST'])
@app.route('/delivery_app/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('viewOrders'))
    form = LoginForm()
    if form.validate_on_submit():
        user_account = UserAccountTb.query.filter_by(Email=form.email.data).first()
        if user_account.Email == form.email.data and user_account.Password == form.password.data:
            #login_user(user_account)
            flash('You have been logged in!', 'success')
            #next_page = request.args.get("next")
            #return redirect(next_page) if next_page else redirect(url_for('viewProduct'))
            return redirect(url_for('view_orders'))
        else:
            flash("Login unsuccessful Please Check Email and Password", "danger")

    return render_template('/delivery_app/login.html', form=form)


@app.route('/pages/pages-settings')
def account():
    return render_template('./pages/pages-settings.html')


@app.route("/send-mail")
def send_email():
    msg = Message('Hello', sender='jamesgituma9961@gmail.com', recipients=['ultratude.mobile@gmail.com'])
    msg.body = "This is the email body"
    mail.send(msg)
    return "Sent"
