from flask import render_template, request, redirect
from flask_login import current_user, login_required
from markupsafe import escape
from app.database import db
from app.models.Posts import Post
from app.models.Categories import Category
from app.strategies.RecentPostsStrategy import RecentPostsStrategy
from app.strategies.PopularPostsStrategy import PopularPostsStrategy
from app.strategies.MostViewedPostsStrategy import MostViewedPostsStrategy


# Landing controller
def landing_controller():

    # es un filtro dinamico que cambia segun la estrategia
    filter_type = request.args.get("filter", "recent")

    # esta es la estrategia por defecto
    strategy = RecentPostsStrategy()

    # aca se puede cambiar la estratigai si queres ver lo "popular" o lo "mas visto"
    if filter_type == "popular":

        strategy = PopularPostsStrategy()

    elif filter_type == "views":

        strategy = MostViewedPostsStrategy()

    # cada estrategia devuelve un post distinto
    posts = strategy.get_posts()

    return render_template("landing.html", posts=posts)


# creacion de un post
@login_required
def create_post_controller():

    if request.method == "POST":

        title = escape(request.form["title"])
        content = escape(request.form["content"])
        category_id = request.form["category"]
        category = Category.query.get(category_id)

        post = Post(title=title, content=content, userId=current_user.id)

        post.categories.append(category)
        db.session.add(post)

        db.session.commit()

        return redirect("/landing")

    categories = Category.query.all()
    return render_template("create_post.html", categories=categories)


# ver un post
def post_detail_controller(post_id):

    post = Post.query.get_or_404(post_id)

    # sumamos una visita
    post.visitas += 1

    db.session.commit()

    return render_template("post_detail.html", post=post)
