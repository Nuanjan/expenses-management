from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user
from flask_app.models import buget


class Expense:
    def __init__(self, data):
        self.id = data['id']
        self.expense = data['expense']
        self.date = data['date']
        self.amount = data['amount']
        self.category = data['category']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.owner = {}

    @staticmethod
    def validate_expense(expensesFormData):
        is_valid = True
        if expensesFormData['expense'] == "" or expensesFormData['date'] == "" or expensesFormData['category'] == "none":
            flash("All filed required")
            is_valid = False
        elif expensesFormData['amount'] == "":
            flash("All filed required")
        elif float(expensesFormData['amount']) < 1.00:
            flash('Amount must be greater than 0')
            is_valid = False
        return is_valid

    @classmethod
    def add_expense(cls, data):
        query = "INSERT INTO expenses (expense, date, amount, category, created_at, updated_at, user_id) VALUES(%(expense)s, %(date)s, %(amount)s, %(category)s,NOW(), NOW(),%(user_id)s)"
        results = connectToMySQL(
            'expenses_management_schema').query_db(query, data)
        return results

    @classmethod
    def all_expenses_with_owner(cls, data):
        query = "SELECT * FROM expenses LEFT JOIN users ON expenses.user_id = users.id WHERE users.id = %(id)s;"
        results = connectToMySQL(
            'expenses_management_schema').query_db(query, data)
        all_expenses = []

        if len(results) < 1:
            return False
        else:
            for row in results:
                one_expense = cls(row)
                user_data = {
                    "id": row['users.id'],
                    "first_name": row['first_name'],
                    "last_name": row['last_name'],
                    "email": row['email'],
                    "password": row['password'],
                    "created_at": row['users.created_at'],
                    "updated_at": row['users.updated_at']
                }

                one_expense.owner = user.User(user_data)
                all_expenses.append(one_expense)
            return all_expenses

    @classmethod
    def one_expense_with_owner(cls, data):
        query = "SELECT * FROM expenses JOIN users ON expenses.user_id = users.id WHERE expenses.id = %(id)s"
        results = connectToMySQL(
            'expenses_management_schema').query_db(query, data)

        one_expenses = cls(results[0])
        user_data = {
            "id": results[0]['users.id'],
            "first_name": results[0]['first_name'],
            "last_name": results[0]['last_name'],
            "email": results[0]['email'],
            "password": results[0]['password'],
            "created_at": results[0]['users.created_at'],
            "updated_at": results[0]['users.updated_at']

        }

        one_expenses.owner = user.User(user_data)
        return one_expenses

    @classmethod
    def edit_exit_expense(cls, data):
        query = "UPDATE expenses SET expense=%(expense)s, date=%(date)s, amount=%(amount)s, category=%(category)s, user_id=%(user_id)s, updated_at= NOW() WHERE id = %(id)s"

        return connectToMySQL('expenses_management_schema').query_db(query, data)

    @classmethod
    def delete_expense(cls, data):
        query = "DELETE FROM expenses WHERE id=%(id)s"
        return connectToMySQL('expenses_management_schema').query_db(query, data)
