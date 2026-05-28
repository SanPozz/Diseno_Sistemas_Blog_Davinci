from flask_login import LoginManager
from authlib.integrations.flask_client import OAuth
from flask_jwt_extended import JWTManager

oauth = OAuth()

login_manager = LoginManager()

jwt = JWTManager()
