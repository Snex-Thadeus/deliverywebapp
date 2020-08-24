from flask import render_template, flash, redirect, url_for, request, jsonify, json
from flask_bcrypt import Bcrypt
from deliverywebapp.forms.forms import DefineAccountInfoForm
from deliverywebapp import app
from deliverywebapp.utility import AlchemyEncoder
from deliverywebapp.models.models import *


@app.route('/search-account-info', methods=['GET', 'POST'])
def search_account_info(user_account=''):
    searchbox = request.form.get('text')
    try:
        if searchbox:
            user_account = UserAccountTb.query.filter(
                UserAccountTb.Name.like('%' + searchbox + '%')).all()
            return json.dumps(user_account, cls=AlchemyEncoder)
        else:
            user_account = UserAccountTb.query.all()
            return json.dumps(user_account, cls=AlchemyEncoder)
    except Exception as ex:
        flash(ex, 'danger')


@app.route('/delivery_app/account-info', methods=['GET', 'POST'])
def define_account_info():
    form = DefineAccountInfoForm()
    if request.method == "POST":
        try:
            # Name, UserName, Email, PhoneNumber, Password, OrganizationID
            user_account = UserAccountTb(
                Name=form.name.data, UserName=form.username.data, Email=form.email.data,
                PhoneNumber=form.phonenumber.data,
                Password=Bcrypt(app).generate_password_hash(form.password.data), OrganizationID="1")
            db.session.add(user_account)
            db.session.commit()

            flash('User "' + form.name.data + '" successfully added', 'success')

            return redirect(url_for("viewAccountInfo"))
        except Exception as ex:
            flash(ex, 'danger')

    return render_template('./delivery_app/account_info.html', form=form)


@app.route('/delivery_app/view-account-info', methods=['GET'])
def view_account_info():
    return render_template('./delivery_app/view-user-accounts.html')


@app.route('/delivery_app/account-info-edit/<string:id>', methods=['GET', 'POST'])
def account_info_edit(id):
    form = DefineAccountInfoForm()
    before_name = None
    before_user_name = None
    before_email = None
    before_phone_number = None

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

            user_account_edit = db.session.query(UserAccountTb) \
                .filter(UserAccountTb.ID == id).one()
            before_name = user_account_edit.Name
            before_user_name = user_account_edit.UserName
            before_email = user_account_edit.Email
            before_phone_number = user_account_edit.PhoneNumber

            user_account_edit.Name = form.name.data
            user_account_edit.UserName = form.username.data
            user_account_edit.Email = form.email.data
            user_account_edit.PhoneNumber = form.phonenumber.data
            db.session.commit()

            if before_name != form.name.data:
                flash(
                    '\n\t ' + form.name.data + '\'s name "' + before_name + '" successfully edited to "' + form.name.data + '"',
                    'success')
            if before_user_name != form.username.data:
                flash(
                    '\n\t ' + form.name.data + '\'s username "' + before_user_name + '" successfully edited to "' + form.username.data + '"',
                    'success')
            if before_email != form.email.data:
                flash(
                    '\n\t ' + form.name.data + '\'s email "' + before_email + '" successfully edited to "' + form.email.data + '"',
                    'success')
            if before_phone_number != form.phonenumber.data:
                flash(
                    '\n\t ' + form.name.data + '\'s phone number "' + before_phone_number + '" successfully edited to "' + form.phonenumber.data + '"',
                    'success')

            return redirect(url_for("viewAccountInfo", form=form))
        except Exception as ex:
            flash(ex, 'danger')

    return render_template('/delivery_app/account_info.html', form=form)
