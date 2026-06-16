from requests import post

from app.models.Posts import Post
from app.models.Comments import Comment

from app.models.Users import User
from app.models.Users import User
from app.strategies.MostViewedPostsStrategy import MostViewedPostsStrategy
from app.strategies.PopularPostsStrategy import PopularPostsStrategy
from app.strategies.RecentPostsStrategy import RecentPostsStrategy
from app.services.comment_builder import build_comment_tree
from app.subjects.PostSubject import PostSubject
from app.observers.NotificationObserver import NotificationObserver

from app.database import db


class PostsService:

    def __init__(self, posts_repository, category_repository):

        self.posts_repository = posts_repository
        self.category_repository = category_repository

        # Patron Observer
        self.post_subject = PostSubject()

        self.post_subject.attach(NotificationObserver())

    def get_all_posts(self):
        return self.posts_repository.get_all_posts()

    def get_post_by_id(self, post_id):

        post = self.posts_repository.get_by_id(post_id)

        if not post:
            return None, "Post no encontrado"

        post.visitas += 1

        db.session.commit()

        # patron composite

        comments_tree = []

        root_comments = [
            comment for comment in post.comments if comment.father_id is None
        ]

        for comment in root_comments:
            tree = build_comment_tree(comment)
            comments_tree.append(tree.display())

        return {
            "post": post,
            "comments_tree": comments_tree,
        }, None

    # crear post
    def create_post(self, post_data):

        category = self.category_repository.get_by_id(post_data["category_id"])

        if not category:
            return None, "Categoría no encontrada"

        post = Post(
            title=post_data["title"],
            content=post_data["content"],
            userId=post_data["user_id"],
        )

        if not post:
            return None, "Error al crear el post"

        post.categories.append(category)

        result_create = self.posts_repository.create(post)

        if not result_create:
            return None, "Error al crear el post"

        return result_create, None

    def update_post(self, post_id, post_data):
        return self.posts_repository.update_post(post_id, post_data)

    def delete_post(self, post_id):
        return self.posts_repository.delete_post(post_id)

    def get_posts_by_category(self, category_id):
        return self.posts_repository.get_by_category(category_id)

    def get_posts_by_user(self, user_id):
        return self.posts_repository.get_posts_by_user(user_id)

    # Patron Strategy
    def get_posts_by_strategy(self, strategy):

        if strategy == "popular":

            posts = PopularPostsStrategy().get_posts()

            if posts:
                return posts, None
            else:
                return None, "No hay posts populares disponibles."

        elif strategy == "views":

            posts = MostViewedPostsStrategy().get_posts()

            if posts:
                return posts, None
            else:
                return None, "No hay posts con más vistas disponibles."

        else:

            posts = RecentPostsStrategy().get_posts()

            if posts:
                return posts, None
            else:
                return None, "No hay posts recientes disponibles."

    # Patron Observer

    def add_like(self, post_id, user_id):
        post = self.posts_repository.get_by_id(post_id)
        if not post:
            return None, "Post no encontrado"
        actor = User.query.get(user_id)
        post.likes += 1
        db.session.commit()
        # Notificar al observers
        self.post_subject.notify({"event": "like", "post": post, "actor": actor})

        return post, None

    # Patron Observer

    def add_comment(self, post_id, user_id, text, father_id=None):
        post = self.posts_repository.get_by_id(post_id)
        if not post:
            return None, "Post no encontrado"
        actor = User.query.get(user_id)
        comment = Comment(
            user_id=user_id, post_id=post_id, text=text, father_id=father_id
        )

        db.session.add(comment)
        db.session.commit()

        if father_id is not None:
            parent_comment = Comment.query.get(father_id)
            self.post_subject.notify(
                {
                    "event": "reply",
                    "post": post,
                    "comment": comment,
                    "parent_comment": parent_comment,
                    "actor": actor,
                }
            )
        else:
            self.post_subject.notify(
                {"event": "comment", "post": post, "comment": comment, "actor": actor}
            )
        return comment, None
