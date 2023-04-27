from flask import Flask, redirect, render_template, url_for, request
from flask_login import current_user
from flask_sqlalchemy import SQLAlchemy
from flask_user import UserManager, UserMixin
from views import views
from flask_mail import Mail, Message

app = Flask(__name__)
app.register_blueprint(views, url_prefix="/")

app.config['SECRET_KEY'] = 'your_secret_key'  # Change this to a secure secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your_database.db'  # Change the database URI

db = SQLAlchemy(app)

# User model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False, server_default='')

# Flask-User settings
app.config['USER_APP_NAME'] = "City Website"
app.config['USER_ENABLE_EMAIL'] = False  # Change to True if you want email-based registration
app.config['USER_ENABLE_USERNAME'] = True
app.config['USER_REQUIRE_RETYPE_PASSWORD'] = True

# Initialize Flask-User
user_manager = UserManager(app, db, User)

# Routes
@app.route('/')
def home():
    return 'Welcome to the home page!'



@app.route('/profile')
def profile():
    if not current_user.is_authenticated:
        return redirect(url_for('user.login'))

    return f'Welcome, {current_user.username}!'

if __name__ == '__main__':
    with app.app_context():  # Set up the application context
        db.create_all()  # Create the database tables
    app.run(debug=True, port=5000)
