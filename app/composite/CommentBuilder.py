from app.composite.CommentLeaf import CommentLeaf
from app.composite.CommentComposite import CommentComposite


class CommentBuilder:
    """Construye el árbol Composite a partir de los objetos Comment del modelo."""

    @staticmethod
    def build(comment):
        if comment.replies:
            node = CommentComposite(comment)
            for reply in comment.replies:
                node.add_child(CommentBuilder.build(reply))
            return node
        return CommentLeaf(comment)

    @staticmethod
    def build_tree(comments):
        
        return [
            CommentBuilder.build(c)
            for c in comments
            if c.father_id is None
        ]
