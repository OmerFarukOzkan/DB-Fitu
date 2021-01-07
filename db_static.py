import psycopg2

create = '''CREATE TABLE Trainer(
    trainer_id SERIAL PRIMARY KEY,
    trainer_name VARCHAR(30) UNIQUE NOT NULL,
    string VARCHAR(250) UNIQUE NOT NULL,
    score FLOAT,
    age INTEGER NOT NULL,
    gender VARCHAR(10) NOT NULL,
    count INTEGER,
    experience_year INTEGER NOT NULL 
); '''
cursor.execute(query)
connection.commit()

create = '''CREATE TABLE users(
    user_id SERIAL PRIMARY KEY, 
    trainer_id INTEGER,
    user_name VARCHAR(30) UNIQUE NOT NULL,
    password VARCHAR(300) NOT NULL,
    height INTEGER NOT NULL,
    point INTEGER,
    CHECK (point>=1 and point<=5),
    weight FLOAT NOT NULL,
    FOREIGN KEY (trainer_id) REFERENCES Trainer(trainer_id)
);'''
cursor.execute(query)
connection.commit()

create = '''CREATE TABLE Comment(
    comment_id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    author VARCHAR(30),
    type INTEGER,
    CHECK (type>=0 and type <=2),
    content VARCHAR(255) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES User(user_id)
);'''
cursor.execute(query)
connection.commit()

create = '''CREATE TABLE Exer_list(
    elist_id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    numb_of_ex INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES User(user_id)
);'''
cursor.execute(query)
connection.commit()

create = '''CREATE TABLE Exercise(
    ex_id SERIAL PRIMARY KEY, 
    body_part VARCHAR(30) NOT NULL,
    exercise_name VARCHAR(50) NOT NULL
);'''
cursor.execute(query)
connection.commit()

create = '''CREATE TABLE Menu_list(
    mlist_id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    numb_of_food INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES User(user_id)
);'''
cursor.execute(query)
connection.commit()

create = '''CREATE TABLE Food(
    food_id SERIAL PRIMARY KEY,
    food_name VARCHAR(30) NOT NULL,
    calorie INTEGER NOT NULL
);'''
cursor.execute(query)
connection.commit()

create = '''CREATE TABLE Exer_rel(
    elist_id INTEGER NOT NULL,
    ex_id INTEGER NOT NULL,
    FOREIGN KEY (elist_id) REFERENCES Exer_list(elist_id)
    ON DELETE CASCADE,
    FOREIGN KEY (ex_id) REFERENCES Exercise(ex_id)
);'''
cursor.execute(query)
connection.commit()

create = '''CREATE TABLE Food_rel(
    food_id INTEGER NOT NULL,
    mlist_id INTEGER NOT NULL,
    FOREIGN KEY (food_id) REFERENCES Food(food_id),
    FOREIGN KEY (mlist_id) REFERENCES Menu_list(mlist_id)
    ON DELETE CASCADE
);'''
cursor.execute(query)
connection.commit()

insert = '''INSERT INTO exercise('Chest', 'Bench Press', 'benchpress.png', 'Adjust the seat back to the upright position. Adjust the seat so that the
bench press handles are even with your chest. The bench press handles
should be adjusted for a comfortable stretch, about even with the front
of your chest. Too far back can cause excessive strain on your shoulders! Grab the handles with an overhand grip and press away from
your chest. Do not lock out your elbows. Return slowly.' );'''

insert = '''INSERT INTO exercise('Chest', 'Cable Incline Fly', 'cableinclinefly.png', 'Adjust the seat back to the upright position. Adjust the Functional
Training Arms to their widest position. Sit upright on the seat and
grab the handles with a neutral grip. Bring your arms together and
upward in a circular motion. Return slowly.' );'''

insert = '''INSERT INTO exercise('Chest', 'Stabilizing Chest Press', 'stabilizingchestpress.png', 'This exercise targets the chest muscles, but because it is done without back
support, the core stabilizing muscles are also engaged. You will need to
use a much lower weight than standard bench press exercises.
Adjust the seat back to the upright position and the Functional Training Arms to chest height. Sit forward on the seat, without back support.
Grab the cable handles with an overhand grip and press away from your
chest. Return slowly.' );'''

insert = '''INSERT INTO exercise('Shoulder', 'Shoulder Press', 'shoulderpress.png', 'Adjust the seat back to one of the holes in the SHOULDER position.
Your personal comfort will determine which hole. Adjust the Press
Arm to one of the holes in the SHOULDER position. Finally, adjust
the seat so that the press handles are at shoulder height. Sit back in
the seat so that the seat back forces a forward lean. The idea is to
align your body with the path of motion of the press arm, so that you
are actually pushing the press handles overhead. Grab the handles
with an overhand grip and press away from your shoulders. Do not
lock out your elbows. Return slowly.' );'''

