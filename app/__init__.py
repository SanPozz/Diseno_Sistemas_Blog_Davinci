from flask import Flask, redirect

from config import DevConfig;
from app.database import init_db;
from app.extensions import login_manager

from app.routes.posts import posts_bp

def create_app():

    app = Flask(__name__);

    app.config.from_object(DevConfig);

    login_manager.init_app(app)

    init_db(app);

    app.register_blueprint(posts_bp, url_prefix="/posts");

    @app.route("/")
    def index():
        return redirect("/posts");

    return app;