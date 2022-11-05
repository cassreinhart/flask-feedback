from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()

bcrypt = Bcrypt()

class User(db.Model):
    """User."""

    __tablename__ = 'users'

    username = db.Column(db.Text(20), primary_key = True, unique = True)
    password = db.Column(db.Text, nullable = False)
    email = db.Column(db.Text(50), nullable = False)
    first_name = db.Column(db.Text, nullable = False)
    last_name = db.Column(db.Text, nullable = False)

    @classmethod
    def register(cls, username, pwd):
        """Register user with hashed password, return user"""
        hashed = username.bcrypt.generate_password_hash(pwd)
        hashed_utf8 = hashed.decode('utf8')
        return cls(username=username, password=hashed_utf8)

    @classmethod
    def authenticate(cls, username, pwd):
        """Verify that the user is who they say they are by 
        checking input against hashed password, then return user"""
        u = User.query.filter_by(username=username).first()

        if u and bcrypt.check_password_hash(u.password, pwd):
            return u
        else:
            return False
