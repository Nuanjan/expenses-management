from flask.helpers import flash
from werkzeug.datastructures import RequestCacheControl
from flask_app import app
from flask_app.models.user import User
from flask import redirect, render_template, session, request, url_for
from flask_app.models.buget import Budget


@app.route('/new/expense')
def new_expense():
    if not 'user_id' in session:
        return render_template('forbidden.html')
    user_data = {
        'id': session['user_id']
    }
    one_user = User.get_user_by_id(user_data)
    return render_template('add_expense.html', one_user=one_user)
