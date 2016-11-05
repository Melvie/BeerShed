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

    def transfer(self,TO):
        if self.status=="Full" and TO.get_status()=="Clean":
            self.set_status("Dirty")
            TO.set_status("Full")
            return "Arduino will transfer from carboy {} to carboy {}".format(self.carboy,TO.get_id())
        else:
            return "Error: Cannot transfer from {} to {}. Carboy {} must not be dirty or full and Carboy {} must be full.".format(self.carboy, TO.get_id(), TO.get_id(), self.id)


    def bottle(self):
        if self.status == "Full":
            self.set_status("Dirty")
            return  "Arduino will bottle carboy {}".format(self.carboy)
        else:
            return "Error: Carboy {} is empty.".format(self.carboy)


    def clean(self):
        if self.status =="Dirty":
            self.set_status("Clean")
            return "Arduino will clean carboy {}".format(self.carboy)
        elif self.status == "Clean":
            return "Error: Carboy {} is already clean.".format(self.carboy)
        else:
            return "Error: Carboy {} is full.".format(self.carboy)

    def brew(self):
        if self.status== "Clean":
            self.set_status("Full")
            return "Arduino will brew into carboy {}".format(self.carboy)

        else:
            return "Error: Carboy {} must not already be full or dirty".format(self.carboy)

    def set_status(self,new_status):
        self.status = new_status

    def get_status(self):
        return self.status

    def get_temp(self):
        return self.temperature

    def get_id(self):
        return self.carboy

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
