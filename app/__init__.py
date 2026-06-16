from flask import Flask, redirect
import os

from config import DevConfig
from app.database import init_db
from app.extensions import login_manager, oauth
from app.routes.authRoutes import auth_bp
from app.routes.postRoutes import post_bp
from app.routes.viewsRoutes import views_bp


def create_app():

    app = Flask(
        __name__,
        static_folder=os.path.join(os.path.dirname(__file__), 'static'),
        static_url_path='/static'
    )

    app.config.from_object(DevConfig)

    login_manager.init_app(app)
    oauth.init_app(app)

    init_db(app)

    app.register_blueprint(views_bp)
    app.register_blueprint(post_bp, url_prefix='/posts')
    app.register_blueprint(auth_bp, url_prefix='/auth')

    return app
