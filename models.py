from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()

bcrypt = Bcrypt()

def connect_db(app):
    """Connect to the database."""

    db.app = app
    db.init_app(app)

class User(db.Model):
    """User."""

    __tablename__ = 'users'

    username = db.Column(db.Text, primary_key = True, unique = True)
    password = db.Column(db.Text, nullable = False)
    email = db.Column(db.Text, nullable = False)
    first_name = db.Column(db.Text, nullable = False)
    last_name = db.Column(db.Text, nullable = False)

    @classmethod
    def register(cls, username, pwd, email, first_name, last_name):
        """Register user with hashed password, return user"""

        hashed = bcrypt.generate_password_hash(pwd)
        hashed_utf8 = hashed.decode('utf8')
        user = cls(
            username=username, 
            password=hashed_utf8,
            email=email,
            first_name=first_name,
            last_name=last_name,
        )

        return user

    @classmethod
    def authenticate(cls, username, pwd):
        """Verify that the user is who they say they are by 
        checking input against hashed password, then return user"""

        u = User.query.filter_by(username=username).first()

        if u and bcrypt.check_password_hash(u.password, pwd):
            return u
        else:
            return False


class Feedback(db.Model):
    """Feedback."""

    __tablename__ = 'feedback'

    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    title = db.Column(db.String(100), nullable = False)
    content = db.Column(db.Text, nullable = False)
    username = db.Column(db.Text, db.ForeignKey('users.username'))