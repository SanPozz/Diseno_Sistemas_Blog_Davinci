from flask import render_template, request, redirect, jsonify
from flask_login import current_user, login_required

from app.services.posts_service import PostsService

from app.repositories.post_repository import PostRepository
from app.repositories.categories_repository import CategoryRepository

posts_service = PostsService(PostRepository, CategoryRepository)

# Landing controller
def landing_controller():

    return render_template("landing.html")

# Home controller
def home_controller():

    
    filter_type = request.args.get("filter", "recent")

    RESULT_SERVICE = posts_service.get_posts_by_strategy(filter_type)

    posts = RESULT_SERVICE[0]
    error = RESULT_SERVICE[1]

    if error:
        return render_template("home.html", error=error)

    return render_template("home.html", posts=posts)