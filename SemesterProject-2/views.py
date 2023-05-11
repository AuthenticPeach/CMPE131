from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from flask_login import login_required, current_user

import json

views = Blueprint("views",__name__)

## URL Parameters

@views.route("/")
def home():
    return render_template("index.html", user=current_user)

@views.route("/add-content", methods=["GET", "POST"])
def add_content():
    if request.method == "POST":
        title = request.form['title']
        content = request.form['content']
        # Store the title and content in a database or file
        # Redirect to the admin dashboard after successful submission
        return redirect(url_for("app.admin_dashboard"))
    
    # Render the add_content.html template for GET requests
    return render_template("add_content.html", user=current_user)

@views.route('/analytics')
def analytics():
    # Retrieve the website statistics from your data source
    # Replace 'your_database_library' with the actual library and code to fetch statistics
    analytics_database = r"C:\Users\travi\Desktop\CMPE131Website\usersdb.sqlite3"
    statistics = analytics_database.fetch_website_statistics()

    # Pass the statistics data to the template for rendering
    return render_template('analytics.html', statistics=statistics)

@views.route("/contact")
def contact():
    return render_template("contact.html", user=current_user)


@views.route('/manage-users')
def manage_users():
    # Retrieve the list of users from the database or any other data source
    # Pass the list of users to the template for rendering

    users = [
        {'name': 'John Doe', 'email': 'john@example.com', 'avatar': '/static/icons/PugPlushieOtis.png'},
        {'name': 'Jane Smith', 'email': 'jane@example.com', 'avatar': '/static/icons/AZ_Maid.png'},

        # Add more users as needed
    ]

    return render_template('manage_users.html', users=users)

## Query Parameters

@views.route("/profile/")
def profile():
    return render_template("profile.html")

## Get Return JSON data

@views.route("/json")
def get_json():
    return jsonify({'name': 'tim', 'coolness': 10})

## Get JSON data

@views.route("/data", methods=["GET", "POST"])
def get_data():
    if request.method == "POST":
        data = request.form  # Access form data using request.form
        return jsonify(data)
    else:
        return "This is a GET request to /data"

## redirect

@views.route("/go-to-home")
def go_to_home():
    return redirect(url_for("views.home"))

## update settings

@views.route('/update-settings', methods=['GET', 'POST'])
def update_settings():
    if request.method == 'POST':
        # Handle the form submission
        # Retrieve the form data using request.form
        # Perform necessary actions (e.g., update settings in the database)
        return redirect(url_for('views.update_settings'))  # Redirect to the same page after POST
        
    # Render the update_settings.html template for GET requests
    return render_template('update_settings.html', user=current_user)
