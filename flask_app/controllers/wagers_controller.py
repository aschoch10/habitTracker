from flask import render_template, request, redirect, session, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.recipe import Recipe

@app.route('/dashboard')
def dashboard():
    if "uuid" not in session:
        return redirect("/")
    return render_template ("dashboard.html", 
    logged_in_user = User.getByID({"id": session["uuid"]}),
    all_recipes = Recipe.readAll()
    )


@app.route("/recipes/new")
def newRecipe():
    return render_template("new_recipe.html")


@app.route("/recipes/create", methods = ['POST'])
def createRecipe():
    if not Recipe.validate(request.form):
        return redirect("/recipes/new")
    data = {
        **request.form,
        "user_id": session['uuid']
    }
    Recipe.create(data)
    return redirect('/dashboard')


@app.route("/recipes/<int:id>")
def displayRecipe(id):
    return render_template("recipe.html",
    logged_in_user = User.getByID({"id": session["uuid"]}),
    recipe = Recipe.readOne({"id": id})
    )


@app.route("/recipes/<int:id>/edit")
def editRecipe(id):
    return render_template("edit_recipe.html", 
    recipe = Recipe.readOne({"id": id})
    )


@app.route("/recipes/<int:id>/update", methods=['POST'])
def updateRecipe(id):
    if not Recipe.validate(request.form):
        return redirect (f"/recipes/{id}/edit")
    data = {
        **request.form,
        "id":id
    }
    Recipe.update(data)
    return redirect ("/dashboard")


@app.route("/recipes/<int:id>/destroy")
def destroy(id):
    Recipe.destroy({"id": id })
    return redirect ('/dashboard ')





