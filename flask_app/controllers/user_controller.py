from flask.helpers import flash
from flask_app import app
from flask import redirect, render_template, session, request, url_for
from flask_app.models.buget import Budget
from flask_app.models.user import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)     # we are creating an object called bcrypt,


@app.route('/')
def index():
    data = {'budget': 1, 'expenses': 0.1}
    return render_template('index.html')


@app.route('/registration')
def register():
    return render_template('registration.html')


@app.route('/register', methods=['POST'])
def register_user():
    print("t his is form request", request.form)
    if not User.validate_user(request.form):
        return redirect('/registration')
    hashed_password = bcrypt.generate_password_hash(request.form['password'])
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['e_mail'],
        "password": hashed_password
    }
    addUser = User.add_user(data)
    if not addUser:
        return redirect('/registration')
    session['user_id'] = addUser
    return redirect('/user_dashboard')


@app.route('/login', methods=['POST'])
def login_user():
    data = {"email": request.form['e_mail']}
    user_in_db = User.get_user_by_email(data)
    validation_data = {
        "user_in_db": user_in_db,
        "password": request.form["password"]
    }
    if not User.validate_login_user(validation_data):
        return redirect('/')
    elif not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        print(bcrypt.check_password_hash(
            user_in_db.password, request.form['password']))
        flash("Invalid user/password")
        return redirect('/')
    session['user_id'] = user_in_db.id
    print(session['user_id'], " id from login")
    return redirect('/user_dashboard')


@app.route('/user_dashboard')
def user_dashboard():
    if 'user_id' in session:
        data = {
            "id": session['user_id']
        }
        one_user = User.get_user_by_id(data)
        print(one_user, " this is one user")
        one_budget = Budget.get_budget_with_user_id(data)
        if not one_budget:
            budget = 0
        else:
            budget = one_budget
        print("one budget", budget)
        return render_template('user_dashboard.html', one_user=one_user, budget=budget)
    else:
        return redirect('/forbidden')


@app.route('/logout')
def log_out():
    session.clear()
    return redirect('/')


@app.route('/forbidden')
def unauthorize():
    return render_template('forbidden.html')
