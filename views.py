from flask import render_template, request, session, redirect, url_for, flash, current_app
from classes import*
from database import Database
from flask_login import LoginManager,login_user,logout_user
import psycopg2.extras
import json 
from passlib.hash import pbkdf2_sha256
from functools import wraps
from flask_login import current_user
from flask import current_app
from flask_login import UserMixin

def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to login', 'danger')
            return redirect(url_for('login'))
    return wrap


def login_user():
    if request.method == 'POST':
        user = User("","","","","","","")
        user.user_name = request.form['user_name']
        user.password = request.form['password']
        db = current_app.config["db"]
        result = db.get_user(user.user_name)

        if result:
            real_password = result['password']
            if pbkdf2_sha256.verify(user.password, real_password):
                session['logged_in'] = True
                session['user_name'] = user.user_name
                session['user_id'] = result['user_id']
                session['trainer_id'] = result['trainer_id']
                session['password'] = result['password']
                session['height'] = result['height']
                session['weight'] = result['weight']
                session['point'] = result['point']
                flash('You are now logged in', 'success')
                return redirect(url_for('home_page'))
            else:
                error = "Invalid password"
                return render_template('sign_up.html', error = error)
        else:
            error = "Username not found"
            return render_template('sign_up.html', error = error)
    return render_template('sign_in.html')

def login_trainer():  #######
    if request.method() == 'POST':
        user = User("","","","","","","")
        user.user_name = request.form['user_name']
        user.password = request.form['password']
        result = db.get_user(user.user_name)

        if result:
            real_password = result['password']
            if sha256_crypt.verify(user.password, real_password):
                session['logged_in'] = True
                session['user_name'] = user.user_name
                session['user_id'] = result['user_id']
                session['trainer_id'] = result['trainer_id']
                session['password'] = result['password']
                session['height'] = result['height']
                session['weight'] = result['weight']
                session['point'] = result['point']
                flash('You are now logged in', 'success')
                return redirect(url_for('user_trainer'))
            else:
                error = "Invalid password"
                return render_template('sign_in.html', error = error)
        else:
            error = "Username not found"
            return render_template('sign_in.html', error = error)
        return render_template('sign_in.html')
    

def sign_up():
    if request.method == "POST":
        fname = request.form["user_name"]
        fheight = request.form["height"]
        fweight = request.form["weight"]
        fpassword = pbkdf2_sha256.hash(request.form["password"])
        

        user = User("", "", fname, fpassword, fheight, fweight, "")
        
        db = current_app.config["db"]
        user_key = db.add_user(user)
        return redirect(url_for("home_page", user_key = user_key))
    return render_template('sign_up.html')

def list_all_exercises():
    db = current_app.config["db"]
    exercises = db.get_exercises()
    image_paths =[]
    for i in exercises:
        image_paths.append(url_for('static', filename=i[3]))
    return render_template('exercises.html',exercises = exercises,image_paths = image_paths,create_mode = 0)

def list_all_foods():
    db = current_app.config["db"]
    foods = db.get_foods()
    image_paths =[]
    for i in foods:
        image_paths.append(url_for('static', filename=i[3]))
    
    return render_template('dietfoods.html',foods = foods,image_paths = image_paths,create_mode = 0)

def list_all_foods_to_create():
    db = current_app.config["db"]
    foods = db.get_foods()
    image_paths =[]
    for i in foods:
        image_paths.append(url_for('static', filename=i[3]))
    
    return render_template('dietfoods.html',foods = foods,image_paths = image_paths,create_mode = 1)


def home_page():
    db = current_app.config["db"]
    last_user_key = db.get_last_user_key()
    users = db.get_users()
    return render_template('index.html',all_users = users)

@is_logged_in
def create_exercise_list():
    db = current_app.config["db"]
    user_id = session['user_id']
    exer_list_id = db.create_exercise_list(user_id)
    exercises = db.get_exercises()
    image_paths =[]
    number_of_ex = 0
    for i in exercises:
        image_paths.append(url_for('static', filename=i[3]))
    return render_template('exercises.html',exercises = exercises,image_paths = image_paths,create_mode = 1,exer_list_id = exer_list_id,number_of_ex = number_of_ex)

@is_logged_in
def add_exercise_to_list(id,exer_list_id,number_of_ex):
    db = current_app.config["db"]
    db.add_exercise_to_list(exer_list_id,id)    
    exercises = db.get_exercises()
    image_paths =[]
    number_of_ex += 1
    for i in exercises:
        image_paths.append(url_for('static', filename=i[3]))
    return render_template('exercises.html',exercises = exercises,image_paths = image_paths,create_mode = 1,exer_list_id = exer_list_id,number_of_ex = number_of_ex)

@is_logged_in
def exercise_list_update(elist_id):
    db = current_app.config["db"]
    exercises = db.get_exercises()
    db.exercise_list_update(elist_id)
    cur_id = session['user_id']
    cur_users_ex_lists = db.get_users_ex_lists(cur_id)
    return render_template('user_profile.html',length = len(cur_users_ex_lists),user_ex_lists = cur_users_ex_lists,exercises = exercises,id = cur_id,name = session['user_name'],trainer_id = session['trainer_id'],height = session['height'],weight = session['weight'],point = session['point'])



@is_logged_in
def user_profile():
    db = current_app.config["db"]
    cur_id = session['user_id']
    exercises = db.get_exercises()
    cur_users_ex_lists = db.get_users_ex_lists(cur_id)
    print(cur_id)
    return render_template('user_profile.html',length = len(cur_users_ex_lists),user_ex_lists = cur_users_ex_lists,exercises = exercises,id = cur_id,name = session['user_name'],trainer_id = session['trainer_id'],height = session['height'],weight = session['weight'],point = session['point'])

@is_logged_in
def log_out_user():
    session.clear()
    flash("You have logged out.")
    return redirect(url_for('home_page'))

@is_logged_in
def trainer_profile():
    return