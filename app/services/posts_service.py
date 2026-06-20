from app.models.Posts import Post
from app.models.Comments import Comment

from app.repositories.user_repository import UserRepository
from app.repositories.post_repository import PostRepository
from app.repositories.categories_repository import CategoryRepository

from app.strategies.MostViewedPostsStrategy import MostViewedPostsStrategy
from app.strategies.PopularPostsStrategy import PopularPostsStrategy
from app.strategies.RecentPostsStrategy import RecentPostsStrategy

from app.subjects.PostSubject import PostSubject
from app.observers.NotificationObserver import NotificationObserver

from app.database import db
from bleach import clean


class PostsService:

    def __init__(self, posts_repository, category_repository):

        self.posts_repository = posts_repository
        self.category_repository = category_repository

        # Patron Observer
        self.post_subject = PostSubject()
        self.post_subject.attach(NotificationObserver())

    # Función para sanitizar HTML usando bleach
    @staticmethod
    def sanitize_html(html_content):

        allowed_tags = [
            'p', 'br', 'strong', 'em', 'u', 's', 
            'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 
            'blockquote', 'code', 'pre', 'ul', 'ol', 'li', 
            'a', 'img', 'hr', 'div', 'span'
        ]
        allowed_attributes = {
            'a': ['href', 'title'], 
            'img': ['src', 'alt', 'title'],
            'div': ['class'],
            'span': ['style', 'class']
        }
        
        return clean(
            html_content,
            tags=allowed_tags,
            attributes=allowed_attributes,
            strip=True
        )

    def get_all_posts(self):
        return self.posts_repository.get_all_posts()

    def get_post_by_id(self, post_id):

        post = self.posts_repository.get_by_id(post_id)

        if not post:
            return None, "Post no encontrado"

        post.visitas += 1

        db.session.commit()

        return post, None

    def create_post(self, post_data):

        category = self.category_repository.get_by_id(
            post_data['category_id']
        )

        if not category:
            return None, "Categoría no encontrada"

        # Sanitizar contenido HTML 
        sanitized_content = self.sanitize_html(post_data['content'])

        post = Post(
            title=post_data['title'],
            content=sanitized_content,
            image=post_data.get('image'),
            userId=post_data['user_id']
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

    
    def add_like(self, post_id, user_id):

        post = self.posts_repository.get_by_id(post_id)

        if not post:
            return None, "Post no encontrado"

        
        
        user = UserRepository.get_by_id(user_id)
        
        if not user:
            return None, "Usuario no encontrado"

        # Verificar si el usuario ya le dio like
        if user in post.liked_by_users:
            # Si ya le dio like, sacarlo
            post.liked_by_users.remove(user)
            post.likes = max(0, post.likes - 1)
            db.session.commit()
            return post, None

        # Si no, agregar el like
        post.liked_by_users.append(user)
        post.likes += 1

        db.session.commit()

        # Notificar observers
        self.post_subject.notify({
            "event": "like",
            "post": post
        })

        return post, None


    def get_post_comments_tree(self, post):
        from app.composite.CommentBuilder import CommentBuilder
        return CommentBuilder.build_tree(post.comments)

    def add_comment(self, post_id, user_id, text):

        post = self.posts_repository.get_by_id(post_id)

        if not post:
            return None, "Post no encontrado"

        # Sanitizar texto del comentario
        cleaned_text = self.sanitize_html(text)

        comment = Comment(
            user_id=user_id,
            post_id=post_id,
            text=cleaned_text
        )

        db.session.add(comment)
        db.session.commit()

        # Notificar observers
        self.post_subject.notify({
            "event": "comment",
            "post": post
        })

        return comment, None

    def add_reply(self, post_id, user_id, text, father_id):

        post = self.posts_repository.get_by_id(post_id)

        if not post:
            return None, "Post no encontrado"

        parent = Comment.query.get(father_id)

        if not parent or parent.post_id != post_id:
            return None, "Comentario padre no encontrado"

        # Sanitizar texto de la respuesta
        cleaned_text = self.sanitize_html(text)

        reply = Comment(
            user_id=user_id,
            post_id=post_id,
            father_id=father_id,
            text=cleaned_text
        )

        db.session.add(reply)
        db.session.commit()

        return reply, None


# Instancia única de PostsService (patrón Singleton por instancia de módulo)
posts_service = PostsService(PostRepository, CategoryRepository)