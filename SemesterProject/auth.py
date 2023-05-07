from flask import Blueprint, render_template, request, flash, redirect, url_for
from CMPE131Website.models import User
from werkzeug.security import generate_password_hash, check_password_hash
from CMPE131Website.app import db   ##means from __init__.py import db
from flask_login import login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

       # Authenticate user
    user = User.query.filter_by(username=username).first()
    if user and user.password == password:
        # Successful login
        # Create a new LoginHistory record
        login_history = LoginHistory(
            user_id=user.id,
            user_type=user.user_type,
            ip_address=request.remote_addr,
            login_status='Success'
        )
        db.session.add(login_history)
        db.session.commit()
        # Redirect to the desired page
        return redirect(url_for('views.home'))
    else:
        # Failed login
        # Create a new LoginHistory record
        login_history = LoginHistory(
            user_id=user.id if user else None,
            user_type=user.user_type if user else None,
            ip_address=request.remote_addr,
            login_status='Failure'
        )
        db.session.add(login_history)
        db.session.commit()
        # Show an error message to the user
        return render_template('login.html', error='Invalid username or password')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(
                password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)
