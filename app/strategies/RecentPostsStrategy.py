from app.strategies.PostStrategy import PostStrategy
from app.models.Posts import Post


class RecentPostsStrategy(PostStrategy):
    def get_posts(self):
        return Post.query.order_by(Post.created_at.desc()).all()
