from flask_sqlalchemy import SQLAlchemy;
from app.database import db

class Comment(db.Model):
    __tablename__ = "comments";

    id = db.Column(db.Integer, primary_key=True);
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False);
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"), nullable=False);
    father_id = db.Column(db.Integer, db.ForeignKey("comments.id"), nullable=True);
    text = db.Column(db.Text, nullable=False);
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp());

    replies = db.relationship("Comment", backref=db.backref("father", remote_side=[id]), lazy="selectin");

    user = db.relationship("User", backref="comments", lazy=True);
    post = db.relationship("Post", backref="comments", lazy=True);

    def __repr__(self):
        return f"<Comment ID: {self.id} User ID: {self.user_id} Post ID: {self.post_id}>";

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "post_id": self.post_id,
            "father_id": self.father_id,
            "text": self.text,
            "created_at": self.created_at,
            "replies": [reply.to_dict() for reply in self.replies]
        };

