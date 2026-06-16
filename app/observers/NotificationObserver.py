from app.models.Notification import Notification
from app.observers.Observer import Observer
from app.database import db


class NotificationObserver(Observer):

    def update(self, data):

        event = data["event"]
        post = data["post"]

        if event == "like":

            owner = post.user
            actor = data["actor"]

            if owner.id != actor.id:

                notification = Notification(
                    user_id=owner.id,
                    message=f"{actor.username} le dio like al post '{post.title}'",
                )

                db.session.add(notification)

        elif event == "comment":

            owner = post.user
            actor = data["actor"]

            if owner.id != actor.id:

                notification = Notification(
                    user_id=owner.id,
                    message=f"{actor.username} comentó el post '{post.title}'",
                )

                db.session.add(notification)

        elif event == "reply":

            parent_comment = data["parent_comment"]
            owner = parent_comment.user
            actor = data["actor"]

            if owner.id != actor.id:

                notification = Notification(
                    user_id=owner.id,
                    message=f"{actor.username} respondió tu comentario en el post '{post.title}'",
                )

                db.session.add(notification)

        db.session.commit()
