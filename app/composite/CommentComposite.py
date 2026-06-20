from app.composite.CommentComponent import CommentComponent


class CommentComposite(CommentComponent):
    """Compuesto del patrón Composite: comentario con respuestas anidadas."""

    def __init__(self, comment):
        self._comment = comment
        self._children = []

    def get_id(self):
        return self._comment.id

    def get_text(self):
        return self._comment.text

    def get_author(self):
        return self._comment.user.username if self._comment.user else "Desconocido"

    def get_created_at(self):
        return self._comment.created_at

    def add_child(self, component):
        self._children.append(component)

    def remove_child(self, component):
        self._children.remove(component)

    def get_children(self):
        return self._children

    def is_composite(self):
        return True
