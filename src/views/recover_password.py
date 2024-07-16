from flask import Blueprint, render_template, request, redirect, url_for
from handlers.SecurityHandler import is_valid_input
from models.UserModel import User
from handlers.AuthenticationHandler import generate_reset_token

# Create a Blueprint for login view
recover_password_view = Blueprint('recover_password_view', __name__)

# This route is used to let the user reset their password
@recover_password_view.route("/", methods=["GET", "POST"])
def reset_password():
    if request.method == "POST":
        email = request.form.get("email")
        if is_valid_input([email]) == False:
            return render_template("reset-password.html", message="Invalid email.")

        user = User.get_user("email", email)
        
        if user is None:
            # If the user doesn't exist, return the signup page
            return redirect(url_for("views.signup"))
        else:
            # Generate a unique reset token
            reset_token = generate_reset_token()
            # Store the reset token in the user's record in the database
            User.set_reset_token(user.username, reset_token)
            # Send a password reset email with the token
            User.send_password_reset_email(email, reset_token)
            return redirect(url_for("views.login"))
    else:
        return render_template("recover-password.html")