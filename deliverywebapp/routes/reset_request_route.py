from flask_login import current_user
from flask import render_template, flash, redirect, url_for
from flask_mail import Message
from deliverywebapp import app, mail
from deliverywebapp.forms.forms import RequestResetForm
from deliverywebapp.models.models import UserAccountTb


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender='noreply@caompany.com',
                  recepients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('reset_token', token=token, _external=True)}

If you did not make this request, then simply ignore this email and no changes will be made
'''
    mail.send(msg)


@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('viewOrders'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = UserAccountTb.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('login'))
    return render_template('/delivery_app/login.html', form=form)
