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

# to do create form and controller to route to this
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
        recipes = []
        for row in results:
            recipes.append(Habit(row))
        return recipes
