from flask import request, redirect, render_template
from flask_login import login_user, logout_user, login_required, current_user

# from flask_jwt_extended import create_access_token
from app.services.auth_service import AuthService
from werkzeug.security import generate_password_hash, check_password_hash

from app.models.Users import User
from app.database import db


def register_controller():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        RESULT_REGISTER = AuthService.register(username, email, password)

        error_message = RESULT_REGISTER[1]
        user = RESULT_REGISTER[0]

        if error_message:
            return redirect(f"/auth/register?error=true&message={error_message}")

        if user:
            return redirect("/auth/login?registered=true&error=false")
    return render_template("register.html")


def login_controller():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        RESULT_LOGIN = AuthService.login(username, password)

        error_message = RESULT_LOGIN[1]
        user = RESULT_LOGIN[0]

        if error_message:
            return redirect(f"/auth/login?error=true&message={error_message}")

        if user:
            login_user(user)

        # access_token = create_access_token(identity=user.id)

        # TODO: Implementar JSON WEB TOKEN con cookies y utilizar @jwt_required en rutas protegidas

        return redirect("/home")

    return render_template("login.html")


@login_required
def profile_controller():

    if not current_user.is_authenticated:

        return redirect("/auth/login")

    posts = current_user.posts

    posts_count = len(posts)

    total_likes = sum(p.likes for p in posts)

    return render_template(
        "profile.html",
        user=current_user,
        posts=posts,
        posts_count=posts_count,
        total_likes=total_likes,
    )
