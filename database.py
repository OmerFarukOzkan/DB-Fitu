from classes import Exer_list, Exercise, Exer_rel, User, Comment, Trainer, Food, Food_rel, Menu_list
import psycopg2
from passlib.handlers.sha2_crypt import sha512_crypt
from flask import current_app
from flask_login import UserMixin
import os

db_url = os.environ.get('DATABASE_URL')

class Database():
    def __init__(self):
        self.connection = psycopg2.connect(db_url, sslmode='require')
        self.cur = self.connection.cursor()

        self.users = {}
        self.exercises = {}
        self.foods = {}
        self.comments = {}
        self.trainers = {}
        self.last_trainer_key = 0
        self.last_user_key = 0
        self.last_exercise_key = 0
        self.last_food_key = 0
        self.last_comment_key = 0

# User
    def add_user(self, new_user):
        with self.connection as con:
            cursor = con.cursor()
            insert = "INSERT INTO users (user_name, password, height, weight) VALUES (%s, %s, %s, %s)"
            cursor.execute(insert, (new_user.user_name, new_user.password, new_user.height, new_user.weight))
            con.commit()
            self.last_user_key += 1
            self.users[self.last_user_key] = new_user
            return self.last_user_key   


    def get_user(self, user_name=None, user_id=None):
        if user_id is not None:
            with self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
                query = "SELECT * FROM users WHERE user_id = %s"
                cursor.execute(query, [user_id])
                result = cursor.fetchone()
            return result
        else:
            with self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
                query = "SELECT * FROM users WHERE user_name = %s"
                cursor.execute(query, [user_name])
                result = cursor.fetchone()
            return result
        
    def get_users(self):
        if self.last_user_key is not None:
            with self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
                query = "SELECT * FROM users ORDER BY user_id"
                cursor.execute(query)
                all_users = cursor.fetchall()
        return all_users

    def get_last_user_key(self):
        return self.last_user_key-1
    
    @property    
    def is_active(self):
        return self.active


# Exercise 
    def add_exercise(self, new_exercise):
        self.last_exercise_key += 1
        self.exercises[self.last_exercise_key] = new_exercise
        return self.last_exercise_key
    def get_exercise(self, key):
        exercise__ = self.exercises[key]
        if exercise__ is None:
            return None
        returned_exercise = Exercise(exercise__.ex_id, exercise__.body_part, exercise__.exercise_name, exercise__.photo, exercise__.content)
    
    def get_exercises(self):
        if self.last_exercise_key is not None:  
            with self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
                query = "SELECT * FROM exercise ORDER BY ex_id"
                cursor.execute(query)
                all_exercises = cursor.fetchall()
        return all_exercises

#Foods

    def get_foods(self):
        if self.last_food_key is not None:  
            with self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
                query = "SELECT * FROM food ORDER BY food_id"
                cursor.execute(query)
                all_foods = cursor.fetchall()
        return all_foods



# Trainer
    def add_trainer(self, new_trainer):
        self.last_trainer_key += 1
        self.trainers[self.last_trainer_key] = new_trainer
        return self.last_trainer_key
    

#ex_list

    def create_exercise_list(self,person_id):
        with self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            query = "INSERT INTO exer_list(user_id,numb_of_ex) VALUES(%s,%s)"
            cursor.execute(query,[person_id,0])
            self.connection.commit()
            query = "SELECT * FROM exer_list WHERE user_id = %s"
            cursor.execute(query,[person_id])
            persons_exer_lists = cursor.fetchall()
            exer_list_id = persons_exer_lists[len(persons_exer_lists)-1][0]
        return exer_list_id

    def exercise_list_update(self,elist_id):
        with self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            query = "SELECT COUNT (*) FROM exer_rel WHERE elist_id = %s"
            cursor.execute(query,[elist_id])
            a = cursor.fetchone()
            query = "UPDATE exer_list SET numb_of_ex = %s WHERE elist_id = %s"
            cursor.execute(query,[a[0],elist_id])
            self.connection.commit()

    def add_exercise_to_list(self,elist_id,exer_id):
        with self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            query = "INSERT INTO exer_rel(elist_id,ex_id) VALUES(%s,%s)"
            cursor.execute(query,[elist_id,exer_id])
            self.connection.commit()

    def get_users_ex_lists(self,user_id):
        with self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            query = "SELECT ex_id,elist_id FROM (SELECT	exer_rel.elist_id,	exer_rel.ex_id,	exer_list.user_id,	exer_list.numb_of_ex FROM exer_rel INNER JOIN exer_list ON exer_list.elist_id = exer_rel.elist_id ) AS query WHERE user_id = %s"
            cursor.execute(query,[user_id])
            person_exer_lists = cursor.fetchall()
        return person_exer_lists
