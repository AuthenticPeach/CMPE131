from flask import Flask, redirect, render_template, url_for, request, redirect
from flask_login import current_user
from flask_sqlalchemy import SQLAlchemy
from flask_user import UserManager, UserMixin
from flask_mail import Mail, Message

app = Flask(__name__)

app.config['SECRET_KEY'] = 'K62z!KXYmi4ZxN'  # Change this to a secure secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # Change the database URI

db = SQLAlchemy(app)

# User model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False, server_default='')
# Function to return a string when we add something
    def __repr__(self):
        return '<Name %r>' % self.id

# Flask-User settings
app.config['USER_APP_NAME'] = "City Website"
app.config['USER_ENABLE_EMAIL'] = False  # Change to True if you want email-based registration
app.config['USER_ENABLE_USERNAME'] = True
app.config['USER_REQUIRE_RETYPE_PASSWORD'] = True

# Initialize Flask-User
user_manager = UserManager(app, db, User)

# Email configuration
app.config['MAIL_SERVER'] = 'your_mail_server'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your_email_username'
app.config['MAIL_PASSWORD'] = 'your_email_password'

mail = Mail(app)

# Register blueprints
from views import views
from auth import auth
app.register_blueprint(views)
app.register_blueprint(auth, url_prefix="/auth")


# Routes
@app.route('/')
def home():
    return 'Welcome to the home page!'

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
        return redirect(url_for('auth.login'))

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

@app.route('/send_email', methods=['GET', 'POST'])
def send_email():
    if request.method == 'POST':
        recipient = request.form['recipient']
        subject = request.form['subject']
        body = request.form['body']

        # Send email
        try:
            msg = Message(subject, sender='travispeachohyeah@gmail.com', recipients=[recipient])
            msg.body = body
            mail.send(msg)
            return 'Email sent successfully!'
        except Exception as e:
            return f'Error sending email: {str(e)}'

    return render_template('send_email.html')    

if __name__ == '__main__':
    with app.app_context():  # Set up the application context
        db.create_all()  # Create the database tables
    app.run(debug=True, port=5000)
