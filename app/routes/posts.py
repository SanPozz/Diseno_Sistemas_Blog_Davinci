from flask import Blueprint, request, redirect, render_template

from app.models.Posts import Post

posts_bp = Blueprint("posts", __name__);

@posts_bp.route("/", methods=["GET"])
def list_posts():
    
    return "Hola, esta es la lista de posts!";