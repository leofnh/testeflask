from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__, template_folder='..\\templates')
app.config['SECRET_KEY'] = '4846ASDASD'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sqlite3.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)