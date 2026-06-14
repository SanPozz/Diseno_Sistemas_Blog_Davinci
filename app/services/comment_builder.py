from app.composite.CommentLeaf import CommentLeaf
from app.composite.CommentComposite import CommentComposite


def build_comment_tree(comment):

    # Si no tiene respuestas
    if len(comment.children) == 0:

        return CommentLeaf(comment)

    # Si tiene respuestas
    composite = CommentComposite(comment)

    for child in comment.children:

        composite.add(build_comment_tree(child))

    return composite
