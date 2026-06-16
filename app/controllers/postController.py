from flask import render_template, request, redirect, jsonify
from flask_login import current_user, login_required
from markupsafe import escape
from app.database import db
from app.models.Posts import Post
from app.models.Categories import Category
from app.strategies.RecentPostsStrategy import RecentPostsStrategy
from app.strategies.PopularPostsStrategy import PopularPostsStrategy
from app.strategies.MostViewedPostsStrategy import MostViewedPostsStrategy
from app.models.Notification import Notification
from app.services.posts_service import PostsService
from app.repositories.post_repository import PostRepository
from app.repositories.categories_repository import CategoryRepository

posts_service = PostsService(PostRepository, CategoryRepository)


# Landing controller
@login_required
def landing_controller():

    # es un filtro dinamico que cambia segun la estrategia
    filter_type = request.args.get("filter", "recent")

    RESULT_SERVICE = posts_service.get_posts_by_strategy(filter_type)

    posts = RESULT_SERVICE[0]
    error = RESULT_SERVICE[1]

    if error:
        return render_template("landing.html", error=error)
    unread_notifications = Notification.query.filter_by(
        user_id=current_user.id, is_read=False
    ).count()

    return render_template(
        "landing.html", posts=posts, unread_notifications=unread_notifications
    )


# creacion de un post
@login_required
def create_post_controller():

    if request.method == "POST":

        title = escape(request.form["title"])
        content = escape(request.form["content"])
        category_id = request.form["category"]

        post_data = {
            "title": title,
            "content": content,
            "user_id": current_user.id,
            "category_id": category_id,
        }

        RESULT_SERVICE = posts_service.create_post(post_data)

        post = RESULT_SERVICE[0]
        error = RESULT_SERVICE[1]

        if post:
            return redirect(f"/posts/{post.id}")

        if error:
            return render_template("create_post.html", error=error)

        return render_template(
            "create_post.html", error="Error desconocido al crear el post."
        )

    categories = CategoryRepository.get_all()
    return render_template("create_post.html", categories=categories)


# ver un post
def post_detail_controller(post_id):

    RESULT_SERVICE = posts_service.get_post_by_id(post_id)

    data = RESULT_SERVICE[0]
    error = RESULT_SERVICE[1]

    if error:
        return render_template("post_detail.html", error=error)

    return render_template(
        "post_detail.html", post=data["post"], comments_tree=data["comments_tree"]
    )


# Like a un post
@login_required
def add_like_controller(post_id):

    RESULT_SERVICE = posts_service.add_like(post_id, current_user.id)

    post = RESULT_SERVICE[0]
    error = RESULT_SERVICE[1]

    if error:
        return jsonify({"error": error}), 404

    return redirect(f"/posts/{post_id}")


# Comentar un post
@login_required
def add_comment_controller(post_id):

    text = request.form["text"]

    father_id = request.form.get("father_id")

    if father_id:
        father_id = int(father_id)
    else:
        father_id = None

    RESULT_SERVICE = posts_service.add_comment(
        post_id, current_user.id, text, father_id
    )

    comment = RESULT_SERVICE[0]
    error = RESULT_SERVICE[1]

    if error:
        return jsonify({"error": error}), 404

    return redirect(f"/posts/{post_id}")


@login_required
def notifications_controller():

    notifications = (
        Notification.query.filter_by(user_id=current_user.id)
        .order_by(Notification.created_at.desc())
        .all()
    )
    return render_template("notifications.html", notifications=notifications)
