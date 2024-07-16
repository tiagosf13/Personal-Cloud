from flask import Blueprint, render_template


# Create a Blueprint for home view
index_view = Blueprint('index_view', __name__)


@index_view.route('/')
def index():
	return render_template('index.html'), 200