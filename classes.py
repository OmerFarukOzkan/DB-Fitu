from flask import current_app
from flask_login import UserMixin

class Exer_list:
    def __init__(self, elist_id, user_id, numb_of_ex):
        self.elist_id = elist_id
        self.user_id = user_id
        self.numb_of_ex = numb_of_ex

class Exer_rel:
    def __init__(self, elist_id, ex_id):
        self.elist_id = elist_id
        self.ex_id = ex_id
        
class Exercise:
    def __init__(self, ex_id, body_part, exercise_name, photo, content):
        self.ex_id = ex_id
        self.body_part = body_part
        self.exercise_name = exercise_name
        self.photo = photo
        self.content = content
        
class Trainer:
    def __init__(self, trainer_id, trainer_name, password, score, age, gender, count, experience_year):
        self.trainer_id = trainer_id
        self.trainer_name = trainer_name
        self.password = password
        self.score = score
        self.age = age
        self.gender = gender
        self.count = count
        self.experience_year = experience_year
        
class User(UserMixin):
    def __init__(self, user_id, trainer_id, user_name, password, height, weight, point):
        self.user_id = user_id
        self.user_name = user_name
        self.password = password
        self.height = height
        self.weight = weight
        self.point = point
        self.active = True
    @property    
    def is_active(self):
        return self.active
        
class Comment:
    def __init__(self, comment_id, user_id, author, content):
        self.comment_id = comment_id
        self.user_id = user_id
        self.author = author
        self.content = content
class Menu_list:
    def __init__(self, mlist_id, user_id, numb_of_food):
        self.mlist_id = mlist_id
        self.user_id = user_id
        self.numb_of_food = numb_of_food

class Food_rel:
    def __init__(self, food_id, mlist_id):
        self.food_id = food_id
        self.mlist_id = mlist_id

class Food:
    def __init__(self, food_id, food_name, calorie, photo, content):
        self.food_id = food_id
        self.food_name = food_name
        self.calorie = calorie
        self.photo = photo
        self.content = content