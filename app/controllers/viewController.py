from flask import render_template, request, redirect, jsonify
from flask_login import current_user, login_required
from app.models.Notifications import Notification
from app.services.posts_service import posts_service


# Landing controller
def landing_controller():

    return render_template("landing.html")


# Home controller
def home_controller():

    filter_type = request.args.get("filter", "recent")

    RESULT_SERVICE = posts_service.get_posts_by_strategy(filter_type)

    posts = RESULT_SERVICE[0]
    error = RESULT_SERVICE[1]

    if error:
        return render_template("home.html", error=error)

    notifications = []

    if current_user.is_authenticated:
        notifications = (
            Notification.query.filter_by(user_id=current_user.id)
            .order_by(Notification.created_at.desc())
            .limit(20)
            .all()
        )

    return render_template("home.html", posts=posts, notifications=notifications)
