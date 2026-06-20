from app.composite.CommentComponent import CommentComponent


class CommentLeaf(CommentComponent):
    """Hoja del patrón Composite: comentario sin respuestas."""

    def __init__(self, comment):
        self._comment = comment

    def get_id(self):
        return self._comment.id

    def get_text(self):
        return self._comment.text

    def get_author(self):
        return self._comment.user.username if self._comment.user else "Desconocido"

    def get_created_at(self):
        return self._comment.created_at

    def get_children(self):
        return []

    def is_composite(self):
        return False
