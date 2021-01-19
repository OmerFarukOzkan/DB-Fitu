import psycopg2
connection = psycopg2.connect("postgres://xifgxuynwnxfjq:5cf0e94393316b2a2ea6717aaf0198e5ac7733e81869d4932bab8f837d015df5@ec2-23-23-88-216.compute-1.amazonaws.com:5432/d10vn8r7hs5nr4",sslmode = 'require')    
cursor = connection.cursor()
def initt():
    query = '''CREATE TABLE IF NOT EXISTS users(
        user_id SERIAL PRIMARY KEY,
        user_name VARCHAR(30) UNIQUE NOT NULL,
        password VARCHAR(300) NOT NULL,
        height INTEGER NOT NULL,
        point INTEGER,
        CHECK (point>=0 and point<=5),
        weight FLOAT NOT NULL
    );'''
    cursor.execute(query)
    connection.commit()
        
    query = '''CREATE TABLE IF NOT EXISTS Food(
        food_id SERIAL PRIMARY KEY,
        food_name VARCHAR(30) NOT NULL,
        calorie INTEGER NOT NULL,
        photo VARCHAR(30) NOT NULL,
        content VARCHAR(300) NOT NULL
    );'''
    cursor.execute(query)
    connection.commit()

    query = '''CREATE TABLE IF NOT EXISTS Exercise(
        ex_id SERIAL PRIMARY KEY, 
        body_part VARCHAR(30) NOT NULL,
        exercise_name VARCHAR(50) NOT NULL,
        photo VARCHAR(30) NOT NULL,
        content VARCHAR(1000) NOT NULL
    );'''
    cursor.execute(query)
    connection.commit()    


    query = '''CREATE TABLE IF NOT EXISTS Comment(
        comment_id SERIAL PRIMARY KEY,
        user_id INTEGER NOT NULL,
        author VARCHAR(30),
        content VARCHAR(255) NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE ON UPDATE CASCADE
    );'''
    cursor.execute(query)
    connection.commit()

    query = '''CREATE TABLE IF NOT EXISTS Trainer(
        trainer_id SERIAL PRIMARY KEY,
        trainer_name VARCHAR(30) UNIQUE NOT NULL,
        password VARCHAR(250) UNIQUE NOT NULL,
        score FLOAT,
        age INTEGER NOT NULL,
        gender VARCHAR(10) NOT NULL,
        count INTEGER,
        experience_year INTEGER NOT NULL 
    );'''
    cursor.execute(query)
    connection.commit()

    query = '''CREATE TABLE IF NOT EXISTS trainer_rel(
    user_id INTEGER PRIMARY KEY ,
    trainer_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (trainer_id) REFERENCES trainer(trainer_id) ON DELETE CASCADE ON UPDATE CASCADE
    );'''
    cursor.execute(query)
    connection.commit()

    query = '''CREATE TABLE IF NOT EXISTS Exer_list(
        elist_id SERIAL PRIMARY KEY,
        user_id INTEGER NOT NULL,
        numb_of_ex INTEGER NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE ON UPDATE CASCADE
    );'''
    cursor.execute(query)
    connection.commit()   

    query = '''CREATE TABLE IF NOT EXISTS Exer_rel(
        elist_id INTEGER NOT NULL,
        ex_id INTEGER NOT NULL,
        FOREIGN KEY (elist_id) REFERENCES Exer_list(elist_id) ON DELETE CASCADE ON UPDATE CASCADE,
        FOREIGN KEY (ex_id) REFERENCES Exercise(ex_id) ON DELETE CASCADE ON UPDATE CASCADE
    );'''
    cursor.execute(query)
    connection.commit()
 

    query = '''CREATE TABLE IF NOT EXISTS Menu_list(
        mlist_id SERIAL PRIMARY KEY,
        user_id INTEGER NOT NULL,
        numb_of_food INTEGER NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE ON UPDATE CASCADE
    );'''
    cursor.execute(query)
    connection.commit()
    
    query = '''CREATE TABLE IF NOT EXISTS Food_rel(
        food_id INTEGER NOT NULL,
        mlist_id INTEGER NOT NULL,
        FOREIGN KEY (food_id) REFERENCES Food(food_id) ON DELETE CASCADE ON UPDATE CASCADE,
        FOREIGN KEY (mlist_id) REFERENCES Menu_list(mlist_id) ON DELETE CASCADE ON UPDATE CASCADE
    );'''
    cursor.execute(query)
    connection.commit()




    query = '''INSERT INTO trainer(trainer_name,password,score,age,gender,count,experience_year) VALUES('Erce Can Bekture','$pbkdf2-sha256$29000$1lorxdjbe48RAiCEcI6R8g$bdDWS9JFYN4Gga7B6GOo3.9VvbQjA.C70SPX8Xf90gg',
    0.0,20,'Male',0,1);'''
    cursor.execute(query)
    connection.commit()

    query = '''INSERT INTO trainer(trainer_name,password,score,age,gender,count,experience_year)  VALUES('Orhan Yılmaz','$pbkdf2-sha256$29000$5hwDQMhZK8XYmxMiRGjNGQ$ffOlYGbatNOBJP8VjtFaslYTFENCxV1lQVu0iVD3M7k',
    0.0,32,'Male',0,13);'''
    cursor.execute(query)
    connection.commit()

    query = '''INSERT INTO trainer(trainer_name,password,score,age,gender,count,experience_year)  VALUES('Tuğçe Çağlayan','$pbkdf2-sha256$29000$AeDcm1Nqbe1da03p3TunFA$1s0awCe/99rfl4w1Ndy.SAVDlkef4DM02OA1TMviZbw',
    0.0,41,'Female',0,20);'''
    cursor.execute(query)
    connection.commit()

    query = '''INSERT INTO trainer(trainer_name,password,score,age,gender,count,experience_year)  VALUES('Furkan Halifeoğlu','$pbkdf2-sha256$29000$COGcU.odwxhj7P2fszam1A$Szha4E.KrZowHTE0PwanE7a8l5lAyugyvANG5rGcGnk',
    0.0,25,'Male',0,5);'''
    cursor.execute(query)
    connection.commit()

    query = '''INSERT INTO trainer(trainer_name,password,score,age,gender,count,experience_year)  VALUES('Berkay Türkkan','$pbkdf2-sha256$29000$LSWE8L4XQshZC8FYa40xxg$xntELIZwlB4oCxos13D8F0di9rsr25qR4hL7uRe/JNs',
    0.0,29,'Male',0,6);'''
    cursor.execute(query)
    connection.commit()

    query = '''INSERT INTO trainer(trainer_name,password,score,age,gender,count,experience_year)  VALUES('Savaş Cebeci','$pbkdf2-sha256$29000$0JozphQCQGjNubf2PmcMAQ$YgWvUjAwI7S36x5RiTXS5TyAvCCiP3EkHX6drpuy0cE',
    0.0,44,'Male',0,22);'''
    cursor.execute(query)
    connection.commit()

    query = '''INSERT INTO trainer(trainer_name,password,score,age,gender,count,experience_year)  VALUES('Testo Taylan','$pbkdf2-sha256$29000$Rsg5R6g1xnhPqRUCYGyNMQ$jkD81HPUDHf.JeGQKpzeNrguP7mR.7hkWUMpn6B9vkI',
    0.0,24,'Male',0,1);'''
    cursor.execute(query)
    connection.commit()

    query = '''INSERT INTO trainer(trainer_name,password,score,age,gender,count,experience_year)  VALUES('Rıza Kayaalp','$pbkdf2-sha256$29000$sNY6B2BMKUUIoZRSivF.jw$repCZuzsOwL.xUsZlS4xCsCAMhy.ZtxtE.t2f4HQfEE',
    0.0,33,'Male',0,10);'''
    cursor.execute(query)
    connection.commit()


    query = '''INSERT INTO exercise(body_part,exercise_name,photo,content) Values('Chest', 'Bench Press', 'benchpress.png', 'Adjust the seat back to the upright position. Adjust the seat so that the
    bench press handles are even with your chest. The bench press handles
    should be adjusted for a comfortable stretch, about even with the front
    of your chest. Too far back can cause excessive strain on your shoulders! Grab the handles with an overhand grip and press away from
    your chest. Do not lock out your elbows. Return slowly.' );'''
    cursor.execute(query)
    connection.commit()

    query = '''INSERT INTO exercise(body_part,exercise_name,photo,content) Values('Chest', 'Cable Incline Fly', 'cableinclinefly.png', 'Adjust the seat back to the upright position. Adjust the Functional
    Training Arms to their widest position. Sit upright on the seat and
    grab the handles with a neutral grip. Bring your arms together and
    upward in a circular motion. Return slowly.' );'''
    cursor.execute(query)
    connection.commit()

    query = '''INSERT INTO exercise(body_part,exercise_name,photo,content) Values('Chest', 'Stabilizing Chest Press', 'stabilizingchestpress.png', 'This exercise targets the chest muscles, but because it is done without back
    support, the core stabilizing muscles are also engaged. You will need to
    use a much lower weight than standard bench press exercises.
    Adjust the seat back to the upright position and the Functional Training Arms to chest height. Sit forward on the seat, without back support.
    Grab the cable handles with an overhand grip and press away from your
    chest. Return slowly.');'''
    cursor.execute(query)
    connection.commit()

    query = '''INSERT INTO exercise(body_part,exercise_name,photo,content) Values('Shoulder', 'Shoulder Press', 'shoulderpress.png', 'Adjust the seat back to one of the holes in the SHOULDER position.
    Your personal comfort will determine which hole. Adjust the Press
    Arm to one of the holes in the SHOULDER position. Finally, adjust
    the seat so that the press handles are at shoulder height. Sit back in
    the seat so that the seat back forces a forward lean. The idea is to
    align your body with the path of motion of the press arm, so that you
    are actually pushing the press handles overhead. Grab the handles
    with an overhand grip and press away from your shoulders. Do not
    lock out your elbows. Return slowly.' );'''
    cursor.execute(query)
    connection.commit()

    qeuery = '''INSERT INTO exercise(body_part,exercise_name,photo,content) Values('Shoulder', 'Cable Lateral Raise', 'cablelateralraise.png', 'Adjust the Functional Training Arms to a low position, about shoulder
    width apart. Sit upright on the seat and grab the cable handles with a
    neutral grip. While keeping your arms straight, raise your hands outward and upward. Lower slowly.' );'''
    cursor.execute(query)
    connection.commit()

    query = '''INSERT INTO exercise(body_part,exercise_name,photo,content) Values('Shoulder', 'Shrugs', 'shrugs.png', 'Attach the straight bar to the low pulley (on some models, this may
    be at the front of the leg extension lever). Stand on the foot plate
    and hold the bar at arms’ length. "Shrug" your shoulders upward
    and rearward. Lower slowly.' );'''
    cursor.execute(query)
    connection.commit()

    query = '''INSERT INTO exercise(body_part,exercise_name,photo,content) Values('Shoulder', 'External Rotator', 'externalrotator.png', 'Stand beside your machine and adjust the Functional Training Arm to
    elbow height. For some, this exercise is more comfortable if you place
    a rolled up towel under your upper arm. Grasp the handle, using a
    neutral grip, with your outside arm. Rotate your arm, as if it were an
    opening door, away from your midsection. Return slowly.' );'''
    cursor.execute(query)
    connection.commit()

    query = '''INSERT INTO exercise(body_part,exercise_name,photo,content) Values('Back', 'Lat Pull Down', 'latpulldown.png', 'Adjust the seat to its lowest position. Attach the lat bar to the high
    pulley. Sit facing the machine and lock your knees under the knee
    hold-down pads. Grab the lat bar with a wide, overhand grip. Keep
    your upper body stationary and pull straight down to your upper
    chest. Return slowly.' );'''
    cursor.execute(query)
    connection.commit()

    query = '''INSERT INTO exercise(body_part,exercise_name,photo,content) Values('Back', 'Low Cable Row', 'lowcablerow.png', 'Attach the straight bar to the low pulley. Sit on the floor facing the
    low pulley, feet on foot plate (against leg extension pads for GXP).
    Keep your upper torso stationary and pull the straight bar to your
    midsection. Squeeze your shoulder blades together. Return slowly.' );'''
    cursor.execute(query)
    connection.commit()

    query = '''INSERT INTO exercise(body_part,exercise_name,photo,content) Values('Back', 'Front Lat Pullover', 'fronlatpullover.png', 'Although the picture does not show this, you may need to use the
    supplied length of chain on this exercise. Otherwise, the weight stack
    can easily “top out” and damage a pulley. Attach the chain to the high
    pulley, and then attach the straight bar to the end of the chain. Grab
    the straight bar with an overhand grip. Keep your arms straight and
    pull down. Return slowly.' );'''
    cursor.execute(query)
    connection.commit()

    query = '''INSERT INTO exercise(body_part,exercise_name,photo,content) Values('Arm', 'Cable Arm Curl', 'cablearmcurl.png', 'Adjust the seat back to the upright position and the Functional Training Arms to their lowest position. Sit upright on the seat and grasp the
    handles with an underhand grip. Try to keep your elbows and upper
    arm stationary while you curl the handles upward, using your biceps
    muscles. Lower slowly.' );'''
    cursor.execute(query)
    connection.commit()
    
    query = '''INSERT INTO exercise(body_part,exercise_name,photo,content) Values('Arm', 'Overhead Biceps Curl', 'benchpress.png', 'Attach the straight bar to the high pulley. Sit facing the machine and
    lock your knees under the knee hold-down pads. Grab the straight bar
    with an underhand grip. Concentrate on keeping your upper arm stationary while curling the straight bar behind your head. Return slowly.' );'''
    cursor.execute(query)
    connection.commit()

    query = '''INSERT INTO exercise(body_part,exercise_name,photo,content) Values('Arm', 'Triceps Pushdown', 'tricepspushdown.png', 'It is important to use the supplied length of chain on this exercise.
    Otherwise, the weight stack can easily “top out” and damage a pulley. Attach the chain to the high pulley and then attach the straight
    bar to the end of the chain. Stand in front of the high pulley and
    grab the straight bar with an overhand grip. Pull the bar downward to a point where you can lock your elbows at your sides. The
    motion is the opposite of an arm curl; push downward on the bar,
    flexing at the elbow. Return slowly. Use a full range of motion.' );'''
    cursor.execute(query)
    connection.commit()

    query = '''INSERT INTO exercise(body_part,exercise_name,photo,content) Values('Arm', 'Triceps Kickback', 'tricepskickback.png', 'Attach a single handle to a Functional Training Arm and adjust it to
    a low position. Stand beside the machine in front of the Functional
    Training Arm. Bend at the waist to near horizontal. Grab the single
    handle with a neutral grip. Try to lock your upper arm at your side
    while extending your lower arm at the elbow. Return slowly.' );'''
    cursor.execute(query)
    connection.commit()

    query = '''INSERT INTO exercise(body_part,exercise_name,photo,content) Values('Core', 'Ab Crunch', 'abcrunch.png', 'Adjust the seat to the lowest position and the seat back to the upright
    position. Attach the ab strap to the cable end located behind your head.
    Drape the ab strap over your shoulders and hold it in place. Use your
    abdominal muscles to crunch forward and downward. Return slowly.' );'''
    cursor.execute(query)
    connection.commit()

    query = '''INSERT INTO exercise(body_part,exercise_name,photo,content) Values('Core', 'Oblique Twist', 'obliquetwist.png', 'Adjust one Functional Training Arm to its highest position and stand
    aside of it. Grab the handle and pull it to your stomach. Hold the
    handle stationary. Lock your hips into place and twist your upper
    torso. Return slowly.' );'''
    cursor.execute(query)
    connection.commit()

    query = '''INSERT INTO exercise(body_part,exercise_name,photo,content) Values('Core', 'Reverse Crunch', 'reversecrunch.png', 'Sit on the seat and grasp the handles, or sides of seat. Extend your legs to a
    horizontal position. Draw your knees toward your chest. Return slowly..' )'''
    cursor.execute(query)
    connection.commit()

    query = '''INSERT INTO exercise(body_part,exercise_name,photo,content) Values('Leg', 'Leg Extension', 'legextension.png', 'Adjust the seat and the seat back so that, when seated, your knees are
    aligned with the pivot point on the leg extension lever arm. Sit and
    hook your ankles behind the lower roller pads. Grasp the handles, or
    the sides of the seat, and extend your legs to horizontal. Return slowly.' );'''
    cursor.execute(query)
    connection.commit()

    query = '''INSERT INTO exercise(body_part,exercise_name,photo,content) Values('Leg', 'Standing Leg Curl', 'standinglegcurl.png', 'Stand facing the machine. Adjust the seat so that the connected roller
    pads are above your knee. Grab the seat back, or the press arm for
    stability. Position your ankles behind the lower set of roller pads. Using one leg at a time, bend your knee backward and upward as far as
    possible. Return slowly.' );'''
    cursor.execute(query)
    connection.commit()

    insert = '''INSERT INTO food(food_name,calorie,photo,content) VALUES ('Whole Eggs','80','wholeegg.png','Eggs are very filling and nutrient-dense. Compared to refined carbs like bagels, eggs can suppress appetite later in the day and may even promote weight loss.
    ');'''
    cursor.execute(insert)
    connection.commit()

    insert = '''INSERT INTO food(food_name,calorie,photo,content) VALUES ('Leafy Greens','40','leafygreens.png','Leafy greens are an excellent addition to your weight loss diet. Not only are they low in calories but also high in fiber that helps keep you feeling full.
    ');'''
    cursor.execute(insert)
    connection.commit()

    insert = '''INSERT INTO food(food_name,calorie,photo,content) VALUES ('Salmon','35','salmon.png','Salmon is high in both protein and omega-3 fatty acids, making it a good choice for a healthy weight loss diet.
    ');'''
    cursor.execute(insert)
    connection.commit()

    insert = '''INSERT INTO food(food_name,calorie,photo,content) VALUES ('Cruciferous Vegetables','35','cruciferousvegetables.png','Cruciferous vegetables are low in calories but high in fiber and nutrients. Adding them to your diet is not only an excellent weight loss strategy but may also improve your overall health.
    ');'''
    cursor.execute(insert)
    connection.commit()

    insert = '''INSERT INTO food(food_name,calorie,photo,content) VALUES ('Lean Beef','35','leanbeef.png','Eating unprocessed lean meat is an excellent way to increase your protein intake. Replacing some of the carbs or fat in your diet with protein could make it easier for you to lose excess fat.
    ');'''
    cursor.execute(insert)
    connection.commit()

    insert = '''INSERT INTO food(food_name,calorie,photo,content) VALUES ('Boiled Potatoes','35','boiledpatato.png','Boiled potatoes are among the most filling foods. They’re particularly good at reducing your appetite, potentially suppressing your food intake later in the day.
    ');'''
    cursor.execute(insert)
    connection.commit()

    insert = '''INSERT INTO food(food_name,calorie,photo,content) VALUES ('Tuna','35','tuna.png','Tuna is an excellent, lean source of high-quality protein. Replacing other macronutrients, such as carbs or fat, with protein is an effective weight loss strategy on a calorie-restricted diet.
    ');'''
    cursor.execute(insert)
    connection.commit()

    insert = '''INSERT INTO food(food_name,calorie,photo,content) VALUES ('Beans','35','beans.png','Beans and legumes are a good addition to your weight loss diet. They’re both high in protein and fiber, contributing to feelings of fullness and a lower calorie intake.
    ');'''
    cursor.execute(insert)
    connection.commit()

    insert = '''INSERT INTO food(food_name,calorie,photo,content) VALUES ('Soups','35','soups.png','Soups can be an effective part of a weight loss diet. Their high water content makes them very filling. However, try to avoid creamy or oily soups.
    ');'''
    cursor.execute(insert)
    connection.commit()

    insert = '''INSERT INTO food(food_name,calorie,photo,content) VALUES ('Cottage Cheese','35','cottagecheese.png','Eating lean dairy products, such as cottage cheese, is one of the best ways to get more protein without significantly increasing your calorie intake.
    ');'''
    cursor.execute(insert)
    connection.commit()

    insert = '''INSERT INTO food(food_name,calorie,photo,content) VALUES ('Avocados','35','avocado.png','Avocados are a good example of a healthy fat source you can include in your diet while trying to lose weight. Just make sure to keep your intake moderate.
    ');'''
    cursor.execute(insert)
    connection.commit()

    insert = '''INSERT INTO food(food_name,calorie,photo,content) VALUES ('Chili Pepper','35','chilipeppers.png','Eating spicy foods that contain chili peppers may reduce your appetite temporarily and even increase fat burning. However, tolerance seems to build up in those who eat chili regularly.
    ');'''
    cursor.execute(insert)
    connection.commit()