insert = '''INSERT INTO exercise('Shoulder', 'Cable Lateral Raise', 'cablelateralraise.png', 'Adjust the Functional Training Arms to a low position, about shoulder
width apart. Sit upright on the seat and grab the cable handles with a
neutral grip. While keeping your arms straight, raise your hands outward and upward. Lower slowly.' );'''

insert = '''INSERT INTO exercise('Shoulder', 'Shrugs', 'shrugs.png', 'Attach the straight bar to the low pulley (on some models, this may
be at the front of the leg extension lever). Stand on the foot plate
and hold the bar at arms’ length. “Shrug” your shoulders upward
and rearward. Lower slowly.' );'''

insert = '''INSERT INTO exercise('Shoulder', 'External Rotator', 'externalrotator.png', 'Stand beside your machine and adjust the Functional Training Arm to
elbow height. For some, this exercise is more comfortable if you place
a rolled up towel under your upper arm. Grasp the handle, using a
neutral grip, with your outside arm. Rotate your arm, as if it were an
opening door, away from your midsection. Return slowly.' );'''

insert = '''INSERT INTO exercise('Back', 'Lat Pull Down', 'latpulldown.png', 'Adjust the seat to its lowest position. Attach the lat bar to the high
pulley. Sit facing the machine and lock your knees under the knee
hold-down pads. Grab the lat bar with a wide, overhand grip. Keep
your upper body stationary and pull straight down to your upper
chest. Return slowly.' );'''

insert = '''INSERT INTO exercise('Back', 'Low Cable Row', 'lowcablerow.png', 'Attach the straight bar to the low pulley. Sit on the floor facing the
low pulley, feet on foot plate (against leg extension pads for GXP).
Keep your upper torso stationary and pull the straight bar to your
midsection. Squeeze your shoulder blades together. Return slowly.' );'''

insert = '''INSERT INTO exercise('Back', 'Front Lat Pullover', 'fronlatpullover.png', 'Although the picture does not show this, you may need to use the
supplied length of chain on this exercise. Otherwise, the weight stack
can easily “top out” and damage a pulley. Attach the chain to the high
pulley, and then attach the straight bar to the end of the chain. Grab
the straight bar with an overhand grip. Keep your arms straight and
pull down. Return slowly.' );'''

insert = '''INSERT INTO exercise('Arm', 'Cable Arm Curl', 'cablearmcurl.png', 'Adjust the seat back to the upright position and the Functional Training Arms to their lowest position. Sit upright on the seat and grasp the
handles with an underhand grip. Try to keep your elbows and upper
arm stationary while you curl the handles upward, using your biceps
muscles. Lower slowly.' );'''

insert = '''INSERT INTO exercise('Arm', 'Overhead Biceps Curl', 'benchpress.png', 'Attach the straight bar to the high pulley. Sit facing the machine and
lock your knees under the knee hold-down pads. Grab the straight bar
with an underhand grip. Concentrate on keeping your upper arm stationary while curling the straight bar behind your head. Return slowly.' );'''

insert = '''INSERT INTO exercise('Arm', 'Triceps Pushdown', 'tricepspushdown.png', 'It is important to use the supplied length of chain on this exercise.
Otherwise, the weight stack can easily “top out” and damage a pulley. Attach the chain to the high pulley and then attach the straight
bar to the end of the chain. Stand in front of the high pulley and
grab the straight bar with an overhand grip. Pull the bar downward to a point where you can lock your elbows at your sides. The
motion is the opposite of an arm curl; push downward on the bar,
flexing at the elbow. Return slowly. Use a full range of motion.' );'''

insert = '''INSERT INTO exercise('Arm', 'Triceps Kickback', 'tricepskickback.png', 'Attach a single handle to a Functional Training Arm and adjust it to
a low position. Stand beside the machine in front of the Functional
Training Arm. Bend at the waist to near horizontal. Grab the single
handle with a neutral grip. Try to lock your upper arm at your side
while extending your lower arm at the elbow. Return slowly.' );'''

insert = '''INSERT INTO exercise('Core', 'Ab Crunch', 'abcrunch.png', 'Adjust the seat to the lowest position and the seat back to the upright
position. Attach the ab strap to the cable end located behind your head.
Drape the ab strap over your shoulders and hold it in place. Use your
abdominal muscles to crunch forward and downward. Return slowly.' );'''

insert = '''INSERT INTO exercise('Core', 'Oblique Twist', 'obliquetwist.png', 'Adjust one Functional Training Arm to its highest position and stand
aside of it. Grab the handle and pull it to your stomach. Hold the
handle stationary. Lock your hips into place and twist your upper
torso. Return slowly.' );'''

insert = '''INSERT INTO exercise('Core', 'Reverse Crunch', 'reversecrunch.png', 'Sit on the seat and grasp the handles, or sides of seat. Extend your legs to a
horizontal position. Draw your knees toward your chest. Return slowly..' );'''

