from flask_app.config.mysqlconnection import connectToMySQL

from flask_app.models import user
from flask import flash 
from flask_app import app


class Recipe:
    schema= ("friends_bets_schema")
    def __init__(self, data):
        self.id = data['id']
        self.user = user.User.getByID({"id": data ['user_id']})
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']


    @classmethod
    def create(cls, data):
        query = "INSERT into recipes (user_id, name, description, instructions) VALUES (%(user_id)s, %(name)s, %(description)s, %(instructions)s);"
        return connectToMySQL(cls.schema).query_db(query, data)


    @classmethod
    def readAll(cls):
        query = "SELECT * FROM recipes;"
        results = connectToMySQL(cls.schema).query_db(query)

        recipes = []
        for row in results:
            recipes.append(Recipe(row))
        return recipes


    @classmethod
    def readOne(cls, data):
        query = "SELECT * from recipes WHERE id = %(id)s;"
        results = connectToMySQL(cls.schema).query_db(query, data)

        if len(results) <1:
            return False 
        return cls(results[0])


    @classmethod
    def update(cls, data):
        query = "UPDATE recipes SET name = %(name)s, description = %(description)s, instructions = %(instructions)s WHERE id = %(id)s;"
        return connectToMySQL(cls.schema).query_db(query, data)


    @classmethod
    def destroy(cls, data):
        query = "DELETE from recipes where id = %(id)s;"
        connectToMySQL(cls.schema).query_db(query, data)


    @staticmethod
    def validate(post_data):
        is_valid = True

        if len(post_data['name']) <2:
            flash("Name must be longer than 2 character")
            is_valid = False
        if len(post_data['description']) <4:
            flash("Description must be longer than 4 character")
            is_valid = False
        if len(post_data['instructions']) <4:
            flash("Instructions must be longer than 4 character")
            is_valid = False

        return is_valid


