from db import db


class User(db.Model):


	id = db.Column(db.Integer, primary_key=True)
	login = db.Column(db.String(100), nullable=False)
	password = db.Column(db.String(100), nullable=False)

  