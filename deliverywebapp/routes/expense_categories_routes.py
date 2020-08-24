from flask import render_template, flash, redirect, url_for, request, jsonify, json
from deliverywebapp.forms.forms import DefineExpenseCategoriesForm
from deliverywebapp import app
from deliverywebapp.utility import AlchemyEncoder
from deliverywebapp.models.models import *


@app.route('/search_view_expense_categories', methods=['POST', 'GET'])
def search_view_expense_categories():
    searchbox = request.form.get('text')
    try:
        if searchbox != "":
            expense_category = ExpenseCategoriesTb.query.filter(
                ExpenseCategoriesTb.CategoryDescription.like('%' + searchbox + '%')).all()
            return json.dumps(expense_category, cls=AlchemyEncoder)
        else:
            expense_category = ExpenseCategoriesTb.query.all()
            return json.dumps(expense_category, cls=AlchemyEncoder)
    except Exception as ex:
            flash(ex, 'danger')


@app.route('/delivery_app/define-expenseCategories', methods=['GET', 'POST'])
def define_expense_category():
    form = DefineExpenseCategoriesForm()
    if form.validate_on_submit():
        try:
            expense_category = ExpenseCategoriesTb(form.categoryDescription.data)
            db.session.add(expense_category)
            db.session.commit()

            flash('Expense Category: "' + form.categoryDescription.data + '" successfully added', 'success')
            return redirect(url_for('view_expense_category', form=form))
        except Exception as ex:
            flash(ex, 'danger')

    return render_template('./delivery_app/define-expense-categories.html', form=form)


@app.route('/delivery_app/define-expense-category-edit/<string:id>', methods=['GET', 'POST'])
def edit_define_expense_categories(id):
    form = DefineExpenseCategoriesForm()
    if not form.validate_on_submit():
        try:
            expense_category = ExpenseCategoriesTb.query.get(id)
            form.categoryDescription.data = expense_category.CategoryDescription
        except Exception as ex:
            flash(ex, 'danger')
    elif form.validate_on_submit():
        try:
            expense_category_tb_edit = db.session.query(ExpenseCategoriesTb).filter(ExpenseCategoriesTb.ID == id).one()
            before_expense_category = expense_category_tb_edit.CategoryDescription

            expense_category_tb_edit.CategoryDescription = form.categoryDescription.data

            db.session.commit()

            if before_expense_category != form.categoryDescription.data:
                flash(
                    '\n\t "' + before_expense_category + '" successfully edited to "' + form.categoryDescription.data + '"',
                    'success')

        except Exception as ex:
            flash(ex, 'danger')

        return redirect(url_for('viewExpenseCategory', form=form))

    return render_template('/delivery_app/define-expense-categories.html', form=form)


@app.route('/delivery_app/view-expense-categories')
def view_expense_category():
    return render_template('/delivery_app/view-expense-categories.html')
