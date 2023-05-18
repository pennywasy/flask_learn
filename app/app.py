from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy 
from sqlalchemy.schema import PrimaryKeyConstraint
from PIL import Image
from io import BytesIO
from datetime import datetime
import base64
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
	avatar = db.Column(db.BLOB)
	user_admin_id = db.relationship('Admins', backref='admin')
	user_entrie_id = db.relationship('Entries', backref='user')

	def __init__(self, login, password, avatar):
		self.login = login
		self.password = password
		self.avatar = avatar



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
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=False)
	event_id = db.Column(db.Integer, db.ForeignKey('event.id'), unique=False)
	
	def __init__(self, user_id, event_id):
		self.user_id = user_id
		self.event_id = event_id



def getUser(login, password):
	return db.session.query(User.id, User.login, User.password).filter_by(login=login, password=password).first()

def getAvatar(id):
	return db.session.query(User.avatar).filter_by(id=id).all()

def getEvents():
	return Event.query.all()

def getEntries(id):
	entries = db.session.query(Event.description, Event.dateofevent, Entries.event_id).join(Entries, Entries.event_id == Event.id).join(User, User.id == Entries.user_id)
	entries = entries.filter(User.id == id).order_by(Event.dateofevent).all()
	return entries

def deleteEntries(user_id, event_id):
	entries = Entries.query.filter_by(user_id=user_id, event_id=event_id).first()
	db.session.delete(entries)
	db.session.commit()
	return 


def getAdmin(user_id):
	return Admins.query.filter_by(id=user_id).all()

def createEvent(description, dateofevent):
	dateofevent = datetime.strptime(dateofevent, '%Y-%m-%d')
	db.session.add(Event(description, dateofevent))
	db.session.commit()
	return


def updateAvatar(img, id):
	User.query.filter_by(id=id).update(dict(avatar=img))
	db.session.commit()
	return

@app.route('/main/updateAvatar', methods=['POST', 'GET'])
def newAvatar():
	avatar = request.files['avatar']
	img = base64.b64encode(avatar.read())
	updateAvatar(img, session['id'])
	return redirect(url_for('main'))


@app.route('/main/addEvent/', methods=['POST'])
def addEvent():
	if session['isAdmin']:
		description = request.form.get('eventName')
		dateofevent = request.form.get('eventDate')
		createEvent(description, dateofevent)
	return redirect(url_for('main'))


@app.route('/main/logoutEntries/<ID_event>', methods=["GET"])
def logoutEntries(ID_event):
	deleteEntries(session['id'], ID_event)
	return redirect(url_for('main'))



@app.route('/main/loginEntries/', methods=["POST"])
def loginEntries():
	user_id = session['id']
	event_id = int(request.form.get('event'))
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
		avatar = request.files['avatar']
		img = base64.b64encode(avatar.read())
		db.session.add(User(login, password, img))
		db.session.commit()
	return render_template("registry.html")


@app.route('/login/', methods=["GET", "POST"])
def login():

	if request.method == "POST":
		login = request.form.get('login')
		password = request.form.get('password')
		user = getUser(login, password)
		if user:
			session['isAuth'] = True
			session['login'] = login
			session['id'] = user.id
			if getAdmin(session['id']):
				session['isAdmin'] = True
				print(session['isAdmin'])
			return redirect(url_for('main'))

	return render_template("form.html")

@app.route('/main/', methods=["POST", "GET"])
def main():
	if session['isAuth']:
		login = session['login']
		events = getEvents()
		entries = getEntries(session['id'])
		avatar = (getAvatar(session['id'])[0][0])
		return render_template('main.html', name=login, events=events, entries=entries, avatar=f'{avatar}'[2:-1:])
	return redirect(url_for('index'))


@app.route('/logout/')
def logout():
	session['isAuth'] = False
	session['name'] = None
	session['isAdmin'] = False
	return redirect(url_for('index'))


