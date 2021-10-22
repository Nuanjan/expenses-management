from flask.helpers import flash
from flask_app import app
from flask import redirect, render_template, session, request, url_for
from flask_app.models.budget import Budget
from flask_app.models.user import User
from flask_app.models.expense import Expense
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol
import google.auth.transport.requests
import requests
import os
import pathlib
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv


os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
client_secrets_file = os.path.join(
    pathlib.Path(__file__).parent, "client_secret.json")
flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile",
            "https://www.googleapis.com/auth/userinfo.email", "openid"],
    redirect_uri="http://localhost:5000/callback")
bcrypt = Bcrypt(app)     # we are creating an object called bcrypt,


@app.route('/')
def index():
    data = {'budget': 1, 'expenses': 0.1}
    return render_template('index.html')


@app.route('/google_login')
def google_login():
    authorization_url, state = flow.authorization_url()
    session['state'] = state
    print(" this is session state", session['state'])
    return redirect(authorization_url)


@app.route("/callback")
def callback():
    flow.fetch_token(authorization_response=request.url)
    if 'state' in session:
        if not session["state"] == request.args["state"]:
            return redirect('/forbidden')

    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(
        session=cached_session)

    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=GOOGLE_CLIENT_ID
    )
    session['e_mail'] = id_info.get("email")
    session['first_name'] = id_info.get("given_name")
    session['last_name'] = id_info.get("family_name")
    session['user_id'] = id_info.get("sub")
    return redirect('/user_dashboard')


@app.route('/registration')
def register():
    return render_template('registration.html')


@app.route('/register', methods=['POST'])
def register_user():
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
        flash("Invalid user/password")
        return redirect('/')
    session['user_id'] = user_in_db.id
    return redirect('/user_dashboard')


@app.route('/user_dashboard')
def user_dashboard():
    if 'user_id' in session:
        data = {
            "id": session['user_id']
        }
        one_user = User.get_user_by_id(data)
        budget = Budget.get_budget_with_user_id(data)
        if not budget:
            session['budget_id'] = 0
        else:
            session['budget_id'] = budget.id

        if 'start_date' in session:
            date_data = {
                "start_date": session['start_date'],
                "end_date": session['end_date']
            }
            all_expenses = Expense.all_expenses_with_date(date_data)
            session.pop('start_date', None)
            session.pop('end_date', None)
        else:
            all_expenses = Expense.all_expenses_with_owner_and_budget(data)
        summary = Expense.get_budget_and_expense(data)
        total_expenses = 0.00
        if not summary:
            total_expenses = 0.00
        else:
            total_expenses = summary['total_expenses']/summary['budget']
        total = Expense.get_total_base_on_category(data)
        data = []
        for tol in total:
            data.append({tol['category']: tol['total']})
        return render_template('user_dashboard.html', one_user=one_user, budget=budget, budget_id=session['budget_id'], all_expenses=all_expenses, total_expenses=total_expenses, data=data)
    else:
        return redirect('/forbidden')


@app.route('/logout')
def log_out():
    session.clear()
    return redirect('/')


@app.route('/forbidden')
def unauthorize():
    return render_template('forbidden.html')
