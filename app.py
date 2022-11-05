from flask import Flask, session, render_template, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension

from forms import UserForm
from models import User

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///auth_demo"
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
        new_user = User.register(username, password)
        db.session.add(new_user)
        try:
            db.session.commit()
        except IntegrityError:
            form.username.errors.append("That username already exists")
            return render_template('register.html', form = form)
        session['user_id'] = new_user.id
        flash("Welcome", "success")
        return redirect('/secret')
    return render_template('register.html', form = form)

@app.route('/login', methods=['GET', 'POST'])
def login_user():
    """Login to site"""
    form = UserForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.authenticate(username, password)

        if user:
            flash(f"Welcome back, {username}")
            session["user_id"] = user.id
            return redirect('/secret')
        else:
            form.username.errors = ["Invalid username/password"]
    return render_template('login.html', form=form)

@app.route('/users/<username>')
def show_user(username):
    """Return text"""
    if 'user_id' in session:
        return render_template('user.html', username=username)
    else:
        return redirect('/login')

@app.route('/logout')
def logout():
    """Log out user"""
    session.clear()
    return redirect('/')