from flask.helpers import flash
from werkzeug.datastructures import RequestCacheControl
from flask_app import app
from flask_app.models.expense import Expense
from flask_app.models.user import User
from flask_app.models.budget import Budget
from flask import redirect, render_template, session, request, url_for


@app.route('/new/expense')
def new_expense():
    if not 'user_id' in session:
        return render_template('forbidden.html')
    user_data = {
        'id': session['user_id']
    }
    one_user = User.get_user_by_id(user_data)
    return render_template('add_expense.html', one_user=one_user)


@app.route('/add_expense', methods=['POST'])
def add_expense():
    if not 'user_id' in session:
        return render_template('forbidden.html')
    if not Expense.validate_expense(request.form):
        return redirect('/new/expense')
    if not 'budget_id' in session:
        session['budget_id'] = 0

    if session['budget_id'] == 0:
        flash("You must add the budget before add the expense")
        return redirect('/user_dashboard')
    else:
        data = {
            "expense": request.form['expense'],
            "date": request.form['date'],
            "amount": request.form['amount'],
            "category": request.form['category'],
            "user_id": session['user_id'],
            "budget_id": session['budget_id']

        }
        Expense.add_expense(data)
        return redirect('/user_dashboard')


@app.route('/edit_expense/<int:expense_id>')
def edit_expense(expense_id):
    if not 'user_id' in session:
        return render_template('forbidden.html')
    user_data = {
        'id': session['user_id']
    }
    one_user = User.get_user_by_id(user_data)
    data = {
        "id": expense_id
    }
    one_expense = Expense.one_expense_with_owner_and_budget(data)
    return render_template('edit_expense.html', one_user=one_user, one_expense=one_expense)


@app.route('/edit_exit_expense/<int:expense_id>', methods=['POST'])
def edit_exit_expense(expense_id):
    if not Expense.validate_expense(request.form):
        return redirect(f'/edit_expense/{expense_id}')
    data = {
        "id": expense_id,
        "expense": request.form['expense'],
        "date": request.form['date'],
        "amount": request.form['amount'],
        "category": request.form['category'],
        "user_id": session['user_id'],
        "budget_id": session['budget_id']

    }
    Expense.edit_exit_expense(data)
    return redirect('/user_dashboard')


@app.route('/delete_expense/<int:expense_id>')
def delete_expense(expense_id):
    data = {
        "id": expense_id
    }
    Expense.delete_expense(data)
    return redirect('/user_dashboard')


@app.route('/expenses/list/date', methods=['POST'])
def all_expenses_with_date():
    if not 'start_date' in session:
        session['start_date'] = request.form['start_date']
    if not 'end_date' in session:
        session['end_date'] = request.form['end_date']
    return redirect('/user_dashboard')
