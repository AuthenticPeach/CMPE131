from flask import Blueprint, render_template, request, jsonify, redirect, url_for

views = Blueprint(__name__, "views")

## URL Parameters

@views.route("/")
def home():
    return render_template("index.html", name="Tim", age="25")

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

