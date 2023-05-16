from flask import Flask, render_template, request, redirect, url_for, json
from flask_sqlalchemy import SQLAlchemy
import os


app = Flask(__name__, static_folder="static/", template_folder="html/")
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = -1
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://root:@localhost/learning_flask'


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


  



@app.route('/registry/', methods=["GET", "POST"])
def registry():

	if request.method == "POST":
		login = request.form.get('login')
		password = request.form.get('password')
		db.session.add(User(login, password))
		db.session.commit()
	return render_template("index.html")


@app.route('/login/', methods=["GET", "POST"])
def login():

	if request.method == "POST":
		login = request.form.get('login')
		password = request.form.get('password')
		loginning(login, password)

	return render_template("index.html")

@app.route('/main', methods=["POST", "GET"])
def main():
	# data = json.loads(request.data)
	# if data['isAuth'] == True:
	# 	return render_template('main.html', name=data['name'])
	# return redirect(url_for('/login'))
	login = request.form.get('name')
	return render_template('main.html')




# if __name__ == '__main__':
# 	app.run()
