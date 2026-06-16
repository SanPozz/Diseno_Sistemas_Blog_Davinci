from flask import Blueprint

from app.controllers.viewController import home_controller, landing_controller

views_bp = Blueprint("views", __name__)

@views_bp.route("/")
def index():
    return landing_controller()

@views_bp.route("/home")
def home():
    return home_controller()