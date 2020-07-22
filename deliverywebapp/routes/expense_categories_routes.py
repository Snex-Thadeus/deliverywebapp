from flask import render_template, flash, redirect, url_for, request, jsonify, json
from deliverywebapp.forms.forms import LoginForm, DefineProductsForm, DefineAreasForm, DefineBillsForm, \
    DefineExpenseCategoriesForm
from deliverywebapp import app, db
from deliverywebapp.forms.search_forms import SearchViewProductsForm
from deliverywebapp.models.models import ProductTb
from flask_sqlalchemy import sqlalchemy
from sqlalchemy import update
from deliverywebapp.utility import AlchemyEncoder
from deliverywebapp.models.models import *


@app.route('/search_view_expense_categories', methods=['POST', 'GET'])
def searchViewExpenseCategories():
    searchbox = request.form.get('text')
    try:
        if searchbox != "":
            expenseCategorys = ExpenseCategoriesTb.query.filter(
                ExpenseCategoriesTb.CategoryDescription.like('%' + searchbox + '%')).all()
            return json.dumps(expenseCategorys, cls=AlchemyEncoder)
        else:
            expenseCategorys = ExpenseCategoriesTb.query.all()
            return json.dumps(expenseCategorys, cls=AlchemyEncoder)
    except Exception as ex:
            flash(ex, 'danger')


@app.route('/delivery_app/define-expenseCategories', methods=['GET', 'POST'])
def defineExpenseCategory():
    form = DefineExpenseCategoriesForm()
    if form.validate_on_submit():
        try:
            expenseCategory = ExpenseCategoriesTb(form.categoryDescription.data)
            db.session.add(expenseCategory)
            db.session.commit()

            flash('Expense Category: "' + form.categoryDescription.data + '" successfully added', 'success')
            return redirect(url_for('viewExpenseCategory', form=form))
        except Exception as ex:
            flash(ex, 'danger')

    return render_template('./delivery_app/define-expense-categories.html', form=form)


@app.route('/delivery_app/define-expense-category-edit/<string:id>', methods=['GET', 'POST'])
def editDefineExpenseCategories(id):
    form = DefineExpenseCategoriesForm()
    if not form.validate_on_submit():
        try:
            expenseCategory = ExpenseCategoriesTb.query.get(id)
            form.categoryDescription.data = expenseCategory.CategoryDescription
        except Exception as ex:
            flash(ex, 'danger')
    elif form.validate_on_submit():
        try:
            ExpenseCategoryTbEdit = db.session.query(ExpenseCategoriesTb).filter(ExpenseCategoriesTb.ID == id).one()
            BeforeExpenseCategory = ExpenseCategoryTbEdit.CategoryDescription

            ExpenseCategoryTbEdit.CategoryDescription = form.categoryDescription.data

            db.session.commit()

            if BeforeExpenseCategory != form.categoryDescription.data:
                flash(
                    '\n\t "' + BeforeExpenseCategory + '" successfully edited to "' + form.categoryDescription.data + '"',
                    'success')

        except Exception as ex:
            flash(ex, 'danger')

        return redirect(url_for('viewExpenseCategory', form=form))

    return render_template('./delivery_app/define-expense-categories.html', form=form)


@app.route('/delivery_app/view-expense-categories')
def viewExpenseCategory():
    return render_template('./delivery_app/view-expense-categories.html')
