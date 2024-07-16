import hashlib, requests, secrets, string
from models.UserModel import User
from flask_login import LoginManager

login_manager = LoginManager()

@login_manager.user_loader
def load_user(id):
    return User.get_user("id", id)

@login_manager.unauthorized_handler
def unauthorized():
    return "You must be logged in to access this page", 403

@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    user = User.get_user("username", username)
    return user if user else None

def check_password(password):
    # Hash the password using SHA-1
    hashed_password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    prefix, suffix = hashed_password[:5], hashed_password[5:]

    # Make a GET request to the HIBP API
    response = requests.get(f'https://api.pwnedpasswords.com/range/{prefix}')

    # Check if the suffix of the hashed password exists in the response
    hashes = (line.split(':') for line in response.text.splitlines())
    for h, count in hashes:
        if h == suffix:
            return int(count)
    return 0

# Generate a unique reset token
def generate_reset_token(code_length=32):
    return ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(code_length))