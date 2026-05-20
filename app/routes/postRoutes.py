from flask import Blueprint

from app.controllers.postController import (
    landing_controller,
    create_post_controller,
    post_detail_controller,
)

post_bp = Blueprint("post", __name__)


@post_bp.route("/landing")
def landing():
    return landing_controller()


@post_bp.route("/post/create", methods=["GET", "POST"])
def create_post():
    return create_post_controller()


@post_bp.route("/post/<int:post_id>")
def post_detail(post_id):
    return post_detail_controller(post_id)
