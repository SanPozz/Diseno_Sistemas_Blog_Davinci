from flask import request, redirect, render_template
from flask_login import login_user
from flask_jwt_extended import create_access_token
from app.services.auth_service import AuthService
from werkzeug.security import generate_password_hash, check_password_hash

from app.models.Users import User
from app.database import db


def register_controller():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        existing_email = User.query.filter_by(email=email).first()
        if existing_email:
            return "El usuario ya existe"
        existing_user = User.query.filter_by(username=username).first()

        if existing_user:
            return "El usuario ya existe"
        hashed_password = generate_password_hash(password)

        new_user = User(username=username, email=email, hashed_password=hashed_password)

        db.session.add(new_user)

        db.session.commit()

        return redirect("/login")
    return render_template("register.html")


def login_controller():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = User.query.filter_by(username=username).first()

        if not user:
            return "Usuario no encontrado"

        valid_password = check_password_hash(user.hashed_password, password)

        if not valid_password:
            return "contraseña incorrecta"

        login_user(user)

        access_token = create_access_token(identity=user.id)

        if user.role == "admin":
            return redirect("/admin")
        return redirect("/landing")

    return render_template("login.html")
