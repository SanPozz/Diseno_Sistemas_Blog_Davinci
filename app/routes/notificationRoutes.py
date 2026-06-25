from flask import Blueprint

from app.controllers.notificationController import (
    get_notifications_controller,
    mark_notification_read_controller,
    mark_all_notifications_read_controller,
)

notification_bp = Blueprint("notifications", __name__)


@notification_bp.route("/", methods=["GET"])
def get_notifications():
    return get_notifications_controller()


@notification_bp.route("/<int:notification_id>/read", methods=["POST"])
def mark_read(notification_id):
    return mark_notification_read_controller(notification_id)


@notification_bp.route("/read-all", methods=["POST"])
def mark_all_read():
    return mark_all_notifications_read_controller()
