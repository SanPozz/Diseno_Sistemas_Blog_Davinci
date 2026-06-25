from app.database import db


class Notification(db.Model):
    __tablename__ = "notifications"

    id = db.Column(db.Integer, primary_key=True)

    # el usuario dueño del post que recibe la notificación
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    # tipo de evento: "like" o "comment"
    event = db.Column(db.String(50), nullable=False)
    # mensaje
    message = db.Column(db.String(255), nullable=False)
    # ID del post relacionado para redirigir
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"), nullable=True)
    # marca si ya fue leida la notificacion
    is_read = db.Column(db.Boolean, default=False, nullable=False)

    created_at = db.Column(
        db.DateTime, nullable=False, default=db.func.current_timestamp()
    )

    # relaciones
    user = db.relationship("User", back_populates="notifications")
    post = db.relationship("Post", backref=db.backref("notifications", lazy="dynamic"))

    def __repr__(self):
        return f"<Notification ID:{self.id} user:{self.user_id} event:{self.event}>"

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "event": self.event,
            "message": self.message,
            "post_id": self.post_id,
            "is_read": self.is_read,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
