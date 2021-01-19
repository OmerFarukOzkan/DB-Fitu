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
            return redirect(url_for('home_page'))
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
                session['password'] = result['password']
                session['height'] = result['height']
                session['weight'] = result['weight']
                flash('You are now logged in', 'success')
                return redirect(url_for('home_page'))
            else:
                error = "Invalid password"
                return render_template('sign_in.html', error = error)
        else:
            error = "Username not found"
            return render_template('sign_in.html', error = error)
    return render_template('sign_in.html')

def login_trainer():  #######
    if  request.method == 'POST':
        trainer = Trainer("","","","","","","","")
        trainer.trainer_name = request.form['trainer_name']
        trainer.password = request.form['password']
        db = current_app.config["db"]
        result = db.get_trainer(None,trainer.trainer_name)
        if result:
            real_password = result['password']
            if pbkdf2_sha256.verify(trainer.password, real_password):
                session['logged_in'] = True
                session['trainer_name'] = trainer.trainer_name
                session['trainer_id'] = result['trainer_id']
                session['password'] = result['password']
                session['score'] = result['score']
                session['age'] = result['age']
                session['gender'] = result['gender']
                session['count'] = result['count']
                session['experience_year'] = result['experience_year']
                flash('You are now logged in', 'success')
                return redirect(url_for('trainer_profile'))
            else:
                error = "Invalid password"
                return render_template('trainer_sign_in.html', error = error)
        else:
            error = "Username not found"
            return render_template('trainer_sign_in.html', error = error)
    return render_template('trainer_sign_in.html')
    

@is_logged_in
def trainer_profile():
    db = current_app.config["db"]
    cur_id = session['trainer_id']
    trainer_ = db.get_trainer(cur_id)
    return render_template('trainer_main.html',trainer = trainer_)

@is_logged_in
def trainer_update():
    if request.method == 'POST':
        db = current_app.config["db"]
        cur_id = session['trainer_id']
        cname = request.form['trainer_name']
        cpassword = pbkdf2_sha256.hash(request.form['password'])
        db.update_trainer(cur_id,cname,cpassword)
        return redirect(url_for('trainer_profile'))
    return render_template('update.html',is_user = 0)

@is_logged_in
def user_update():
    if request.method == 'POST':
        db = current_app.config["db"]
        cur_id = session['user_id']
        cname = request.form['user_name']
        if cname:
            session['user_name'] = cname
        cheight = request.form['height']
        if cheight:
            session['height'] = cheight
        cweight = request.form['weight']
        if cweight:
            session['weight'] = cweight
        if len(request.form['password']):
            cpassword = pbkdf2_sha256.hash(request.form['password'])
            session['password'] = cpassword
        else:
            cpassword = ""
        db.update_user(cur_id,cname,cpassword,cheight,cweight)
        return redirect(url_for('user_profile'))
    return render_template('update.html',is_user = 1)

@is_logged_in
def trainer_delete():
    db = current_app.config["db"]
    cur_id = session['trainer_id']
    db.delete_trainer(cur_id)
    return redirect(url_for('log_out_page'))

@is_logged_in
def user_delete():
    db = current_app.config["db"]
    cur_id = session['user_id']
    db.delete_user(cur_id)
    return redirect(url_for('log_out_page'))


def sign_up():
    if request.method == "POST":
        fname = request.form["user_name"]
        fheight = request.form["height"]
        fweight = request.form["weight"]
        if(request.form["password"] != request.form["passwordag"]):
            return render_template("sign_up.html",error = "Passwords are not match.")
        fpassword = pbkdf2_sha256.hash(request.form["password"])
        db = current_app.config["db"]
        x = db.check_user_name(fname)
        if x:
            error = "This username already exists, please select another username !"
            return render_template("sign_up.html",error = error)
        user = User("", "", fname, fpassword, fheight, fweight, 0)
        
        db = current_app.config["db"]
        user_key = db.add_user(user)
        return redirect(url_for("home_page", user_key = user_key))
    return render_template('sign_up.html')


def home_page():
    db = current_app.config["db"]
    users = db.get_users()
    comments = db.get_all_comments()
    return render_template('index.html',comments = comments,all_users = users)

@is_logged_in
def comment():
    db = current_app.config["db"]
    comments = db.get_all_comments()
    user_ = db.get_user("",session['user_id'])
    if request.method == "GET":
        return render_template("comment.html",comments = comments)

    if request.method == "POST":
        if 'comment' in request.form:
            form_comment = request.form["comment"]
            new_comment = Comment("",session['user_id'],session['user_name'],form_comment)
            db.add_comment(new_comment)
            return redirect(url_for("comment"))
        if 'updated' in request.form:
            updated = request.form["updated"]
            id = request.form['id']
            db.update_comment(id,updated)
            return redirect(url_for("comment"))
    
    return render_template("comment.html",comments = comments)
            
