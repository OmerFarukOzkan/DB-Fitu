from classes import Exer_list, Exercise, Exer_rel, User, Comment, Trainer, Food, Food_rel, Menu_list
import psycopg2
from passlib.handlers.sha2_crypt import sha512_crypt
from flask import current_app
from flask_login import UserMixin

class Database():
    def __init__(self,database_url):
        self.connection = psycopg2.connect(database_url, sslmode = 'require')
        
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
            insert = "INSERT INTO users (user_name, password, height, weight, point) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(insert, (new_user.user_name, new_user.password, new_user.height, new_user.weight, 0))
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

    def update_user(self,cur_id,cname,cpassword,cheight,cweight):
        if cname:
            with self.connection.cursor(cursor_factory = psycopg2.extras.DictCursor) as cursor:
                query = "UPDATE users SET user_name = %s WHERE user_id = %s"
                cursor.execute(query,(cname,cur_id))
                self.connection.commit()
        if cpassword:
            with self.connection.cursor(cursor_factory = psycopg2.extras.DictCursor) as cursor:
                query = "UPDATE users SET password = %s WHERE user_id = %s"
                cursor.execute(query,(cpassword,cur_id))
                self.connection.commit()
        if cheight:
            with self.connection.cursor(cursor_factory = psycopg2.extras.DictCursor) as cursor:
                query = "UPDATE users SET height = %s WHERE user_id = %s"
                cursor.execute(query,(cheight,cur_id))
                self.connection.commit()
        if cweight:
            with self.connection.cursor(cursor_factory = psycopg2.extras.DictCursor) as cursor:
                query = "UPDATE users SET weight = %s WHERE user_id = %s"
                cursor.execute(query,(cweight,cur_id))
                self.connection.commit()

    def delete_user(self,cur_id):
        with self.connection.cursor(cursor_factory = psycopg2.extras.DictCursor) as cursor:
            query = "DELETE FROM users WHERE user_id = %s"
            cursor.execute(query,[cur_id])
            self.connection.commit()

    def add_trainer_to_user(self,user_id,trainer_id,point,old_point):
        with self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            query = "INSERT INTO trainer_rel(user_id,trainer_id) VALUES(%s,%s)"
            cursor.execute(query,[user_id,trainer_id])
            self.connection.commit()
            query = "UPDATE trainer SET score = %s,count=count+1 WHERE trainer_id = %s"
            cursor.execute(query,(point,trainer_id))
            self.connection.commit()
            query = "UPDATE users SET point = %s WHERE user_id = %s"
            cursor.execute(query,(old_point,user_id))
            self.connection.commit()

    def get_trainer_name(self,user_id):
        with self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            query = "SELECT trainer_id FROM trainer_rel WHERE user_id = %s"
            cursor.execute(query,[user_id])
            trainer_ = cursor.fetchone()
            if(trainer_ is None):
                return None
            trainer_id = trainer_[0]
            query = "SELECT trainer_name FROM trainer WHERE trainer_id = %s"
            cursor.execute(query,[trainer_id])
            trainer_name = cursor.fetchone()
        return trainer_name

    def have_trainer(self,user_id):
        with self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            query = "SELECT * FROM trainer_rel WHERE user_id = %s"
            cursor.execute(query,[user_id])
            trainer_ = cursor.fetchone()
            if(trainer_):
                return 1
        return 0

    def get_avg_age(self):
        with self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            query = "SELECT AVG(age) FROM trainer"
            cursor.execute(query)
            avg_age = cursor.fetchone()
        return avg_age

    def check_user_name(self,name):
        with self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            query = "SELECT EXISTS (SELECT true FROM users WHERE user_name = %s)"
            cursor.execute(query,[name])
            x = cursor.fetchone()
        return x[0]

    
    @property    
    def is_active(self):
        return self.active

