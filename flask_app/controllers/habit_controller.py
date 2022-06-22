
from flask import render_template, request, redirect, session, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.habit import Habit
from datetime import datetime, date, timedelta



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


@app.route("/habits/<int:id>/edit")
def editShow(id):
    return render_template("test.html", 
    habit = Habit.readOne({"id": id})
    )


@app.route('/habits/<int:id>/increase', methods = ['POST'])
def increase(id):
    data = {
        **request.form,
        "updated_at":request.form['updated_at'],
        "id":id,
        "streak_count": int(request.form['streak_count']) +1,
    }
    Habit.update(data)
    print("updated at" + data['updated_at'])
    print(timedelta(hours=12))
    print(datetime.now())
    if "time" not in session:
        session["time"] = datetime.now()
    # if  data['updated_at'] + timedelta(hours=12) > session['time']:
        # print("it has been more than twelve hours")
    else: print ("it hasn't been more than twelve hours")
        # data['streak_count']+1
    Habit.update(data)

    return redirect ("/dashboard")

@app.route('/habits/<int:id>/destroy')
def destroy(id):
        session.pop("time")
        Habit.destroy({"id": id })
        return redirect("/dashboard")