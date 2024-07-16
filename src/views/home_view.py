from flask import Blueprint, render_template, jsonify
from flask_login import login_required
from handlers.SecurityHandler import is_valid_input
from handlers.StorageHandler import get_storage_info, get_file_system_structure
from models.UserModel import User


# Create a Blueprint for home view
home_view = Blueprint('home_view', __name__)


# Define the route for the home view
@home_view.route('/<id>', methods=["GET"])
@login_required
def home(id):
    # Verify if the user_id is valid
    if not is_valid_input([id]):
        return render_template("404.html"), 404
    else:
        user = User.get_user("id", id)
        return render_template('home.html', id=user.id, username=user.username), 200