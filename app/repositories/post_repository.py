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