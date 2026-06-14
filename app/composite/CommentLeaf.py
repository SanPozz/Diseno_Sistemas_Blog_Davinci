from .CommentComponent import CommentComponent


class CommentLeaf(CommentComponent):

    def __init__(self, comment):
        self.comment = comment

    def display(
        self, level=0
    ):  # comvertimos el comentario a un diccionario para mostrarlo en el frontend

        return {
            "id": self.comment.id,
            "text": self.comment.text,
            "user": self.comment.user.username,
            "replies": [],
        }

    def add(self, comment):
        raise Exception("Un leaf no puede agregar comentarios o hijos")

    def remove(self, comment):
        raise Exception("Un leaf no puede eliminar comentarios o hijos")
