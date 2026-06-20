from flask import Blueprint


from app.controllers.postController import (
    create_post_controller,
    post_detail_controller,
    add_like_controller,
    add_comment_controller,
    add_reply_controller
)

post_bp = Blueprint("post", __name__)



@post_bp.route("/create", methods=["GET", "POST"])
def create_post():
    return create_post_controller()


@post_bp.route("/<int:post_id>")
def post_detail(post_id):
    return post_detail_controller(post_id)



@post_bp.route("/<int:post_id>/like", methods=["POST"])
def add_like(post_id):
    return add_like_controller(post_id)



@post_bp.route("/<int:post_id>/comment", methods=["POST"])
def add_comment(post_id):
    return add_comment_controller(post_id)


@post_bp.route("/<int:post_id>/comment/<int:comment_id>/reply", methods=["POST"])
def add_reply(post_id, comment_id):
    return add_reply_controller(post_id, comment_id)