# Comment
    def get_all_comments(self):
        with self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            query = "SELECT * FROM comment ORDER BY comment_id"
            cursor.execute(query)
            all_comments = cursor.fetchall()
        return all_comments

    def delete_comment(self,id,user_id):
        with self.connection.cursor(cursor_factory = psycopg2.extras.DictCursor) as cursor:
            query = "DELETE FROM comment WHERE comment_id = %s and user_id = %s"
            cursor.execute(query,(id,user_id))
            self.connection.commit()

    def add_comment(self, new_comment):
        with self.connection as con:
            cursor = con.cursor()
            insert = "INSERT INTO comment (user_id, author, content) VALUES (%s, %s, %s)"
            cursor.execute(insert, (new_comment.user_id, new_comment.author, new_comment.content))
            con.commit()
            return 
    
    def get_user_comments(self, user_id):
        with self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            query = "SELECT * FROM comment WHERE user_id = %s"
            cursor.execute(query,[user_id])
            out = cursor.fetchall()
        return out

    def update_comment(self,id,content):
        with self.connection.cursor(cursor_factory = psycopg2.extras.DictCursor) as cursor:
            query = "UPDATE comment SET content = %s WHERE comment_id = %s"
            cursor.execute(query,(content,id))
            self.connection.commit()


# Exercise 
    
    def get_exercises(self):
        if self.last_exercise_key is not None:  
            with self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
                query = "SELECT * FROM exercise order by ex_id"
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
    
    def get_cal_sum(self):
        with self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            query = "SELECT sum(calorie) FROM food"
            cursor.execute(query)
            cal_sum = cursor.fetchone()
        return cal_sum
    
    def get_all_foods(self,id):
        with self.connection.cursor(cursor_factory = psycopg2.extras.DictCursor) as cursor:
            query = "SELECT mlist_id FROM menu_list WHERE user_id = %s"
            cursor.execute(query,[id])
            users_lists = cursor.fetchall()
            a = len(users_lists)
            query = ""
            for i in users_lists:
                query = query + "SELECT food_id FROM food_rel WHERE mlist_id = " + str(i[0])
                a -= 1
                if(a):
                    query = query + " UNION "
            if query == "":
                return
            cursor.execute(query)

            x = cursor.fetchall()
            arr = []
            for i in x:
                query = "SELECT food_name FROM food WHERE food_id = %s"
                cursor.execute(query,[i[0]])
                arr.append(cursor.fetchone())
            return arr


# Trainer
    def add_trainer(self, new_trainer):
        self.last_trainer_key += 1
        self.trainers[self.last_trainer_key] = new_trainer
        return self.last_trainer_key


    def get_trainer(self, trainer_id = None,trainer_name = None):
        if trainer_id is not None:
            with self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
                query = "SELECT * FROM trainer WHERE trainer_id = %s"
                cursor.execute(query, [trainer_id])
                result = cursor.fetchone()
            return result
        else:
            with self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
                query = "SELECT * FROM trainer WHERE trainer_name = %s"
                cursor.execute(query, [trainer_name])
                result = cursor.fetchone()
            return result


    def update_trainer(self,cur_id,cname,cpassword):
        if cname:
            with self.connection.cursor(cursor_factory = psycopg2.extras.DictCursor) as cursor:
                query = "UPDATE trainer SET trainer_name = %s WHERE trainer_id = %s"
                cursor.execute(query,(cname,cur_id))
                self.connection.commit()
        if cpassword:
            with self.connection.cursor(cursor_factory = psycopg2.extras.DictCursor) as cursor:
                query = "UPDATE trainer SET password = %s WHERE trainer_id = %s"
                cursor.execute(query,(cpassword,cur_id))
                self.connection.commit()

    def delete_trainer(self,cur_id):
        with self.connection.cursor(cursor_factory = psycopg2.extras.DictCursor) as cursor:
            query = "SELECT user_id FROM trainer_rel WHERE trainer_id = %s"
            cursor.execute(query,[cur_id])
            usert = cursor.fetchall()
            for p in usert:
                query = "UPDATE users SET point = 0 WHERE user_id = %s"
                cursor.execute(query,(p))
                self.connection.commit()
            query = "DELETE FROM trainer WHERE trainer_id = %s"
            cursor.execute(query,[cur_id])
            self.connection.commit()

    def get_trainers(self):  
        with self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            query = "SELECT * FROM trainer ORDER BY trainer_id"
            cursor.execute(query)
            all_trainers = cursor.fetchall()
        return all_trainers


