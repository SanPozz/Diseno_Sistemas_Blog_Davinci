import os
from flask import Blueprint, request, redirect, render_template
from flask_login import login_required, current_user, logout_user
from flask import url_for
from authlib.integrations.flask_client import OAuth
from app.extensions import oauth
from app.controllers.authController import login_controller, register_controller
from flask_login import login_user
from app.models.Users import User
from app.database import db

auth_bp = Blueprint("auth", __name__)

google = oauth.register(
    name="google",
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    return login_controller()


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    return register_controller()


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/login")


# google
@auth_bp.route("/google/login")
def google_login():

    redirect_uri = url_for("auth.google_callback", _external=True)

    return google.authorize_redirect(redirect_uri)


@auth_bp.route("/google/callback")
def google_callback():

    token = google.authorize_access_token()

    user_info = token.get("userinfo")

    email = user_info["email"]
    username = user_info["name"]

    user = User.query.filter_by(email=email).first()

    if not user:

        user = User(
            username=username, email=email, hashed_password="google_login", role="user"
        )

        db.session.add(user)
        db.session.commit()

    login_user(user)

    if user.role == "admin":
        return redirect("/admin")

    return redirect("/landing")
