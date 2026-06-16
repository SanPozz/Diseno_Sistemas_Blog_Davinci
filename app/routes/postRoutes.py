from flask import Blueprint


from app.controllers.postController import (
    landing_controller,
    create_post_controller,
    post_detail_controller,
    add_like_controller,
    add_comment_controller,
    notifications_controller,
)

post_bp = Blueprint("post", __name__)


@post_bp.route("/landing")
def landing():
    return landing_controller()


@post_bp.route("/posts/create", methods=["GET", "POST"])
def create_post():
    return create_post_controller()


@post_bp.route("/posts/<int:post_id>")
def post_detail(post_id):
    return post_detail_controller(post_id)


@post_bp.route("/posts/<int:post_id>/like", methods=["POST"])
def add_like(post_id):
    return add_like_controller(post_id)


@post_bp.route("/posts/<int:post_id>/comment", methods=["POST"])
def add_comment(post_id):
    return add_comment_controller(post_id)


@post_bp.route("/notifications")
def notifications():
    return notifications_controller()
