from flask_wtf import Form
from wtforms import StringField, SelectMultipleField, IntegerField, TextAreaField, PasswordField
from wtforms.validators import DataRequired, Email
from wtforms.fields.html5 import TelField

class AddForm(Form):
  name = StringField('name', validators=[DataRequired()])
  number = IntegerField('number', validators=[DataRequired()])

class RentForm(Form):
    renter_name = StringField('renter', validators=[DataRequired()])
    renter_email = StringField('email', validators=[DataRequired(), Email()])
    renter_phone_number = TelField('phone-number', validators=[DataRequired()])
    name = SelectMultipleField('name', validators=[DataRequired()])
    renter_idea = TextAreaField('idea')

class LoginForm(Form):  
    """Login form to access writing and settings pages"""

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
