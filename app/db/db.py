from .. import app
from User import User

from flask_sqlalchemy import SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:pass@localhost/test'


db = SQLAlchemy(app)

db.create_all()