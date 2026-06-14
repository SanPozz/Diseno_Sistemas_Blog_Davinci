from app.observers.Observer import Observer


class NotificationObserver(Observer):

    def update(self, data):

        event = data["event"]
        post = data["post"]

        if event == "like":

            print(f"El post '{post.title}' recibió un like")

        elif event == "comment":

            print(f"El post '{post.title}' recibió un comentario")

        elif event == "reply":

            print(f"El post '{post.title}' recibió una respuesta a un comentario")
