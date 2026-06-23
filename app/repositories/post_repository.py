from requests import post

from app.models.Posts import Post
from app.models.Categories import Category
from app.database import db


class PostRepository:
    @staticmethod
    def get_by_id(post_id):
        return Post.query.get(post_id)

    @staticmethod
    def get_posts_by_user(user_id):
        return Post.query.filter_by(user_id=user_id).all()

    @staticmethod
    def create(post):
        db.session.add(post)
        db.session.commit()
        return post

    @staticmethod
    def get_all():
        return Post.query.all()

    @staticmethod
    def get_by_category(category_id):
        category = Category.query.get(category_id)
        return category.posts if category else []

    @staticmethod
    def update_post(post_id, post_data):
        post = Post.query.get(post_id)
        if not post:
            return None, "Post no encontrado"

        if "title" in post_data:
            post.title = post_data["title"]
        if "content" in post_data:
            post.content = post_data["content"]
        if "image" in post_data and post_data["image"] is not None:
            post.image = post_data["image"]
        if "category_id" in post_data:
            category = Category.query.get(post_data["category_id"])
            if category:
                post.categories = [category]

        db.session.commit()
        return post, None

    @staticmethod
    def delete_post(post_id):
        from app.models.Comments import Comment

        post = Post.query.get(post_id)
        if not post:
            return False, "Post no encontrado"

        # Eliminar comentarios primero (incluyendo respuestas)
        Comment.query.filter_by(post_id=post_id).delete()

        # Limpiar relaciones de tablas pivote
        post.categories.clear()
        post.liked_by_users.clear()

        db.session.delete(post)
        db.session.commit()
        return True, None
