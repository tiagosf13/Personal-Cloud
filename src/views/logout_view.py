from flask import Blueprint, render_template
from flask_login import login_required, logout_user



# Create a Blueprint for agendar view
logout_view = Blueprint('logout_view', __name__)


# Define the route for the agendar view /vacinas
@logout_view.route('/', methods=['GET'])
@login_required
def logout():
    # Log the user out
    logout_user()
    return render_template('index.html'), 200