#ex_list

    def check_user_name(self,name):
        with self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            query = "SELECT EXISTS (SELECT true FROM users WHERE user_name = %s)"
            cursor.execute(query,[name])
            x = cursor.fetchone()
        return x[0]
    def check_exercise(self,exl_id,id):
        with self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            query = "SELECT EXISTS (SELECT true FROM exer_rel WHERE elist_id = %s and ex_id = %s)"
            cursor.execute(query,(exl_id,id))
            x = cursor.fetchone()
        return x[0] 



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
            query = "SELECT COUNT(ex_id) FROM exer_rel WHERE elist_id = %s GROUP BY elist_id"
            cursor.execute(query,[elist_id])
            b = cursor.fetchone()
            query = "UPDATE exer_list SET numb_of_ex = %s WHERE elist_id = %s"
            cursor.execute(query,[b[0],elist_id])
            self.connection.commit()

    def add_exercise_to_list(self,elist_id,exer_id):
        with self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            query = "SELECT ex_id FROM exer_rel WHERE elist_id = %s and ex_id = %s"
            cursor.execute(query,[elist_id,exer_id])
            xx = cursor.fetchone()
            if xx:
                return
            query = "INSERT INTO exer_rel(elist_id,ex_id) VALUES(%s,%s)"
            cursor.execute(query,[elist_id,exer_id])
            self.connection.commit()

    def get_users_ex_lists(self,user_id):
        with self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            query = '''SELECT ex_id,elist_id FROM (SELECT	exer_rel.elist_id,	exer_rel.ex_id,	exer_list.user_id,	exer_list.numb_of_ex FROM exer_rel 
            INNER JOIN exer_list ON exer_list.elist_id = exer_rel.elist_id ) AS query WHERE user_id = %s'''
            cursor.execute(query,[user_id])
            person_exer_lists = cursor.fetchall()
        return person_exer_lists

#food_list

    def check_food(self,mlist_id,id):
        with self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            query = "SELECT EXISTS (SELECT true FROM food_rel WHERE mlist_id = %s and food_id = %s)"
            cursor.execute(query,(mlist_id,id))
            x = cursor.fetchone()
        return x[0] 

    def create_food_list(self,person_id):
        with self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            query = "INSERT INTO menu_list(user_id,numb_of_food) VALUES(%s,%s)"
            cursor.execute(query,[person_id,0])
            self.connection.commit()
            query = "SELECT * FROM menu_list WHERE user_id = %s"
            cursor.execute(query,[person_id])
            persons_food_lists = cursor.fetchall()
            food_list_id = persons_food_lists[len(persons_food_lists)-1][0]
        return food_list_id

    def food_list_update(self,mlist_id):
        with self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            query = "SELECT COUNT(food_id) FROM food_rel WHERE mlist_id = %s GROUP BY mlist_id"
            cursor.execute(query,[mlist_id])
            b = cursor.fetchone()
            query = "UPDATE menu_list SET numb_of_food = %s WHERE mlist_id = %s"
            cursor.execute(query,[b[0],mlist_id])
            self.connection.commit()

    def add_food_to_list(self,mlist_id,food_id):
        with self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            query = "SELECT food_id FROM food_rel WHERE mlist_id = %s and food_id = %s"
            cursor.execute(query,[mlist_id,food_id])
            xx = cursor.fetchone()
            if xx:
                return
            query = "INSERT INTO food_rel(mlist_id,food_id) VALUES(%s,%s)"
            cursor.execute(query,[mlist_id,food_id])
            self.connection.commit()

    def get_users_food_lists(self,user_id):
        with self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            query = '''SELECT food_id,mlist_id FROM (SELECT	food_rel.mlist_id,	food_rel.food_id,	menu_list.user_id,	menu_list.numb_of_food FROM food_rel 
            INNER JOIN menu_list ON menu_list.mlist_id = food_rel.mlist_id ) AS query WHERE user_id = %s'''
            cursor.execute(query,[user_id])
            person_food_lists = cursor.fetchall()
        return person_food_lists