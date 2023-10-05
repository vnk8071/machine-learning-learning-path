# ---------------------------------------------------------------------------- #
# Imports
# ---------------------------------------------------------------------------- #

from flask import Flask
from flask_migrate import Migrate
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy

from logger import Logger

# ---------------------------------------------------------------------------- #
# App Config.
# ---------------------------------------------------------------------------- #

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
with app.app_context():
    db = SQLAlchemy(app)
logger = Logger.get_logger(__name__)
migrate = Migrate(app, db)

# ---------------------------------------------------------------------------- #
# Models.
# ---------------------------------------------------------------------------- #


class Venue(db.Model):
    __tablename__ = 'venues'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(200))
    state = db.Column(db.String(200))
    address = db.Column(db.String(200))
    phone = db.Column(db.String(200))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(200))
    seeking_talent = db.Column(db.Boolean, nullable=False, default=False)
    seeking_description = db.Column(db.String, nullable=True)
    website_link = db.Column(db.String(), nullable=True)
    genres = db.Column(db.  String(200))
    shows = db.relationship("Show", backref="venue", lazy=True)

    def __str__(self):
        return f'Venue has {self.id} and named {self.name}'

    def __repr__(self):
        return f'<Venue {self.id} {self.name}>'


class Artist(db.Model):
    __tablename__ = 'artists'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(200))
    state = db.Column(db.String(200))
    phone = db.Column(db.String(200))
    genres = db.Column(db.String(200))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(200))
    website_link = db.Column(db.String(), nullable=True)
    seeking_venue = db.Column(db.Boolean, nullable=False, default=False)
    seeking_description = db.Column(db.String, nullable=True)
    shows = db.relationship("Show", backref="artist", lazy=True)

    def __str__(self):
        return f'Artist has {self.id} and named {self.name}'

    def __repr__(self):
        return f'<Artist {self.id} {self.name}>'


class Show(db.Model):
    __tablename__ = 'shows'

    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime, nullable=False)
    artist_id = db.Column(
        db.Integer,
        db.ForeignKey("artists.id"),
        nullable=False
    )
    venue_id = db.Column(
        db.Integer,
        db.ForeignKey("venues.id"),
        nullable=False
    )