@is_logged_in
def delete_comment(com_id):
    db = current_app.config["db"]
    db.delete_comment(com_id,session['user_id'])
    return redirect(url_for("comment"))

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
    cal = db.get_cal_sum()
    image_paths =[]
    for i in foods:
        image_paths.append(url_for('static', filename=i[3]))
    return render_template('foods.html',foods = foods,image_paths = image_paths,create_mode = 0,sum_of_cal = cal)

@is_logged_in
def list_all_trainers():
    db = current_app.config["db"]
    trainer_ = db.get_trainers()
    user_ = db.get_user("",session['user_id'])
    have_trainer = db.have_trainer(session['user_id'])
    avg_age = db.get_avg_age()
    return render_template('trainers.html',trainers = trainer_,user = user_,have_trainer = have_trainer,avg_age = avg_age)

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
def create_food_list():
    db = current_app.config["db"]
    user_id = session['user_id']
    food_list_id = db.create_food_list(user_id)
    foods = db.get_foods()
    image_paths =[]
    number_of_food = 0
    cal = db.get_cal_sum()
    for i in foods:
        image_paths.append(url_for('static', filename=i[3]))
    return render_template('foods.html',sum_of_cal = cal,foods = foods,image_paths = image_paths,create_mode = 1,food_list_id = food_list_id,number_of_food = number_of_food)

@is_logged_in
def add_exercise_to_list(id,exer_list_id,number_of_ex):
    db = current_app.config["db"]
    x = db.check_exercise(exer_list_id,id)
    exercises = db.get_exercises()
    image_paths =[]
    number_of_ex += 1
    for i in exercises:
        image_paths.append(url_for('static', filename=i[3]))
    if x:
        error = "You have already add this exercise to list, please select another one."
        return render_template('exercises.html',error = error, exercises = exercises,image_paths = image_paths,create_mode = 1,exer_list_id = exer_list_id,number_of_ex = number_of_ex)
    db.add_exercise_to_list(exer_list_id,id) 
    return render_template('exercises.html',exercises = exercises,image_paths = image_paths,create_mode = 1,exer_list_id = exer_list_id,number_of_ex = number_of_ex)

@is_logged_in
def add_trainer_to_user(user_id,trainer_id,point):
    db = current_app.config["db"]
    trainer = db.get_trainer(trainer_id)
    top = trainer[3] * trainer[6] + point
    new_point = top/(trainer[6] + 1)
    db.add_trainer_to_user(user_id,trainer_id,new_point,point)    
    return redirect(url_for('user_profile'))

@is_logged_in
def add_food_to_list(id,food_list_id,number_of_food):
    db = current_app.config["db"]
    x = db.check_food(food_list_id,id)  
    foods = db.get_foods()
    image_paths =[]
    number_of_food += 1
    cal = db.get_cal_sum()
    for i in foods:
        image_paths.append(url_for('static', filename=i[3]))
    if x:
        error = "You have already add this food to list, please select another one."
        return render_template('foods.html',error = error, sum_of_cal = cal,foods = foods,image_paths = image_paths,create_mode = 1,food_list_id = food_list_id,number_of_food = number_of_food)

    db.add_food_to_list(food_list_id,id)  
    return render_template('foods.html',sum_of_cal = cal,foods = foods,image_paths = image_paths,create_mode = 1,food_list_id = food_list_id,number_of_food = number_of_food)


@is_logged_in
def exercise_list_update(elist_id):
    db = current_app.config["db"]
    exercises = db.get_exercises()
    users = db.get_users()
    db.exercise_list_update(elist_id)
    cur_id = session['user_id']
    cur_users_ex_lists = db.get_users_ex_lists(cur_id)
    return redirect(url_for('home_page'))


@is_logged_in
def food_list_update(mlist_id):
    db = current_app.config["db"]
    foods = db.get_foods()
    users = db.get_users()
    db.food_list_update(mlist_id)
    cur_id = session['user_id']
    cur_users_food_lists = db.get_users_food_lists(cur_id)
    return redirect(url_for('home_page'))


@is_logged_in
def user_profile():
    db = current_app.config["db"]
    cur_id = session['user_id']
    trainer_name = db.get_trainer_name(cur_id)
    user_ = db.get_user("",cur_id)  
    exercises = db.get_exercises()
    cur_users_ex_lists = db.get_users_ex_lists(cur_id)
    foods = db.get_foods()
    cur_users_food_lists = db.get_users_food_lists(cur_id)
    have_trainer = db.have_trainer(cur_id)
    comments = db.get_user_comments(cur_id)
    all_foods = db.get_all_foods(cur_id)
    return render_template('user_profile.html',all_foods = all_foods, comments = comments, have_trainer = have_trainer,length = len(cur_users_ex_lists),length2 = len(cur_users_food_lists),user_food_lists = cur_users_food_lists,foods = foods,user_ex_lists = cur_users_ex_lists,exercises = exercises,user = user_,trainer_name = trainer_name)

@is_logged_in
def log_out_page():
    session.clear()
    flash("You have logged out.")
    return redirect(url_for('home_page'))

