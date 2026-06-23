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
        if "image" in request.files:
            file = request.files["image"]
            image_filename, error = save_post_image(file)
            if error:
                return render_template(
                    "create_post.html",
                    error=error,
                    categories=CategoryRepository.get_all(),
                )

        post_data = {
            "title": title,
            "content": content,
            "image": image_filename,
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

    post = RESULT_SERVICE[0]
    error = RESULT_SERVICE[1]

    if error:
        return render_template("post_detail.html", error=error)

    comment_tree = posts_service.get_post_comments_tree(post)

    return render_template("post_detail.html", post=post, comment_tree=comment_tree)


# editar un post
@login_required
def edit_post_controller(post_id):

    RESULT_SERVICE = posts_service.get_post_by_id(post_id)
    post = RESULT_SERVICE[0]
    error = RESULT_SERVICE[1]

    if error or not post:
        return redirect("/auth/profile")

    # Solo el autor puede editar
    if post.userId != current_user.id:
        return redirect(f"/posts/{post_id}")

    categories = CategoryRepository.get_all()

    if request.method == "POST":
        title = escape(request.form.get("title", "").strip())
        content = request.form.get("content", "").strip()
        category_id = request.form.get("category")

        image_filename = None
        if "image" in request.files:
            file = request.files["image"]
            if file and file.filename:
                image_filename, img_error = save_post_image(file)
                if img_error:
                    return render_template(
                        "edit_post.html",
                        post=post,
                        categories=categories,
                        error=img_error,
                    )

        post_data = {
            "title": title,
            "content": content,
            "category_id": category_id,
        }
        if image_filename:
            post_data["image"] = image_filename

        updated_post, upd_error = posts_service.update_post(post_id, post_data)

        if upd_error:
            return render_template(
                "edit_post.html", post=post, categories=categories, error=upd_error
            )

        return redirect(f"/posts/{post_id}")

    return render_template("edit_post.html", post=post, categories=categories)


# eliminar un post
@login_required
def delete_post_controller(post_id):

    post = posts_service.posts_repository.get_by_id(post_id)

    if not post:
        return jsonify({"error": "Post no encontrado"}), 404

    if post.userId != current_user.id:
        return jsonify({"error": "No tienes permiso para eliminar este post"}), 403

    success, error = posts_service.delete_post(post_id)

    if error:
        return jsonify({"error": error}), 500

    return jsonify({"message": "Post eliminado correctamente"}), 200


# Like a un post
@login_required
def add_like_controller(post_id):

    RESULT_SERVICE = posts_service.add_like(post_id, current_user.id)

    post = RESULT_SERVICE[0]
    error = RESULT_SERVICE[1]

    if error:
        return jsonify({"error": error}), 404

    return jsonify({"message": "Like agregado", "likes": post.likes}), 200


@login_required
def add_comment_controller(post_id):

    text = request.form.get("text", "").strip()

    if not text:
        return redirect(
            f"/posts/{post_id}?error=El comentario no puede estar vacío#comments"
        )

    RESULT_SERVICE = posts_service.add_comment(post_id, current_user.id, text)

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
        return redirect(
            f"/posts/{post_id}?error=El comentario no puede estar vacío#comments"
        )

    RESULT_SERVICE = posts_service.add_reply(post_id, current_user.id, text, comment_id)

    comment = RESULT_SERVICE[0]
    error = RESULT_SERVICE[1]

    if error:
        return redirect(f"/posts/{post_id}?error={error}#comments")

    return redirect(f"/posts/{post_id}#comments")
