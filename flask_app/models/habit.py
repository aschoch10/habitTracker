from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL
from flask_bcrypt import Bcrypt
from flask_app import app

bcrypt = Bcrypt(app)

class Habit:
    schema = ("habittracker_schema")
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.streak_count = data['streak_count']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    @classmethod
    def getById(cls, data):
        query = "SELECT * FROM habits WHERE email = %(id)s;"
        results = connectToMySQL(cls.schema).query_db(query, data)
        if len(results) < 1:
            return False
        return Habit(results[0])


    @classmethod
    def readAll(cls):
        query = "SELECT * FROM habits;"
        results = connectToMySQL(cls.schema).query_db(query)
        habits = []
        for row in results:
            habits.append(Habit(row))
        return habits

    @classmethod
    def create(cls, data):
        query = "INSERT into habits (user_id, name, description, streak_count) VALUES (%(user_id)s, %(name)s, %(description)s, %(streak_count)s);"
        return connectToMySQL(cls.schema).query_db(query, data)
    
    @classmethod
    def readOne(cls, data):
        query = "SELECT * from habits WHERE id = %(id)s;"
        results = connectToMySQL(cls.schema).query_db(query, data)

        if len(results) <1:
            return False 
        return cls(results[0])

    @classmethod
    def update(cls, data):
        query = "UPDATE habits SET name = %(name)s, description = %(description)s, streak_count = %(streak_count)s WHERE id = %(id)s;"
        return connectToMySQL(cls.schema).query_db(query, data)


    @classmethod
    def destroy(cls, data):
        query = "DELETE from habits where id = %(id)s;"
        connectToMySQL(cls.schema).query_db(query, data)


# todo add validations for form input
    @staticmethod
    def validate(post_data):
        is_valid = True

        if len(post_data['name']) < 3:
            flash("Name must be longer than 3 characters")
            is_valid = False
        if len(post_data['description']) < 3:
            flash("Description must be longer than 3 characters")
            is_valid = False
        

        return is_valid