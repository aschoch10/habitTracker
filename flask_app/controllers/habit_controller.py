
from flask import render_template, request, redirect, session, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.habit import Habit
from datetime import datetime, date, timedelta, time



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


@app.route('/habits/<int:id>/increase', methods = ['POST'])
def increase(id):
    data = {
        **request.form,
        "id":id,
    }
    # convert [updated_at] to datetime object
    # print(datetime.strptime(data['updated_at'], "%Y-%m-%d %H:%M:%S"))
    # print(type(timedelta(hours=12)))
    # print(type(datetime.now()))
    if(datetime.strptime(data['updated_at'], "%Y-%m-%d %H:%M:%S")) < (datetime.now()) - (timedelta(hours=18)):
        print("it HAS been more than twelve hours your streak has been updated")
        data["streak_count"] +1
        Habit.update(data)
    else: print ("It hasn't been more than twelve hours")
    return redirect ("/dashboard")


@app.route('/habits/<int:id>/destroy')
def destroy(id):
        Habit.destroy({"id": id })
        return redirect("/dashboard")


@app.route('/habits/<int:id>/reset', methods = ['POST'])
def reset(id):
    data = {
        **request.form,
        "id":id,
    }
    data['streak_count'] = 0
    Habit.update(data)
    return redirect("/dashboard")

