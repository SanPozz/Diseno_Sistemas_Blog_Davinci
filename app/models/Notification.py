from flask_sqlalchemy import SQLAlchemy
from app.database import db


class Notification(db.Model):
    __tablename__ = "notifications"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    message = db.Column(db.String(255), nullable=False)
    is_read = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(
        db.DateTime, default=db.func.current_timestamp(), nullable=False
    )
    user = db.relationship("User", back_populates="notifications")

    def __repr__(self):
        return f"<Notification {self.id} - User {self.user_id}>"
