from flask import Flask, render_template
from views import*
import views
from flask_login import LoginManager,current_user
from database import Database
from flask import current_app
from flask_login import UserMixin

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
    app.add_url_rule("/login_trainer", view_func = views.login_trainer, methods = ["GET","POST"])
    app.add_url_rule("/user_profile",view_func = views.user_profile)
    app.add_url_rule("/log_out_user",view_func = views.log_out_user)
    app.add_url_rule("/trainer_profile",view_func = views.trainer_profile)
    app.add_url_rule("/exercises",view_func=views.list_all_exercises)
    #app.add_url_rule("/list_all_exercises_to_create",view_func=views.list_all_exercises_to_create)
    app.add_url_rule("/create_exercise_list",view_func=views.create_exercise_list)
    app.add_url_rule("/exercise_list_update/<string:elist_id>",view_func=views.exercise_list_update)    
    app.add_url_rule("/dietfoods",view_func=views.list_all_foods)
    app.add_url_rule("/list_all_foods_to_create",view_func=views.list_all_foods_to_create)
    app.add_url_rule("/add_exercise_to_list/<int:id>/<string:exer_list_id>/<int:number_of_ex>",view_func=views.add_exercise_to_list)

    lm.init_app(app)
    lm.login_view = "login_user"

    db = Database()

    app.config["db"] = db
    
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host = "0.0.0.0", port = 8080, debug = True)
