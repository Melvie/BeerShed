from project import db,bcrypt #pragma: no cover
from sqlalchemy import ForeignKey #pragma: no cover 
from sqlalchemy.orm import relationship #pragma: no cover


class CarboyStates(db.Model):

    __tablename__="info"
    
    id = db.Column(db.Integer, primary_key=True)
    carboy = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String, nullable=False)
    temperature = db.Column(db.Integer, nullable=False)

    def __init__(self, carboy, status, temperature):
        self.carboy = carboy
        self.status  = status
        self.temperature = temperature

    def __repr__(self):
        return '<status {}'.format(self.status)


class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    role = db.Column(db.String, nullable=True)

    def __init__(self, name, email, password, role):
        self.name = name
        self.email = email
        self.password = bcrypt.generate_password_hash(password)
        self.role = role

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return '<name - {}>'.format(self.name)
