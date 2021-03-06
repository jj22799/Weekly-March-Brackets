from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy import PickleType


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Picks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    winners = db.Column(MutableList.as_mutable(PickleType), default=[]) # List of all winners picked
    link_id = db.Column(db.Integer, db.ForeignKey('link.id'))
    
class Matchup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    game = db.Column(db.Integer) # 1 - 63 as shown on image in enter_teams.html
    team1 = db.Column(db.String(100)) # Name of Team 1
    team2 = db.Column(db.String(100)) # Name of Team 2
    winner = db.Column(db.String(100)) # Name of winning team

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    is_admin = db.Column(db.Boolean, default=False)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Note')

class Pool(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pool_name = db.Column(db.String(100))
    password = db.Column(db.String(12))

class Link(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    pool_id = db.Column(db.Integer, db.ForeignKey('pool.id'))
    picks = db.relationship('Picks')
    
class Lock(db.Model):
    # Used to track when a round of picks is locked so users
    # can't edit their picks.  This should have one Lock for each week
    # (3 per year) which will be manually toggled to is_locked=True
    # at tip off of the first game of each week.
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    week = db.Column(db.Integer) # 1: Round of 64 and 32; 2: Sweet 16 and Elite 8; 3: Final 4 and Championship
    is_locked = db.Column(db.Boolean, default=False)

