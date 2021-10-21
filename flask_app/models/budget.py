from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user


class Budget:
    def __init__(self, data):
        self.id = data['id']
        self.amount = data['amount']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

        self.owner = {}

    @staticmethod
    def validate_budget(budgetForm):
        is_valid = True
        if budgetForm['amount'] == "":
            return flash("Amount can't be empty")
        elif float(budgetForm['amount']) < 0:
            return flash("amount must be greater than 0")
        return is_valid

    @classmethod
    def add_budget(cls, data):
        query = "INSERT INTO budgets (amount, created_at, updated_at, user_id) VALUES(%(amount)s, NOW(), NOW(), %(user_id)s)"
        return connectToMySQL('expenses_management_schema').query_db(query, data)

    @classmethod
    def get_budget_with_user_id(cls, data):
        query = "SELECT * FROM budgets JOIN users ON budgets.user_id = users.id WHERE users.id = %(id)s;"
        results = connectToMySQL(
            'expenses_management_schema').query_db(query, data)
        if len(results) < 1:
            return False
        else:
            one_budget = cls(results[0])
            user_data = {
                "id": results[0]['users.id'],
                "first_name": results[0]['first_name'],
                "last_name": results[0]['last_name'],
                "email": results[0]['email'],
                "password": results[0]['password'],
                "created_at": results[0]['users.created_at'],
                "updated_at": results[0]['users.updated_at']
            }
            one_budget.owner = user.User(user_data)
            return one_budget

    @classmethod
    def edit_exit_budget(cls, data):
        query = "UPDATE budgets SET amount = %(amount)s, updated_at = NOW() WHERE budgets.id = %(id)s"
        return connectToMySQL(
            'expenses_management_schema').query_db(query, data)
