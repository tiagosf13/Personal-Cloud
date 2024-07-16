from flask import Blueprint, redirect, url_for, request, render_template, jsonify
from models.UserModel import User
from handlers.AuthenticationHandler import check_password

# Create a Blueprint for especialidades view
signup_view = Blueprint('signup_view', __name__)


# Define the route for the especialidades view /
@signup_view.route('/')
def signup():
    return render_template('signup.html'), 200

# Define the route to create a new user
@signup_view.route('/create_user', methods=['POST'])
def create_user():
    
    # Get the user data from the request
    username = request.form['username']
    password = request.form['password']
    email = request.form['email']
    
    # Check if the email is already in use
    if User.check_email_in_use(email):
        return 'Email already in use', 400

    # Use a id created by the database

    # Create a new instance of the User class
    response = User(username, User.hash_password(password), email).create_user()
    
    # If the user was created successfully redirect to the login page, else return an error
    if response:
        return redirect(url_for("login_view.login")), 200
    else:
        return 'Error creating user', 400
    

@signup_view.route('/verify-password', methods=['POST'])
def verify_password():
    data = request.get_json()
    password = data.get('password')

    if not password:
        return jsonify({'error': 'Password not provided'}), 400

    # Check if the password has been breached
    count = check_password(password)
    
    if count > 0:
        return jsonify({'breached': True, 'count': count})
    else:
        return jsonify({'breached': False})