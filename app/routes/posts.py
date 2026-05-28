from flask import Blueprint, request, redirect, render_template
from flask_jwt_extended import jwt_required
from app.models.Posts import Post

posts_bp = Blueprint("posts", __name__);

@posts_bp.route("/", methods=["GET"])
def list_posts():
      
      return render_template("register.html")
    