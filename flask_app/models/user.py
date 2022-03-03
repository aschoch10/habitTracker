import re
from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL
from flask_bcrypt import Bcrypt
from flask_app import app

bcrypt = Bcrypt(app)

class User:
# to do create scema in mySQL workbench
    schema = ("habittracker_schema")
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.habits = []


    @classmethod
    def getByEmail(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(cls.schema).query_db(query, data)
        if len(results) < 1:
            return False
        return User(results[0])


    @classmethod
    def getByID(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(cls.schema).query_db(query, data)
        if len(results) < 1:
            return False
        return User(results[0])


    @classmethod
    def create(cls, data):
        query = "INSERT into users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        return connectToMySQL(cls.schema).query_db(query, data)


    @staticmethod
    def registerValidate(post_data):
        is_valid = True
        if len(post_data['first_name']) < 2:
            flash("First Name must be longer than 2 characters")
            is_valid = False
        if len(post_data['last_name']) < 2:
            flash("Last Name must be longer than 2 characters")
            is_valid = False
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
        if not EMAIL_REGEX.match(post_data['email']):
            flash('Invalid Email!')
            is_valid = False
        else: 
            user = User.getByEmail({"email": post_data['email']})
            if user:
                flash('Email already in use!')
                is_valid= False
        if len(post_data['password']) < 8:
            flash("Password must be longer than 8 characters")
            is_valid = False
        if post_data['password'] != post_data['confirm_password']:
            flash('Password and confirm password must match')
            is_valid= False
        return is_valid 


    @staticmethod
    def loginValidate(post_data):
        user = User.getByEmail({"email": post_data['email']})
        if not user:
            flash("Invalid Email Credentials")
            return False
        if not bcrypt.check_password_hash(user.password, post_data['password']):
            flash("Invalid password")
            return False
        return True