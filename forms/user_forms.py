from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, URLField, TextAreaField
from wtforms.validators import InputRequired, Optional, AnyOf, URL, NumberRange

class RegisterUser(FlaskForm):
    """
    Model for form object with all fields for adding new users to database
    """
    username = StringField('Username', validators=[InputRequired(message='Username cannot be blank')])
    email = URLField('Email', validators=[InputRequired(message='Email cannot be blank')])
    password = PasswordField('Password', validators=[InputRequired(message='Password cannot be blank')])

class LoginUser(FlaskForm):
    """
    Model for form object with all fields for adding new users to database
    """
    username = StringField('Username', validators=[InputRequired(message='Username cannot be blank')])
    password = PasswordField('Password', validators=[InputRequired(message='Password cannot be blank')])

class EditUser(FlaskForm):
    """
    Model for form object with all fields for updating users in database
    """

    new_username = StringField('Username', validators=[InputRequired(message='Username cannot be blank')])
    new_email = URLField('Email', validators=[InputRequired(message='Email cannot be blank')])
    current_password = PasswordField('Current Password', validators=[InputRequired(message='Current password must be entered for authentication')])
    new_password = PasswordField('New Password', validators=[InputRequired(message='Password cannot be blank')])