from .CommentComponent import CommentComponent


class CommentComposite(CommentComponent):

    def __init__(self, comment):
        self.comment = comment
        self.children = []  # crea lista de hijos almacenados

    def add(self, comment):
        self.children.append(comment)

    def remove(self, comment):
        self.children.remove(comment)

    def display(
        self, level=0
    ):  # comvertimos el comentario a un diccionario para mostrarlo en el frontend y los recorremos

        return {
            "id": self.comment.id,
            "text": self.comment.text,
            "user": self.comment.user.username,
            "replies": [child.display(level + 1) for child in self.children],
        }
