from flask import Flask, redirect
import os
from config import DevConfig
from app.database import init_db
from app.extensions import login_manager, oauth
from flask_login import current_user
from app.models.Notifications import Notification
from app.routes.authRoutes import auth_bp
from app.routes.postRoutes import post_bp
from app.routes.viewsRoutes import views_bp
from app.routes.notificationRoutes import notification_bp


def create_app():

    app = Flask(
        __name__,
        static_folder=os.path.join(os.path.dirname(__file__), "static"),
        static_url_path="/static",
    )

    app.config.from_object(DevConfig)

    login_manager.init_app(app)
    oauth.init_app(app)

    init_db(app)

    app.register_blueprint(views_bp)
    app.register_blueprint(post_bp, url_prefix="/posts")
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(notification_bp, url_prefix="/notifications")

    @app.context_processor
    def inject_notifications():

        notifications = []

        if current_user.is_authenticated:
            notifications = (
                Notification.query.filter_by(user_id=current_user.id)
                .order_by(Notification.created_at.desc())
                .limit(20)
                .all()
            )

        return dict(notifications=notifications)

    return app
