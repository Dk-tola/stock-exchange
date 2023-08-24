from . import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    address = db.Column(db.String(250))
    city = db.Column(db.String(100))
    zipcode = db.Column(db.String(100))
    phonenumber = db.Column(db.String(100))
    bankaccount = db.Column(db.String(250))
    balance = db.Column(db.Float, default=10000.00)
    profit = db.Column(db.Numeric, default=0.00)


class User_Stock_Info(db.Model):
    transaction_id = db.Column("transaction_id", db.Integer, primary_key=True)
    stock_id = db.Column("stock_id", db.Integer)
    stock_price = db.Column("stock_price", db.Float)
    user_id = db.Column("user_id", db.String)
    quantity = db.Column("quantity", db.Float)
