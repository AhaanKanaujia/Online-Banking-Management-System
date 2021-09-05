from . import db 
from flask_login import UserMixin
from sqlalchemy.sql import func 

class Claim_FD(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    fd_index = db.Column(db.Integer())
    time = db.Column(db.DateTime(timezone=True), default= func.now())
    amount = db.Column(db.Integer())
    claim_amount = db.Column(db.Integer())
    status = db.Column(db.String(200), default = "Yet to mature!")
    time = db.Column(db.DateTime(timezone=True), default= func.now())
    note = note = db.Column(db.String(200))
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))

class Avail_Loan(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    loan_index = db.Column(db.Integer())
    amount = db.Column(db.Integer())
    repay_amount = db.Column(db.Integer())
    status = db.Column(db.String(200), default = "Repayment Due!")
    time = db.Column(db.DateTime(timezone=True), default= func.now())
    note = note = db.Column(db.String(200))
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))

class Make_Transaction(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    amount = db.Column(db.Integer())
    recipient_id = db.Column(db.Integer())
    time = db.Column(db.DateTime(timezone=True), default= func.now())
    note = note = db.Column(db.String(200))
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))

class Make_Deposit(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    amount = db.Column(db.Integer())
    source = db.Column(db.String(200))
    time = db.Column(db.DateTime(timezone=True), default= func.now())
    note = db.Column(db.String(200))
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))

class Make_Withdrawl(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    amount = db.Column(db.Integer())
    purpose = db.Column(db.String(200))
    time = db.Column(db.DateTime(timezone=True), default= func.now())
    note = db.Column(db.String(200))
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key = True)
    email = db.Column(db.String(150), unique= True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    password = db.Column(db.String(100))
    balance = db.Column(db.Integer(), default = 0)
    deposits = db.relationship('Make_Deposit')
    withdrawls = db.relationship('Make_Withdrawl')
    transactions = db.relationship('Make_Transaction')
    loans = db.relationship('Avail_Loan')
    fixed_deposits = db.relationship('Claim_FD')
