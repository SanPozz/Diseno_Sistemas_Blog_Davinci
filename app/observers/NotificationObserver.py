from app.models.Notifications import Notification
from app.database import db
from app.observers.Observer import Observer


class NotificationObserver(Observer):

    def update(self, data):
        event = data.get("event")
        post = data.get("post")
        actor = data.get("actor")

        if event == "like":
            message = f'{actor.username} le dio like a tu post "{post.title[:50]}"'

        elif event == "comment":
            message = f'{actor.username} comentó tu post "{post.title[:50]}"'

        else:
            return

        notification = Notification(
            user_id=post.userId,  # dueño del post
            event=event,
            message=message,
            post_id=post.id,
            is_read=False,
        )

        db.session.add(notification)
        db.session.commit()
