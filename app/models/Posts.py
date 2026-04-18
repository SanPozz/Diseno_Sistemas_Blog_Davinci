from flask_sqlalchemy import SQLAlchemy;

from app.database import db;


category_post = db.Table('category_post',
    db.Column('category_id', db.Integer, db.ForeignKey('categories.id'), primary_key=True),
    db.Column('post_id', db.Integer, db.ForeignKey('posts.id'), primary_key=True)
);


class Post(db.Model):
    __tablename__ = "posts";

    id = db.Column(db.Integer, primary_key=True);
    userId = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False);
    title = db.Column(db.String(200), nullable=False);
    content = db.Column(db.Text, nullable=False);
    likes = db.Column(db.Integer, default=0);
    visitas = db.Column(db.Integer, default=0);

    user = db.relationship("User", back_populates="posts", lazy=True);

    created_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp());
    updated_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp());

    categories = db.relationship("Category", secondary="category_post", back_populates="posts", lazy=True);

    def __repr__(self):
        return f"<Post {self.title} Post ID: {self.id}>";

    def to_dict(self):
        return {
            "id": self.id,
            "userId": self.userId,
            "title": self.title,
            "content": self.content,
            "likes": self.likes,
            "visitas": self.visitas,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "categories": [category.to_dict() for category in self.categories]
        };
