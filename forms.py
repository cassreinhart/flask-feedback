from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField
from wtforms.validators import InputRequired, EqualTo, Email, Length


class RegisterForm(FlaskForm):
    """Form for registering a user."""

    username= StringField("Username", validators=[InputRequired(), Length(min = 6, max = 20)])
    password = PasswordField("Password", validators=[InputRequired(), EqualTo('confirm', message="Passwords must match")])
    confirm = PasswordField("Repeat Password")
    email = EmailField("Email", validators=[InputRequired(), Email()])
    first_name = StringField("First Name", validators=[InputRequired()])
    last_name = StringField("Last Name", validators=[InputRequired()])


class LoginForm(FlaskForm):
    """Form for logging in a user."""

    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])