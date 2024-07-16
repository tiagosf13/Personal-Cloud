from flask import Flask, render_template
from handlers.DatabaseHandler import check_database_tables_exist
from handlers.AuthenticationHandler import login_manager
from views.index_view import index_view
from views.login_view import login_view
from views.signup_view import signup_view
from views.home_view import home_view
from views.profile_view import profile_view
from views.logout_view import logout_view
from views.recover_password import recover_password_view
from views.files_view import files_view

# Create the application instance
personal_cloud_system = Flask(__name__)
personal_cloud_system.config['SECRET_KEY'] = 'PERSONAL-CLOUD'
personal_cloud_system.config['TEMPLATES_AUTO_RELOAD'] = True
personal_cloud_system.config['TEMPLATES_AUTO_RELOAD'] = 'utf-8'

# Register the blueprints
personal_cloud_system.register_blueprint(index_view)
personal_cloud_system.register_blueprint(login_view, url_prefix='/login')
personal_cloud_system.register_blueprint(signup_view, url_prefix='/signup')
personal_cloud_system.register_blueprint(home_view, url_prefix='/home')
personal_cloud_system.register_blueprint(profile_view, url_prefix='/profile')
personal_cloud_system.register_blueprint(logout_view, url_prefix='/logout')
personal_cloud_system.register_blueprint(recover_password_view, url_prefix='/recover-password')
personal_cloud_system.register_blueprint(files_view, url_prefix='/files')

check_database_tables_exist()

# Declare error handlers here
@personal_cloud_system.errorhandler(403)
def forbidden(error):
    # Return a redirect to the 403 error page
    return render_template("403.html"), 403

@personal_cloud_system.errorhandler(500)
def server_error(error):
    return render_template("500.html"), 500

@personal_cloud_system.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404

@personal_cloud_system.errorhandler(405)
def method_not_allowed(error):
    return render_template("405.html"), 4057


if __name__ == '__main__':
    # Run the login manager
    login_manager.init_app(personal_cloud_system)

    # Run the application
    personal_cloud_system.run(debug=True, host='127.0.0.1', port=5000)