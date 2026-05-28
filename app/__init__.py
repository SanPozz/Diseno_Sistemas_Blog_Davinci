from flask import Flask, redirect

from config import DevConfig
from app.database import init_db
from app.extensions import login_manager, oauth
from app.routes.authRoutes import auth_bp
from app.routes.postRoutes import post_bp


def create_app():

    app = Flask(__name__)

    app.config.from_object(DevConfig)

    login_manager.init_app(app)
    oauth.init_app(app)

    init_db(app)

    app.register_blueprint(post_bp)
    app.register_blueprint(auth_bp)

    @app.route("/")
    def index():

        return redirect("/login")

    return app
