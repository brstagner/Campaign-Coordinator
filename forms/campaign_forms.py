from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, URLField, TextAreaField, IntegerField, SelectField, RadioField, SelectMultipleField, widgets, BooleanField
from wtforms.validators import InputRequired, Optional, AnyOf, URL, NumberRange, EqualTo

class CreateCampaign(FlaskForm):
    name = StringField('Name (required)', validators=[InputRequired(message='Name cannot be blank')])
    password = StringField('Password (required)', validators=[InputRequired(message='Password cannot be blank'), EqualTo('repassword', message='Passwords must match')])
    repassword = StringField('Reenter Password')
    description = TextAreaField('Description')

class EditCampaign(FlaskForm):
    name = StringField('Name (required)', validators=[InputRequired(message='Name cannot be blank')])
    description = TextAreaField('Description')
    