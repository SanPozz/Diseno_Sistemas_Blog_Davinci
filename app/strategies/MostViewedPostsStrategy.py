from app.strategies.PostStrategy import PostStrategy

from app.models.Posts import Post


class MostViewedPostsStrategy(PostStrategy):

    def get_posts(self):

        return Post.query.order_by(Post.visitas.desc()).all()
