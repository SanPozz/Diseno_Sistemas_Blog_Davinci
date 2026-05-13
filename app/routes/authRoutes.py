from flask import Blueprint, request, redirect, render_template

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