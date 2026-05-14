from flask import Blueprint, request, redirect, render_template
from flask_login import login_required, current_user, logout_user

from app.controllers.authController import(
    login_controller,
    register_controller
)

auth_bp = Blueprint("auth", __name__);

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
  return login_controller()

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    return register_controller()

@auth_bp.route("/landing")
@login_required
def landing():
   if current_user.role != "user":
      return "Acceso denegado"
   return render_template("landing.html")

@auth_bp.route("/admin")
@login_required
def admin():
   if current_user.role != "admin":
      return "Acceso denegado"
   return render_template("admin.html")

@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/login")
   