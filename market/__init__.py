from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SECRET_KEY'] = '618c21286d52ef876d89a6d1'
db = SQLAlchemy(app)
app.static_url_path = 'market/static'

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login_page"
login_manager.login_message_category ="info"
from market import route


"""
def create_database():
    db.create_all()
    print('Database Created')
    
    
    with app.app_context():
        create_database()
"""