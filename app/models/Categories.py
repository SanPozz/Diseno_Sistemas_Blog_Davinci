from flask_sqlalchemy import SQLAlchemy

from app.database import db;

class Category(db.Model):
    __tablename__ = "categories";

    id = db.Column(db.Integer, primary_key=True);
    name = db.Column(db.String(50), unique=True, nullable=False);
    description = db.Column(db.String(200), nullable=True);


    created_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp());
    updated_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp());

    posts = db.relationship("Post", secondary="category_post", back_populates="categories", lazy=True);

    def __repr__(self):
        return f"<Category {self.name} Category ID: {self.id}>";

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "posts": [post.to_dict() for post in self.posts]
        };