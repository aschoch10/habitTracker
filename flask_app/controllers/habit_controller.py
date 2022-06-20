
from flask import render_template, request, redirect, session, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.habit import Habit


@app.route('/dashboard')
def dashboard():
    if "uuid" not in session:
        return redirect("/")
    return render_template ("dashboard.html", 
    logged_in_user = User.getByID({"id": session["uuid"]}),
    all_habits = Habit.readAll()
    )


@app.route("/habits/new")
def newHabit():
    return render_template("new_habit.html")


@app.route("/habits/create", methods = ['POST'])
def createHabit():
    if not Habit.validate(request.form):
        return redirect("/habits/new")
    data = {
        **request.form,
        "user_id": session['uuid']
    }
    Habit.create(data)
    return redirect('/dashboard')

@app.route('/increase')
def increase():
    if "num" not in session:
        session["num"] = 1
    else:
        session['num'] += 1
    return redirect ("/dashboard")

@app.route('/destroy')
def destroy():
    session.pop("num")
    return redirect("/dashboard")