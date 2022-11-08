from flask import Flask, session, render_template, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from werkzeug.exceptions import Unauthorized

from forms import RegisterForm, LoginForm
from models import db, connect_db, User
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///feedback"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "abc123"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False


connect_db(app)

toolbar = DebugToolbarExtension(app)

@app.route('/')
def show_registration_page():
    """Redirects to registration page"""
    return redirect('/register')

@app.route('/register', methods=['GET', 'POST'])
def register_form():
    """Process registration form or show registration form"""
    form = RegisterForm()
    
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        user = User.register(username, password, email, first_name, last_name)
        db.session.add(new_user)
        try:
            db.session.commit()
        except IntegrityError as err:
            print(err)
            print('*************')
            form.username.errors.append("That username already exists")
            return render_template('register.html', form = form)
        session['username'] = user.username
        flash("Welcome", "success")
        return redirect(f'/users/{user.username}')
    return render_template('register.html', form = form)

@app.route('/login', methods=['GET', 'POST'])
def login_user():
    """Login to site"""
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.authenticate(username, password)

        if user:
            flash(f"Welcome back, {username}")
            session["username"] = user.username
            return redirect(f'/users/{user.username}')
        else:
            form.username.errors = ["Invalid username/password"]
    return render_template('/user/login.html', form=form)

@app.route('/logout')
def logout():
    """Log out user"""
    
    session.pop("username") # vs session.clear()?
    return redirect('/')

@app.route('/users/<username>')
def show_user(username):
    """Show info about the given user. Show all feedback given by that user."""
    if 'username' not in session or 'username' != session['username']:
        raise Unauthorized()
    
    user = User.query.get(username)
    return render_template('/user/user.html', user=user)

@app.route('/users/<username>/delete', methods=['POST'])
def delete_user(username):
    """Remove the user from the database, cascade to feedback.
    Clear username from session, then redirect"""
    
    if 'username' not in session or 'username' != session['username']:
        raise Unauthorized()

    user = User.query.get(username)
    db.session.delete(user)
    db.session.commit()
    session.pop("username")

    return redirect("/login")

@app.route('/users/<username>/feedback/add', methods=['GET', 'POST'])
def add_feedback(username):
    """Display add feedback form, check that only current user can see this.
    Process feedback form."""

    if 'username' not in session or 'username' != session['username']:
        raise Unauthorized()
    
    form = FeedbackForm()

    if form.validate_on_submit():
        title = form.data.title
        content = form.data.content
        feedback = Feedback(title=title, content=content, username=username)

        db.session.add(feedback)
        db.session.commit()

        return redirect(f'/users/{username}')

    return render_template('/feedback/add.html', form=form)

@app.route('/users/<username>/feedback/update', methods=['GET', 'POST'])
def edit_feedback(username):
    """Display edit feedback form, process form and redirect to /users/username"""

@app.route('/users/<username>/feedback/delete', methods=['GET', 'POST'])
def delete_feedback(username):
    """Delete feedback and redirect to /users/username""""
