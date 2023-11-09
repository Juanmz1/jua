from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://ghimfdxhlbpxpd:c38911c4c72fdb642f62d73eaccea174046b4f779bdb41e0dc5cc0023f21790c@ec2-35-169-11-108.compute-1.amazonaws.com:5432/depdt592d36ael'
#app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
#DATABASE_URL=postgresql://juanmrender_user:TQbrkxi5KgkPHyIpuXYxHMnGQ58CuOS8@dpg-cl58hmk72pts739ucilg-a.oregon-postgres.render.com/juanmrender
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