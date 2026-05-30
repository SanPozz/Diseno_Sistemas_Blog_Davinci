from app.models.Posts import Post
from app.strategies.MostViewedPostsStrategy import MostViewedPostsStrategy
from app.strategies.PopularPostsStrategy import PopularPostsStrategy
from app.strategies.RecentPostsStrategy import RecentPostsStrategy

from app.database import db

class PostsService:
    def __init__(self, posts_repository, category_repository):
        self.posts_repository = posts_repository
        self.category_repository = category_repository

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

        category = self.category_repository.get_by_id(post_data['category_id'])

        if not category:
            return None, "Categoría no encontrada"

        post = Post(title=post_data['title'], content=post_data['content'], userId=post_data['user_id'])

        if not post:
            return None, "Error al crear el post"

        post.categories.append(category)

        RESULT_CREATE = self.posts_repository.create(post)

        if not RESULT_CREATE:
            return None, "Error al crear el post"

        return RESULT_CREATE, None

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

        # Retorna: posts, error
        # Param: Stategy (string)

        if strategy == "popular":
            posts = PopularPostsStrategy().get_posts();

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