insert = '''INSERT INTO exercise('Leg', 'Leg Extension', 'legextension.png', 'Adjust the seat and the seat back so that, when seated, your knees are
aligned with the pivot point on the leg extension lever arm. Sit and
hook your ankles behind the lower roller pads. Grasp the handles, or
the sides of the seat, and extend your legs to horizontal. Return slowly.' );'''

insert = '''INSERT INTO exercise('Leg', 'Standing Leg Curl', 'standinglegcurl.png', 'Stand facing the machine. Adjust the seat so that the connected roller
pads are above your knee. Grab the seat back, or the press arm for
stability. Position your ankles behind the lower set of roller pads. Using one leg at a time, bend your knee backward and upward as far as
possible. Return slowly.' );'''

insert = '''INSERT INTO exercise('Leg', 'Leg Press', 'legpress.png', 'This exercise can only be performed if you have purchased the optional
leg press attachment. Adjust the seat back to a comfortable position. You should try to get as close as possible to the foot plate, yet
not so close that your knees are against your chest, forcing your knees
outward. Place your feet squarely on the foot plates and press outward
to full extension. Be careful not to lock out your knees! Locking your
knees is extending a bit too far and can result in injury. Return slowly.' );'''

insert = '''INSERT INTO exercise('Leg', 'Glute Kick', 'glutekick.png', 'Stand facing the machine and attach the ankle strap to one leg. Stand and
grab the seat back, or press arm for support, pelvis tilted forward. Extend
the hip and pull your leg backward.' );'''

insert = '''INSERT INTO food(food_name,calorie,photo,content) VALUES ('Whole Eggs','80','wholeegg.png','Eggs are very filling and nutrient-dense. Compared to refined carbs like bagels, eggs can suppress appetite later in the day and may even promote weight loss.
');'''

insert = '''INSERT INTO food(food_name,calorie,photo,content) VALUES ('Leafy Greens','40','leafygreens.png','Leafy greens are an excellent addition to your weight loss diet. Not only are they low in calories but also high in fiber that helps keep you feeling full.
');'''

insert = '''INSERT INTO food(food_name,calorie,photo,content) VALUES ('Salmon','35','salmon.png','Salmon is high in both protein and omega-3 fatty acids, making it a good choice for a healthy weight loss diet.
');'''

insert = '''INSERT INTO food(food_name,calorie,photo,content) VALUES ('Cruciferous Vegetables','35','cruciferousvegetables.png','Cruciferous vegetables are low in calories but high in fiber and nutrients. Adding them to your diet is not only an excellent weight loss strategy but may also improve your overall health.
');'''

insert = '''INSERT INTO food(food_name,calorie,photo,content) VALUES ('Lean Beef','35','leanbeef.png','Eating unprocessed lean meat is an excellent way to increase your protein intake. Replacing some of the carbs or fat in your diet with protein could make it easier for you to lose excess fat.
');'''

insert = '''INSERT INTO food(food_name,calorie,photo,content) VALUES ('Boiled Potatoes','35','boiledpatato.png','Boiled potatoes are among the most filling foods. They’re particularly good at reducing your appetite, potentially suppressing your food intake later in the day.
');'''

insert = '''INSERT INTO food(food_name,calorie,photo,content) VALUES ('Tuna','35','tuna.png','Tuna is an excellent, lean source of high-quality protein. Replacing other macronutrients, such as carbs or fat, with protein is an effective weight loss strategy on a calorie-restricted diet.
');'''

insert = '''INSERT INTO food(food_name,calorie,photo,content) VALUES ('Beans','35','beans.png','Beans and legumes are a good addition to your weight loss diet. They’re both high in protein and fiber, contributing to feelings of fullness and a lower calorie intake.
');'''

insert = '''INSERT INTO food(food_name,calorie,photo,content) VALUES ('Soups','35','soups.png','Soups can be an effective part of a weight loss diet. Their high water content makes them very filling. However, try to avoid creamy or oily soups.
');'''

insert = '''INSERT INTO food(food_name,calorie,photo,content) VALUES ('Cottage Cheese','35','cottagecheese.png','Eating lean dairy products, such as cottage cheese, is one of the best ways to get more protein without significantly increasing your calorie intake.
');'''

insert = '''INSERT INTO food(food_name,calorie,photo,content) VALUES ('Avocados','35','avocado.png','Avocados are a good example of a healthy fat source you can include in your diet while trying to lose weight. Just make sure to keep your intake moderate.
');'''

insert = '''INSERT INTO food(food_name,calorie,photo,content) VALUES ('Chili Pepper','35','chilipeppers.png','Eating spicy foods that contain chili peppers may reduce your appetite temporarily and even increase fat burning. However, tolerance seems to build up in those who eat chili regularly.
');'''