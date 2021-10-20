# import the function that will return an instance of a connection
from flask_app.config.mysqlconnection import connectToMySQL
# model the class after the friend table from our database
from flask import flash
from flask_app.models import budget
from flask_app.models import expense

import re


EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PW_REGEX = re.compile(r'\A(?=\S*?\d)(?=\S*?[A-Z])(?=\S*?[a-z])\S{8,}\Z')


class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        # Now we use class methods to query our database
        self.budget = {}
        self.expenses = []

    @staticmethod
    def validate_user(userFormData):
        is_valid = True  # we assume this is true
        if len(userFormData['first_name']) < 2:
            flash("First Name must be at least 2 characters.")
            is_valid = False
        if len(userFormData['last_name']) < 2:
            flash("Last Name must be at least 2 characters.")
            is_valid = False

        if len(userFormData['password']) < 8:
            flash("Password must be at least 8 characters.")
            is_valid = False
        if not PW_REGEX.match(userFormData['password']):
            flash("email must be at least one digit")
            flash("email must be at least one uppercase letter")
            flash("email must be at least one lowercase letter")
            is_valid = False
        if userFormData['password'] != userFormData['confirm_password']:
            flash("password and confirm password does not match")
            is_valid = False
        if not EMAIL_REGEX.match(userFormData['e_mail']):
            flash("Invalid email")
            is_valid = False
        data = {"email": userFormData['e_mail']}
        if User.get_user_by_email(data):
            flash("Thia Email already taken!")
            is_valid = False
        return is_valid

    @staticmethod
    def validate_login_user(data):
        is_valid = True
        if not data['user_in_db']:
            flash("Incorrect Email/Password")
            is_valid = False
        return is_valid

    @classmethod
    def add_user(cls, data):
        print('data from queries: ', data)
        query = "INSERT INTO users (first_name , last_name , email ,password, created_at, updated_at ) VALUES ( %(first_name)s , %(last_name)s , %(email)s ,%(password)s, NOW() , NOW());"
        return connectToMySQL('expenses_management_schema').query_db(query, data)

    @classmethod
    def get_user_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s"
        result = connectToMySQL('expenses_management_schema').query_db(query, data)
        if len(result) < 1:
            return False
        return cls(result[0])

    @classmethod
    def get_user_by_id(cls, data):
        query = "SELECT * FROM users WHERE users.id = %(id)s"
        result = connectToMySQL('expenses_management_schema').query_db(query, data)
        if len(result) < 1:
            return False
        return cls(result[0])
    