from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_user
from models.UserModel import User

# Create a Blueprint for login view
login_view = Blueprint('login_view', __name__)

# Define the route for the login view '/'
@login_view.route('/', methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        # Check user credentials
        # If credentials are correct, log the user in
        user = User.get_user(value=request.form['email'], attr_type="email")
        if user and user.check_password(request.form['password']):
            login_user(user)
            print("User logged in")
            return redirect(url_for('home_view.home', id=user.id, username=user.username)), 200
        else:
            print("Invalid username or password")
            return render_template('login.html', error="Invalid username or password"), 401
    else:
        return render_template('login.html'), 200
