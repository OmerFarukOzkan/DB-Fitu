from flask import Flask, render_template
from views import*
import views
from flask_login import LoginManager,current_user
from database import Database
from flask import current_app
from flask_login import UserMixin
from db_static import initt
import os

lm = LoginManager()

@lm.user_loader
def load_user(user_id):
    return get_user(user_id)


def create_app():
    app = Flask(__name__)

    app.secret_key = 'hello'

    app.add_url_rule("/",view_func=views.home_page)
    app.add_url_rule("/login_user", view_func = views.login_user, methods = ["GET","POST"])
    app.add_url_rule("/sign_up", view_func = views.sign_up, methods = ["GET","POST"])
    app.add_url_rule("/sign_in", view_func = views.login_user, methods = ["GET","POST"])
    app.add_url_rule("/trainer_sign_in", view_func = views.login_trainer, methods = ["GET","POST"])
    app.add_url_rule("/login_trainer", view_func = views.login_trainer, methods = ["GET","POST"])
    app.add_url_rule("/user_profile",view_func = views.user_profile, methods = ["GET","POST"])
    app.add_url_rule("/log_out_page ",view_func = views.log_out_page)
    app.add_url_rule("/trainer_profile",view_func = views.trainer_profile)
    app.add_url_rule("/exercises",view_func=views.list_all_exercises)
    app.add_url_rule("/dietfoods",view_func=views.list_all_foods)
    app.add_url_rule("/create_exercise_list",view_func=views.create_exercise_list)
    app.add_url_rule("/create_food_list",view_func=views.create_food_list)
    app.add_url_rule("/exercise_list_update/<string:elist_id>",view_func=views.exercise_list_update)
    app.add_url_rule("/food_list_update/<string:mlist_id>",view_func=views.food_list_update)
    app.add_url_rule("/add_exercise_to_list/<int:id>/<string:exer_list_id>/<int:number_of_ex>",view_func=views.add_exercise_to_list)
    app.add_url_rule("/add_food_to_list/<int:id>/<string:food_list_id>/<int:number_of_food>",view_func=views.add_food_to_list)
    app.add_url_rule("/add_trainer_to_user/<int:user_id>/<int:trainer_id>/<int:point>",view_func=views.add_trainer_to_user)
    app.add_url_rule("/trainer_update",view_func=views.trainer_update, methods = ["GET","POST"])
    app.add_url_rule("/trainer_delete",view_func=views.trainer_delete)
    app.add_url_rule("/user_update",view_func=views.user_update, methods = ["GET","POST"])
    app.add_url_rule("/user_delete",view_func=views.user_delete)
    app.add_url_rule("/list_all_trainers",view_func=views.list_all_trainers)
    app.add_url_rule("/comment",view_func= views.comment, methods = ["GET","POST"])
    #app.add_url_rule("/update_comment",view_func= views.update_comment, methods = ["GET","POST"])
    app.add_url_rule("/delete_comment/<int:com_id>",view_func= views.delete_comment, methods = ["GET","POST"])
    
    
    lm.init_app(app)
    lm.login_view = "login_user"

    db = Database(os.environ.get("DATABASE_URL"))

    app.config["db"] = db
    
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host = "0.0.0.0", port = 8080, debug = True)
