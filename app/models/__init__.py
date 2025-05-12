from app.models.user import User, Follow
from app.models.post import Post, PostStatus
from app.models.media import Media
from app.models.comment import Comment
from app.models.like import Like
from app.models.favorite import Favorite

# Import all models here for easy access
__all__ = [
    "User", "Follow", "Post", "PostStatus", 
    "Media", "Comment", "Like", "Favorite"
]
