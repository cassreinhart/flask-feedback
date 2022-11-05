from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField #password field shows dots when you start typing
from wtforms.validators import InputRequired, EqualTo, Email

class UserForm(FlaskForm):
    username= StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired(), EqualTo('confirm', message="Passwords must match")])
    confirm = PasswordField("Repeat Password")
    email = EmailField("Email", validators=[InputRequired(), Email()])
    first_name = StringField("First Name", validators=[InputRequired()])
    last_name = StringField("Last Name", validators=[InputRequired()])