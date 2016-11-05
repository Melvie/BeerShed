from flask_wtf import Form
from wtforms import SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class ButtonForm(Form):
    action = SubmitField(label = 'button')
