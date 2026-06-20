from flask import render_template, request, redirect, jsonify
from flask_login import current_user, login_required
from markupsafe import escape

from app.services.posts_service import posts_service
from app.repositories.categories_repository import CategoryRepository
from app.utils.image_utils import save_post_image




# creacion de un post
@login_required
def create_post_controller():

    if request.method == "POST":

        title = escape(request.form["title"])
        content = request.form["content"]  
        category_id = request.form["category"]
        
        
        image_filename = None
        if 'image' in request.files:
            file = request.files['image']
            image_filename, error = save_post_image(file)
            if error:
                return render_template("create_post.html", error=error, categories=CategoryRepository.get_all())

        post_data = {
            "title": title,
            "content": content,
            "image": image_filename,
            "user_id": current_user.id,
            "category_id": category_id
        }

        RESULT_SERVICE = posts_service.create_post(post_data)

        post = RESULT_SERVICE[0]
        error = RESULT_SERVICE[1]

        if post:
            return redirect(f"/posts/{post.id}")
        
        if error:
            return render_template("create_post.html", error=error)
        
        return render_template("create_post.html", error="Error desconocido al crear el post.")

    categories = CategoryRepository.get_all()
    return render_template("create_post.html", categories=categories)


# ver un post
def post_detail_controller(post_id):

    RESULT_SERVICE = posts_service.get_post_by_id(post_id)

    post = RESULT_SERVICE[0]
    error = RESULT_SERVICE[1]

    if error:
        return render_template("post_detail.html", error=error)

    comment_tree = posts_service.get_post_comments_tree(post)

    return render_template("post_detail.html", post=post, comment_tree=comment_tree)

# Like a un post
@login_required
def add_like_controller(post_id):

    RESULT_SERVICE = posts_service.add_like(post_id, current_user.id)

    post = RESULT_SERVICE[0]
    error = RESULT_SERVICE[1]

    if error:
        return jsonify({"error": error}), 404

    return jsonify({
        "message": "Like agregado",
        "likes": post.likes
    }), 200


@login_required
def add_comment_controller(post_id):
    
    text = request.form.get("text", "").strip()

    if not text:
        return redirect(f"/posts/{post_id}?error=El comentario no puede estar vacío#comments")

    RESULT_SERVICE = posts_service.add_comment(
        post_id,
        current_user.id,
        text
    )

    comment = RESULT_SERVICE[0]
    error = RESULT_SERVICE[1]

    if error:
        return redirect(f"/posts/{post_id}?error={error}#comments")

    return redirect(f"/posts/{post_id}#comments")


# Responder un comentario 
@login_required
def add_reply_controller(post_id, comment_id):

    text = request.form.get("text", "").strip()

    if not text:
        return redirect(f"/posts/{post_id}?error=El comentario no puede estar vacío#comments")

    RESULT_SERVICE = posts_service.add_reply(
        post_id,
        current_user.id,
        text,
        comment_id
    )

    comment = RESULT_SERVICE[0]
    error = RESULT_SERVICE[1]

    if error:
        return redirect(f"/posts/{post_id}?error={error}#comments")

    return redirect(f"/posts/{post_id}#comments")
