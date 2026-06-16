from flask_sqlalchemy import SQLAlchemy

from app.database import db

# Tabla pivote posts-categorias
category_post = db.Table(
    "category_post",
    db.Column(
        "category_id", db.Integer, db.ForeignKey("categories.id"), primary_key=True
    ),
    db.Column("post_id", db.Integer, db.ForeignKey("posts.id"), primary_key=True),
)

# Tabla pivote posts-likes
post_likes = db.Table(
    "post_likes",
    db.Column("user_id", db.Integer, db.ForeignKey("users.id"), primary_key=True),
    db.Column("post_id", db.Integer, db.ForeignKey("posts.id"), primary_key=True),
    db.Column("created_at", db.DateTime, nullable=False, default=db.func.current_timestamp())
)


class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(255), nullable=True)
    likes = db.Column(db.Integer, default=0)
    visitas = db.Column(db.Integer, default=0)

    user = db.relationship("User", back_populates="posts", lazy=True)

    created_at = db.Column(
        db.DateTime, nullable=False, default=db.func.current_timestamp()
    )
    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp(),
    )

    categories = db.relationship("Category",
                                secondary="category_post",
                                back_populates="posts",
                                lazy=True
    )
    comments = db.relationship("Comment",
                                back_populates="post",
                                lazy=True)
    
    liked_by_users = db.relationship("User",
                                    secondary="post_likes",
                                    lazy=True,
                                    backref=db.backref("liked_posts", lazy=True)
    )

    def __repr__(self):
        return f"<Post {self.title} Post ID: {self.id}>"

    def to_dict(self):
        return {
            "id": self.id,
            "userId": self.userId,
            "title": self.title,
            "content": self.content,
            "image": self.image,
            "likes": self.likes,
            "visitas": self.visitas,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "categories": [category.to_dict() for category in self.categories],
            "comments": [comment.to_dict() for comment in self.comments],
            "liked_by_users": [user.id for user in self.liked_by_users]
        }
