from datetime import datetime
from flask_login import UserMixin
from handlers.DatabaseHandler import db_query, get_current_dir
from handlers.EmailHandler import send_email
from extensions.AppExtensions import bcrypt
from flask import render_template_string


class User(UserMixin):
    def __init__(self, username, hashed_password, email, admin_role=False, user_id=None):
        self.id = user_id
        self.username = username
        self.hashed_password = hashed_password
        self.email = email
        self.admin_role = admin_role
       
    def check_password(self, password):
        return bcrypt.check_password_hash(self.hashed_password, password)
    
    def create_user(self):
        # Create a new user in the database
        query = "INSERT INTO users (username, hashed_password, email, admin) VALUES (%s, %s, %s, %s);"
        try:
            db_query(query, (self.username, self.hashed_password, self.email, self.admin_role))
            return True
        except:
            return False
     
    # Define the __str__ method for the User class
    def __str__(self):
        return f"User(id='{self.id}', username='{self.username}', password='{self.hashed_password}', email='{self.email}', role='{self.admin_role}')" 
    
    @classmethod
    def get_user(self, attr_type, value):
        # Check if attr_type is a valid attribute
        assert attr_type in ["id", "username", "email"], "Invalid attribute type"
        # Get user from database and left outer join with patients table
        query = f"SELECT id, username, hashed_password, email, admin \
                  FROM users \
                  WHERE users.{attr_type} = %s;"
        result = db_query(query, (value,))
        if result:
            return User(user_id=result[0][0], username=result[0][1], hashed_password=result[0][2], email=result[0][3], admin_role=result[0][4])
        else:
            return None
    
    @classmethod
    def check_email_in_use(self, email):
        query = "SELECT email FROM users WHERE email = %s;"
        result = db_query(query, (email,))
        return True if result else False
    
    @classmethod
    def hash_password(self, password):
        # Hash the password
        return bcrypt.generate_password_hash(password).decode("utf-8")
    
    @classmethod
    # Store the reset token in the user's record in the database
    def set_reset_token(user, reset_token):
        # Store the reset_token in the user's record in the database
        # This may involve creating a new column in the user table to store the token.

        # Build the query to update the reset_token in the user's table

        # Secure Query
        query = """
            UPDATE users SET password_reset_token = ? WHERE username = ?;
            UPDATE users SET password_reset_token_timestamp = ? WHERE username = ?
        """
        db_query(query, (reset_token, user, datetime.now(), user))
        
    @classmethod
    # Send a password reset email with the token
    def send_password_reset_email(email, reset_token):
        # Use your email library to send a password reset email with a link containing the reset token.
        # The link should point to a password reset route in your application where users can reset their passwords.
        # Make sure the token is securely validated in the reset route.

        with open(get_current_dir() + '/templates/email_password_reset.html', 'r', encoding='utf8') as html_file:
            email_template = html_file.read()

        # Render the email template with the context (including the reset_token)
        body = render_template_string(email_template, reset_token=reset_token)
    
        # Send the recovery email to the user
        return send_email(email, "Reset your password", body)