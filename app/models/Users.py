from database import db;

from flask_login import UserMixin, login_manager;

class User(db.Model, UserMixin):
    __tablename__ = "users";

    id = db.Column(db.Integer, primary_key=True);
    username = db.Column(db.String(50), unique=True, nullable=False);
    email = db.Column(db.String(120), unique=True, nullable=False);
    hashed_password = db.Column(db.String(128), nullable=False);
    role = db.Column(db.String(20), nullable=False, default="user");

    def __repr__(self):
        return f"<User {self.username} User ID: {self.id}>";

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "role": self.role
        };


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id));