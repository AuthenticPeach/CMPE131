from flask import Flask, redirect, render_template, url_for, request, redirect
from flask_login import current_user, LoginManager, UserMixin, login_user, login_required, logout_user
from flask_sqlalchemy import SQLAlchemy
from flask_user import UserManager, UserMixin
from flask_mail import Mail, Message


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///my-login-app.db'
app.config['SECRET_KEY'] = 'my-secret-key'
db = SQLAlchemy(app)
login_manager = LoginManager(app)

# User model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

@app.route('/index')
def index():
    return render_template('index.html')
# Routes
@app.route('/')
def home():
#    return 'Welcome to the home page!'
    return render_template('index.html')

# Function to return a string when we add something
    # def __repr__(self):
    #     return '<Name %r>' % self.id

# Flask-User settings
app.config['USER_APP_NAME'] = "City Website"
app.config['USER_ENABLE_EMAIL'] = False  # Change to True if you want email-based registration
app.config['USER_ENABLE_USERNAME'] = True
app.config['USER_REQUIRE_RETYPE_PASSWORD'] = True

# Initialize Flask-User
user_manager = UserManager(app, db, User)

# Register blueprints
from views import views
app.register_blueprint(views)

from passlib.hash import pbkdf2_sha256

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and pbkdf2_sha256.verify(password, user.password):
            login_user(user)
            return redirect(url_for('index'))
    return render_template('login.html')

from passlib.hash import pbkdf2_sha256
app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = pbkdf2_sha256.hash(password)
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/users', methods=['POST', 'GET'])
def users():
    title = "The User List"

    if request.method == "POST":
        user_name = request.form['name']
        new_user = users(name=user_name)

        #push to database
        try:
            db.session.add(new_user)
            db.session.commit()
            return redirect('/friends')
        except:
            return "There was an error adding the new user in the db"
    else:
        return render_template("users.html", title=title)

@app.route('/profile')
def profile():
    if not current_user.is_authenticated:
        return redirect(url_for('user.login'))

    return f'Welcome, {current_user.username}!'

# Route for the administrative dashboard
@app.route('/admin/dashboard')
def admin_dashboard():
    # Fetch data for the dashboard (e.g., recent activity logs, important messages)
    recent_activity_logs = get_recent_activity_logs()
    important_messages = get_important_messages()

    # Render the dashboard template and pass the data to it
    return render_template('admin_dashboard.html', activity_logs=recent_activity_logs, messages=important_messages)

# Helper functions to fetch data for the dashboard
def get_recent_activity_logs():
    # Fetch and return the recent activity logs from the database or any other data source
    # You can customize this function based on your specific requirements
    activity_logs = [
        'User "John" updated the homepage',
        'New user "Alice" registered',
        'Article "Tips for Effective Content Management" published'
    ]
    return activity_logs

def get_important_messages():
    # Fetch and return the important messages from the database or any other data source
    # You can customize this function based on your specific requirements
    messages = [
        'Site maintenance scheduled on May 15th, 9 PM - 11 PM',
        'Reminder: Submit monthly reports by the end of the week',
        'New content contributor guidelines updated'
    ]
    return messages


if __name__ == '__main__':
    with app.app_context():  # Set up the application context
        db.create_all()  # Create the database tables
    app.run(debug=True, port=5000)
