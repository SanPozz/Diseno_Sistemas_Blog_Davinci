from abc import ABC, abstractmethod


class CommentComponent(ABC):
    """Componente abstracto del patrón Composite para comentarios."""

    @abstractmethod
    def get_id(self):
        pass

    @abstractmethod
    def get_text(self):
        pass

    @abstractmethod
    def get_author(self):
        pass

    @abstractmethod
    def get_created_at(self):
        pass

    @abstractmethod
    def get_children(self):
        pass

    @abstractmethod
    def is_composite(self):
        pass
