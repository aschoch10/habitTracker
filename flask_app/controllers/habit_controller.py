# to do code the stuff from flask import render_template, request, redirect, session, flash
from flask import render_template, request, redirect, session, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.user import Habit

@app.route('/dashboard')
def dashboard():
    if "uuid" not in session:
        return redirect("/")
    return render_template ("dashboard.html", 
    logged_in_user = User.getByID({"id": session["uuid"]}),
    all_habits = Habit.readAll()
    )