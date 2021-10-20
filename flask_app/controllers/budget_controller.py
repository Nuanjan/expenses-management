from flask.helpers import flash
from werkzeug.datastructures import RequestCacheControl
from flask_app import app
from flask_app.models.user import User
from flask import redirect, render_template, session, request, url_for
from flask_app.models.buget import Budget


@app.route('/new/budget')
def new_budget():
    if not 'user_id' in session:
        return render_template('forbidden.html')
    user_data = {
        'id': session['user_id']
    }
    one_user = User.get_user_by_id(user_data)
    return render_template('add_budget.html', one_user=one_user)


@app.route('/add_budget', methods=['POST'])
def add_budget():
    print('form request', request.form)
    print('user_id', session['user_id'])
    if not 'user_id' in session:
        return render_template('forbidden.html')
    else:
        if not Budget.validate_budget(request.form):
            return redirect('/new/budget')
        data = {
            "amount": request.form['amount'],
            "user_id": session['user_id']

        }
        Budget.add_budget(data)
        return redirect('/user_dashboard')
