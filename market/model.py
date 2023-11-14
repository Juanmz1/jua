""" import all necessary function """
from market import db, login_manager
from market import bcrypt
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    """ a class defining the user model """
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email_addr = db.Column(db.String(length=50), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)
    budget = db.Column(db.Integer(), nullable=False, default=500)
    items = db.relationship('Item', backref='owned_user', lazy=True)
    carts = db.relationship('Cart', backref='owned_user', lazy=True)
    orders = db.relationship('Order', backref='owned_user', lazy=True)

    def prettier_budget(self):
        if len(str(self.budget)) >= 4:
            return f'{str(self.budget)[:-3]},{str(self.budget)[-3:]}$'
        else:
            return f"{self.budget}$"
    @property
    def password(self):
        return self.password_hash

    @password.setter
    def password(self, plain_text_password):
        """ encrpyting the password """
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)



    def __repr__(self):
        return f'Item{self.username}'


class Item(db.Model):
    """ a class defining the item """
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30), nullable=False, unique=True)
    price = db.Column(db.Integer(), nullable=False)
    stock = db.Column(db.Integer(), nullable=False)
    item_picture = db.Column(db.String(10000), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    owner = db.Column(db.Integer(), db.ForeignKey('user.id'))
    carts = db.relationship('Cart', backref='item', lazy=True)
    orders = db.relationship('Order', backref='item', lazy=True)


    def __repr__(self):
        return f'Item{self.name, self.price}'


class Cart(db.Model):
    """ a class defining the cart section """
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    user_link = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=False)
    item_link = db.Column(db.Integer(), db.ForeignKey('item.id'), nullable=False)

    def __str__(self):
        return '<Cart %r>' % self.id

class Order(db.Model):
    """ a class defining the order section """
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(100), nullable=False)
    payment_id = db.Column(db.String(1000), nullable=False)
    user_link = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=False)
    item_link = db.Column(db.Integer(), db.ForeignKey('item.id'), nullable=False)

    def __str__(self):
        return '<Order %r>' % self.id
