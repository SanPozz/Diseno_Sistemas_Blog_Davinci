from abc import ABC, abstractmethod


# clase padre del  commentLeaf y commentComposite
class CommentComponent(ABC):

    @abstractmethod
    def display(
        self, level=0
    ):  # inicia en nivel 0  y se incrementa dependiendo los comentarios
        pass

    @abstractmethod
    def add(self, comment):  # agrega un hijo/respuesta
        pass

    @abstractmethod
    def remove(self, comment):
        pass
