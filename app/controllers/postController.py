from flask import render_template, request, redirect

from flask_login import current_user, login_required

from markupsafe import escape

from app.database import db

from app.models.Posts import Post


# LANDING
def landing_controller():

    posts = Post.query.order_by(Post.created_at.desc()).all()

    return render_template("blog/landing.html", posts=posts)


# CREAR POST
@login_required
def create_post_controller():

    if request.method == "POST":

        title = escape(request.form["title"])

        content = escape(request.form["content"])

        post = Post(title=title, content=content, userId=current_user.id)

        db.session.add(post)

        db.session.commit()

        return redirect("/landing")

    return render_template("blog/create_post.html")


# VER POST
def post_detail_controller(post_id):

    post = Post.query.get_or_404(post_id)

    return render_template("blog/post_detail.html", post=post)
