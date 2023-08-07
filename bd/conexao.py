from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

app = Flask(__name__, template_folder='..\\templates')
CORS(app)
app.config['SECRET_KEY'] = '4846ASDASD'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sqlite3.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)