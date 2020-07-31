from flask import render_template, flash, redirect, url_for, request, jsonify, json
from flask_bcrypt import Bcrypt

from deliverywebapp.forms.forms import LoginForm, DefineProductsForm, DefineAreasForm, DefineAccountInfo
from deliverywebapp import app, db

from deliverywebapp.utility import AlchemyEncoder
from deliverywebapp.models.models import *


@app.route('/search-account-info', methods=['GET', 'POST'])
def searchAccountInfo():
    searchbox = request.form.get('text')
    try:
        if searchbox:
            userAccount = UserAccountTb.query.filter(
                UserAccountTb.Name.like('%' + searchbox + '%')).all()
            return json.dumps(userAccount, cls=AlchemyEncoder)
        else:
            userAccount = UserAccountTb.query.all()
            return json.dumps(userAccount, cls=AlchemyEncoder)
    except Exception as ex:
        flash(ex, 'danger')


@app.route('/delivery_app/account-info', methods=['GET', 'POST'])
def defineAccountInfo():
    form = DefineAccountInfo()
    if request.method == "POST":
        try:
            # Name, UserName, Email, PhoneNumber, Password, OrganizationID
            userAccount = UserAccountTb(
                Name=form.name.data, UserName=form.username.data, Email=form.email.data,
                PhoneNumber=form.phonenumber.data,
                Password=Bcrypt(app).generate_password_hash(form.password.data), OrganizationID="1")
            db.session.add(userAccount)
            db.session.commit()

            flash('User "' + form.name.data + '" successfully added', 'success')

            return redirect(url_for("viewAccountInfo"))
        except Exception as ex:
            flash(ex, 'danger')

    return render_template('./delivery_app/account_info.html', form=form)


@app.route('/delivery_app/view-account-info', methods=['GET'])
def viewAccountInfo():
    return render_template('./delivery_app/view-user-accounts.html')


@app.route('/delivery_app/account-info-edit/<string:id>', methods=['GET', 'POST'])
def accountInfoEdit(id):
    form = DefineAccountInfo()
    BeforeName = None
    BeforeUsername = None
    BeforeEmail = None
    BeforePhonenumber = None

    if request.method == 'GET':
        try:
            accountinfo = UserAccountTb.query.get(id)
            form.name.data = accountinfo.Name
            form.username.data = accountinfo.UserName
            form.email.data = accountinfo.Email
            form.phonenumber.data = accountinfo.PhoneNumber

            form.edit = 1

        except Exception as ex:
            flash(ex, 'danger')
    elif request.method == 'POST':
        try:

            userAccountEdit = db.session.query(UserAccountTb) \
                .filter(UserAccountTb.ID == id).one()
            BeforeName = userAccountEdit.Name
            BeforeUsername = userAccountEdit.UserName
            BeforeEmail = userAccountEdit.Email
            BeforePhonenumber = userAccountEdit.PhoneNumber

            userAccountEdit.Name = form.name.data
            userAccountEdit.UserName = form.username.data
            userAccountEdit.Email = form.email.data
            userAccountEdit.PhoneNumber = form.phonenumber.data
            db.session.commit()

            if BeforeName != form.name.data:
                flash(
                    '\n\t ' + form.name.data + '\'s name "' + BeforeName + '" successfully edited to "' + form.name.data + '"',
                    'success')
            if BeforeUsername != form.username.data:
                flash(
                    '\n\t ' + form.name.data + '\'s username "' + BeforeUsername + '" successfully edited to "' + form.username.data + '"',
                    'success')
            if BeforeEmail != form.email.data:
                flash(
                    '\n\t ' + form.name.data + '\'s email "' + BeforeEmail + '" successfully edited to "' + form.email.data + '"',
                    'success')
            if BeforePhonenumber != form.phonenumber.data:
                flash(
                    '\n\t ' + form.name.data + '\'s phone number "' + BeforePhonenumber + '" successfully edited to "' + form.phonenumber.data + '"',
                    'success')

            return redirect(url_for("viewAccountInfo", form=form))
        except Exception as ex:
            flash(ex, 'danger')

    return render_template('./delivery_app/account_info.html', form=form)
