from enum import unique
from logging import debug
from flask import Flask, url_for, render_template, request, redirect, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
sc = "ThisIsASecret466"

   
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))


    def __init__(self, email, password):
        self.email = email
        self.password = password
        

admin = Admin(app)
admin.add_view(ModelView(User, db.session))


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            new = User(email=request.form.get['email'], unique=True, password=request.form.get['password'])
            db.session.add(new)
            db.session.commit()
            return redirect(url_for('login'))
        except:
            return render_template('register.html', register_message="User Already Exists")
    else:
        return render_template('register.html')


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        e = request.form['username']
        p = request.form['password']
        data = User.query.filter_by(email=e, password=p).first()
        if data is not None:
            session['logged_in'] = True
            return redirect(url_for('index'))
        return render_template('login.html', login_message="Sorry, I couldn't find you in our system. Please try again")


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session['logged_in'] = False
    return redirect(url_for('login'))



app.secret_key = sc

if __name__ == '__main__':
    app.run(debug=True)