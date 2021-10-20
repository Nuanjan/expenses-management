from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user
from flask_app.models import buget


class Expense:
    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.date = data['date']
        self.amount = data['amount']
        self.category = data['category']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']

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
    def all_expenses_with_owner(cls,data):
        
