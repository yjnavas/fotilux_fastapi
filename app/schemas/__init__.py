from app.schemas.user import UserBase, UserCreate, UserOut
from app.schemas.post import PostBase, PostCreate, PostOut
from app.schemas.media import MediaOut
from app.schemas.comment import CommentOut
from app.schemas.like import LikeOut
from app.schemas.favorite import FavoriteOut
from app.schemas.follow import FollowOut

# Import all schemas here for easy access
__all__ = [
    "UserBase", "UserCreate", "UserOut",
    "PostBase", "PostCreate", "PostOut",
    "MediaOut", "CommentOut", "LikeOut", "FavoriteOut", "FollowOut"
]
