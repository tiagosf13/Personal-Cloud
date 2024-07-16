from flask import Blueprint, request, render_template, redirect, url_for
from flask_login import login_required
from handlers.MediaHandler import save_image
from handlers.SecurityHandler import is_valid_input
from models.UserModel import User



# Create a Blueprint for profile view
profile_view = Blueprint('profile_view', __name__)


# Define the route for the profile view
@profile_view.route('/<user_id>', methods=["GET"])
@login_required
def profile(user_id):
    # Verify if the user_id is valid
    if not is_valid_input([user_id]):
        return render_template("404.html"), 404
    else:
        return render_template('profile.html', user_id=user_id), 200

# Define the route to update the profile photo
@profile_view.route('/update_photo/<id>', methods=['POST'])
@login_required
def update_photo(id):
    # Verify if the user_id is valid
    if not is_valid_input([id]):
        return render_template("404.html"), 404
    else:
        # Save the photo to the Database
        if save_image(id, request.files['photo'].read()):
            user = User.get_user(attr_type=" id", value=id)
            return redirect(url_for("home_view.home", id=id, username=user.username))
        else:
            return 'Error updating photo'