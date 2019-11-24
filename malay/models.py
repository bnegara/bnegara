from malay import db
from flask_login import UserMixin
from datetime import datetime

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    accountNumber = db.Column(db.String(120), nullable=True)
    accountBalance = db.Column(db.Integer, nullable=True, default=0.00)
    pendingBalance = db.Column(db.Integer, nullable=True, default=0.00)
    amountOnHold = db.Column(db.Integer, nullable=True, default=0.00)
    billing = db.Column(db.Integer, nullable=False, default=1)
    withdrawal = db.relationship('Withdrawal', backref='payee', lazy='dynamic')
    image = db.relationship('Image', backref='images', lazy='dynamic')
    

    def __str__(self):
        return f'User {self.username}'

class Withdrawal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    accountName = db.Column(db.String(120), nullable=False)
    bankName = db.Column(db.String(100))
    withdrawalAccountNumber = db.Column(db.String(120), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(100), default='Canceled')
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'), nullable=False)
    

    def __str__(self):
        return f'Withdrawal {self.accountName}'

class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String(50))
    date=db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'), nullable=False)

    def __str__(self):
        return f'Withdrawal {self.image}'