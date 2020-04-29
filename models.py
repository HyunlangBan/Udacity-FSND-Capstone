import os
from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
import json


database_path = os.environ.get('DATABASE_URL')


db = SQLAlchemy()


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


class Reservation(db.Model):
    __tablename__ = 'rsvn'
    id = db.Column(db.Integer, primary_key=True)
    rest_id = db.Column(db.Integer, db.ForeignKey('rest.id'), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey(
        'customer.id'), nullable=False)
    number = db.Column(db.Integer, nullable=False)
    time = db.Column(db.DateTime, nullable=False)
    request = db.Column(db.String)
    review = db.Column(db.String)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return f'<Venue {self.start_time}>'

    def format(self):
        return {
            'id': self.id,
            'rest_id': self.rest_id,
            'customer_id': self.customer_id,
            'number': self.number,
            'time': self.time,
            'request': self.request,
            'review': self.review
        }


class Restaurant(db.Model):
    __tablename__ = 'rest'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    address = db.Column(db.String(120), nullable=False)
    category = db.Column(db.String(), nullable=False)
    photo = db.Column(db.String)
    tel = db.Column(db.String(120), nullable=False)
    menu = db.Column(db.String, nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    open_time = db.Column(db.Time, nullable=False)
    close_time = db.Column(db.Time, nullable=False)

    rest_rsvn = db.relationship('Reservation', backref='rest')

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return f'<Restaurant {self.id} {self.name}>'

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'photo': self.photo,
            'address': self.address,
            'tel': self.tel,
            'category': self.category
        }


class Customer(db.Model):
    __tablename__ = 'customer'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String, nullable=False)

    customer_rsvn = db.relationship('Reservation', backref='customer')

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return f'<Customer {self.id} {self.name}>'

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'phone': self.phone,
            'email': self.email
        }
