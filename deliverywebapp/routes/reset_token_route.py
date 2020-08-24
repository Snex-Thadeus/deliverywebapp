from flask_login import current_user
from flask import render_template, flash, redirect, url_for
from deliverywebapp import app, bcrypt, db
from deliverywebapp.forms.forms import ResetPasswordForm
from deliverywebapp.models.models import UserAccountTb


@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('viewOrders'))
    user = UserAccountTb.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('/delivery_app/login.html', title='Reset Password', form=form)
