from flask import jsonify
from flask_login import current_user, login_required

from app.models.Notifications import Notification
from app.database import db


@login_required
def get_notifications_controller():
    """Devuelve las notis en forma de json"""
    notifications = (
        Notification.query.filter_by(user_id=current_user.id)
        .order_by(Notification.created_at.desc())
        .limit(20)
        .all()
    )
    unread_count = Notification.query.filter_by(
        user_id=current_user.id, is_read=False
    ).count()
    return (
        jsonify(
            {
                "notifications": [n.to_dict() for n in notifications],
                "unread_count": unread_count,
            }
        ),
        200,
    )


@login_required
def mark_notification_read_controller(notification_id):
    """marca la noti como leida"""
    notification = Notification.query.filter_by(
        id=notification_id, user_id=current_user.id
    ).first()

    if not notification:
        return jsonify({"error": "Notificación no encontrada"}), 404

    notification.is_read = True
    db.session.commit()

    return jsonify({"message": "Notificación marcada como leída"}), 200


@login_required
def mark_all_notifications_read_controller():

    Notification.query.filter_by(user_id=current_user.id, is_read=False).update(
        {"is_read": True}
    )

    db.session.commit()

    return jsonify({"message": "Todas las notificaciones marcadas como leídas"}), 200
