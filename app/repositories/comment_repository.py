from app.models.Comments import Comment
from app.database import db


class CommentRepository:

    @staticmethod
    def create(comment):

        db.session.add(comment)
        db.session.commit()

        return comment

    @staticmethod
    def get_by_id(comment_id):

        return Comment.query.get(comment_id)

    @staticmethod
    def get_comments_by_post(post_id):

        return Comment.query.filter_by(post_id=post_id).all()

    @staticmethod
    def get_root_comments(post_id):
        return Comment.query.filter_by(post_id=post_id, father_id=None).all()
