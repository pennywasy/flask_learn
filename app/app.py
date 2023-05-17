from flask import Flask, render_template, request, redirect, url_for, json, session
from flask_sqlalchemy import SQLAlchemy
import os


app = Flask(__name__, static_folder="static/", template_folder="html/")
app.secret_key = 'VERYSECRET'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = -1
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///C:/Users/Egorov/Documents/flask_learn/app/test.db'


db = SQLAlchemy(app)


class User(db.Model):

	__tablename__ = "user"
	id = db.Column(db.Integer, primary_key=True)
	login = db.Column(db.String(100), nullable=False)
	password = db.Column(db.String(100), nullable=False)

	def __init__(self, login, password):
		self.login = login
		self.password = password

	def __repr__(self):
		return "{}".format(self.login)


def loginning(login, password):
	if User.query.filter_by(login=login, password=password).first():
		return True
	return False


  
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
		if loginning(login, password):
			session['isAuth'] = True
			session['login'] = login
			return redirect(url_for('main'))

	return render_template("form.html")

@app.route('/main/', methods=["POST", "GET"])
def main():
	if session['isAuth']:
		login = session['login']
		print(login)
		return render_template('main.html', name=login)
	return redirect(url_for('index'))


@app.route('/logout/')
def logout():
	session['isAuth'] = False
	session['name'] = None
	return redirect(url_for('index'))



# if __name__ == '__main__':
# 	app.run()
