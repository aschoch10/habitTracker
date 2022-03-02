# to do code some more stuff I would imagine import re
from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL
from flask_bcrypt import Bcrypt
from flask_app import app

bcrypt = Bcrypt(app)

class Habit:
    schema = ("habittracker_schema")
    def __init__(self, data):
        self.id = data['id']
        self.name = data['first_name']
        self.description = data['description']
        self.streak_count = data['streak_count']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.recipes = []


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
