from flask import Flask, render_template, request, url_for, redirect, flash
import backendmodel as mod
import numpy as np
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

user_name = ''
login_status = 0
already_log = 0
Age = None

class users(db.Model):
    _id = db.Column("id", db.Integer, primary_key = True)
    age = db.Column(db.Integer, nullable = False)
    name = db.Column(db.String(50), nullable = False)
    email = db.Column(db.String(100), nullable = False)
    username = db.Column(db.String(100), nullable = False, unique = True)
    password = db.Column(db.String(100), nullable = False)
    login_Status = db.Column(db.Boolean, nullable = False)
    status = db.Column(db.String(50), nullable = True)


    def __init__(self, age, name, email, username, password, login_Status, status = ''):
        self.age = age
        self.name = name
        self.email = email
        self.username = username
        self.password = password
        self.login_Status = login_Status
        self.status = status

@app.route('/')
def main_page():
    global user_name, Age
    try:
        search = users.query.filter_by(login_Status = True).first()
        user_name = search.name
        Age = search.age

        return render_template('homepage.html', stat = 1, Data = user_name, login_Stat = login_status)
    except:
        return render_template('homepage.html', Data = user_name, stat = 0, login_Stat = login_status)

@app.route('/home', methods = ["POST", "GET"])
def home_page():
    global pred
    if (request.method == "POST"):
        age  = request.form["Age"]
        dia_BP = request.form["DiastolicBP"]
        sys_BP = request.form["SystolicBP"]
        blood_Sugar = request.form["BS"]
        body_Temp = request.form["BodyTemp"]
        heart_Rate = request.form["HeartRate"]

        print(age)

        X_data = [[age, dia_BP, sys_BP, blood_Sugar, body_Temp, heart_Rate]]
        pred = mod.Model(X_data)

        res = ["High Risk", "Low Risk", "Mid Risk"]

        if login_status:
            search = users.query.filter_by(login_Status = True).first()
            print(res[pred])
            search.status = res[pred]
            db.session.commit()
            
        if (pred == 0):
            return render_template('highrisk.html', login_Stat = login_status)
        elif (pred == 1):
            return render_template('lowrisk.html', login_Stat = login_status)
        else:
            return render_template('midrisk.html', login_Stat = login_status)
    
    else:
        if Age:
            return render_template('mainpage.html', age = Age, login_Stat = login_status)
        else:
            return render_template('mainpage.html', age = 0, login_Stat = login_status)

@app.route('/signup', methods = ['GET', 'POST'])
def signup_page():
    global user_name
    global login_status
    global age
    global already_log

    search = users.query.filter_by(login_Status = True).first()

    if search:
        login_status = 1
        user_name = search.name
        age = search.age
        print("Hello")

    if (not login_status):
        if (request.method == 'POST'):
            name = request.form['Name']
            age = request.form['Age']
            email = request.form['Email']
            uname = request.form['Uname']
            passwd = request.form['Password']
            try:
                usr = users(age, name, email, uname, passwd, 1)
                db.session.add(usr)
                db.session.commit()

                login_status = 1
                user_name = name

                return render_template('after_signup.html', login_Stat = login_status)
            except:
                return render_template('signup.html', stat = 1, login_Stat = login_status)

        else:
            return render_template('signup.html', login_Stat = login_status)
    
    else:
        already_log = 1
        return render_template('login_page.html', login_Stat = login_status)
    
    
@app.route('/login', methods = ['GET', 'POST'])
def login_page():
    global user_name
    global login_status
    global already_log
    global age

    search = users.query.filter_by(login_Status = True).first()

    if search:
        login_status = 1
        user_name = search.name
        age = search.age

    if (not login_status):
        if(request.method == 'POST'):
            username = request.form["username"]
            password = request.form["password"]

            data = users.query.filter_by(username = username, password = password).first()

            if data:
                user_name = data.name
                data.login_Status = True
                db.session.commit()
                login_status = 1
                already_log = 0
                return render_template('after_login.html', login_Stat = login_status)
                
            else:
                return render_template('login.html', stat = 1, login_Stat = login_status)

        else:
            return render_template('login.html', login_Stat = login_status)
    else:
        already_log = 1
        return render_template('login_page.html', login_Stat = login_status)

            
@app.route('/logout')
def logout():
    global login_status, already_log, user_name, Age
    search = users.query.filter_by(login_Status = True).first()
    search.login_Status = False
    db.session.commit()
    user_name = ''
    login_status = 0
    already_log = 0
    Age = None

    return render_template('logout.html', login_Stat = login_status)

@app.route('/about')
def about_page():
    return render_template('about.html', login_Stat = login_status)

@app.route('/profile')
def profile_page():
    search = users.query.filter_by(login_Status = True).first()
    return render_template('profile.html', name = search.name, age = search.age, email = search.email, uname = search.username, login_Stat = 1, pred = search.status)
    

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run()