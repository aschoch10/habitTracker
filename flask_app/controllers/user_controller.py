from flask import render_template, request, redirect, session, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.habit import Habit

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route('/')
def index():
    if "uuid" in session: 
        return redirect ('/dashboard')
    return render_template("index.html")


@app.route('/submit', methods=['POST'])
def submit():
    print(request.form)
    if not User.registerValidate(request.form):
        return redirect ('/')
    hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        **request.form,
        "password": hash
    }
    user_id = User.create(data)
    session['uuid'] = user_id
    return redirect ("/dashboard")


@app.route('/logout')
def LOGout():
    session.clear()
    return redirect("/")


@app.route('/login', methods = ['POST'])
def login():
    if not User.loginValidate(request.form):
        return redirect ('/')
    user = User.getByEmail({"email": request.form["email"]})
    session ['uuid'] = user.id
    return redirect("/dashboard")


@app.route('/dashboard')
def dashboard():
    if "uuid" not in session:
        return redirect("/")
    return render_template ("dashboard.html", 
    logged_in_user = User.getByID({"id": session["uuid"]}),
    # all_habits = Habit.readAll()
    )

# only can acces user controller from html buttons
# to do connect habit controller 
@app.route("/test")
def newHabit():
    return render_template("test.html")






