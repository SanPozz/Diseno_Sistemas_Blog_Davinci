from flask_login import UserMixin, login_manager

from app.database import db

class User(db.Model, UserMixin):
    __tablename__ = "users";

    id = db.Column(db.Integer, primary_key=True);
    username = db.Column(db.String(50), unique=True, nullable=False);
    email = db.Column(db.String(120), unique=True, nullable=False);
    hashed_password = db.Column(db.String(128), nullable=False);
    role = db.Column(db.String(20), nullable=False, default="user");

    created_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp());
    updated_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp());

    posts = db.relationship("Post", back_populates="user", lazy=True);
    comments = db.relationship("Comment", back_populates="user", lazy=True);

    def __repr__(self):
        return f"<User {self.username} User ID: {self.id}>";

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "role": self.role,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "posts": [post.to_dict() for post in self.posts],
            "comments": [comment.to_dict() for comment in self.comments],

        };

    

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id));