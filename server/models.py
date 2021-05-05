# ----------------------------------------------------------------------------#
# Imports
# ----------------------------------------------------------------------------#
from flask import Flask
from flask_migrate import Migrate
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import datetime
from sqlalchemy import create_engine
from sqlalchemy.sql import text
from sqlalchemy.orm import backref
from sqlalchemy.types import ARRAY

# ----------------------------------------------------------------------------#
# App Config.
# ----------------------------------------------------------------------------#
db = SQLAlchemy()

def setup_db(app):
    app.config["SECRET_KEY"] = "mysecret"
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    moment = Moment(app)
    migrate = Migrate(app, db)


# ============================================================================#

class User(db.Model):
    __tablename__ = "User"

    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    username = db.Column(db.String(30), nullable=False, unique=True)
    password = db.Column(db.String(400),nullable=False)
    user_created_at = db.Column(db.Date(),default=datetime.datetime.now())
    user_updated_at = db.Column(db.Date(),default=datetime.datetime.now())


class Transaction(db.Model):
    __tablename__ = "Transaction"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id,onupdate="CASCADE", ondelete="CASCADE"))
    users = db.Column(db.String(1000), nullable=False)
    amount = db.Column(db.String(100), nullable=False)
    transaction_date = db.Column(db.Date(), nullable=False)
    transaction_added = db.Column(db.Date(), default=datetime.datetime.now())


class Account(db.Model):
    __tablename__ = "Account"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    transaction_id = db.Column(db.Integer, nullable=False)
    receiver_id = db.Column(db.Integer, nullable=False)
    lender_id = db.Column(db.Integer, nullable=False)
    amount = db.Column(db.Integer,default=0)
    transaction_date = db.Column(db.Date(), nullable=False)

def create_new():
    db.drop_all()
    db.create_all()
