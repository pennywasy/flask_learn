from flask import Flask, render_template, request, redirect, url_for, json, session
from flask_sqlalchemy import SQLAlchemy 
from sqlalchemy.schema import PrimaryKeyConstraint
import os


app = Flask(__name__, static_folder="static/", template_folder="html/")
app.secret_key = 'VERYSECRET'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = -1
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///C:/Users/Egorov/Documents/flask_learn/app/test.db'


db = SQLAlchemy(app)


class User(db.Model):

	__tablename__ = "user"
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	login = db.Column(db.String(100), nullable=False, unique=True)
	password = db.Column(db.String(100), nullable=False)
	user_admin_id = db.relationship('Admins', backref='admin')
	user_entrie_id = db.relationship('Entries', backref='user')

	def __init__(self, login, password):
		self.login = login
		self.password = password



class Event(db.Model):
	__tablename__ = "event"
	id = db.Column(db.Integer, primary_key=True)
	description = db.Column(db.String(150), nullable=False)
	dateofevent = db.Column(db.Date, nullable=False)
	event_entrie_id = db.relationship('Entries', backref='event')


	def __init__(self, description, dateofevent):
		self.description = description
		self.dateofevent = dateofevent


class Admins(db.Model):
	__tablename__ = 'admins'
	id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
	


class Entries(db.Model):
	__tablename__ = 'entries'
	__table_args__ = (
		PrimaryKeyConstraint('user_id', 'event_id'),
	)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	event_id = db.Column(db.Integer, db.ForeignKey('event.id'))
	
	def __init__(self, user_id, event_id):
		self.user_id = user_id
		self.event_id = event_id



def getUser(login, password):
	return User.query.filter_by(login=login, password=password).first()

def getEvents():
	return Event.query.all()

def getEntries():
	return Entries.query.all()

@app.route('/main/loginEntries/', methods=["POST"])
def loginEntries():
	user_id = session['id']
	event_id = request.form.get('event')
	db.session.add(Entries(user_id, event_id))
	db.session.commit()
	return redirect(url_for('main'))


  
@app.route('/', methods=["GET"])
def index():
	return render_template('index.html')


@app.route('/registry/', methods=["GET", "POST"])
def registry():

	if request.method == "POST":
		login = request.form.get('login')
		password = request.form.get('password')
		db.session.add(User(login, password))
		db.session.commit()
	return render_template("form.html")


@app.route('/login/', methods=["GET", "POST"])
def login():

	if request.method == "POST":
		login = request.form.get('login')
		password = request.form.get('password')
		user = getUser(login, password)
		print(user.id)
		if user:
			session['isAuth'] = True
			session['login'] = login
			session['id'] = user.id
			return redirect(url_for('main'))

	return render_template("form.html")

@app.route('/main/', methods=["POST", "GET"])
def main():
	if session['isAuth']:
		login = session['login']
		events = getEvents()
		return render_template('main.html', name=login, events=events)
	return redirect(url_for('index'))


@app.route('/logout/')
def logout():
	session['isAuth'] = False
	session['name'] = None
	return redirect(url_for('index'))


