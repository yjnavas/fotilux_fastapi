from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
import enum
from datetime import datetime
from app.core.database import Base

class PostStatus(enum.Enum):
    active = "active"
    deleted = "deleted"

class Post(Base):
    __tablename__ = 'post'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    body = Column(Text, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    status = Column(String, default='active')
    created_at = Column(DateTime, default=datetime.utcnow)
    # Relationships
    user = relationship('User', back_populates='posts')
    comments = relationship('Comment', back_populates='post')
    likes = relationship('Like', back_populates='post')
    favorites = relationship('Favorite', back_populates='post')
    media = relationship('Media', 
                         primaryjoin="and_(Media.entity_id==Post.id, Media.entity_type=='post')", 
                         foreign_keys="[Media.entity_id]", 
                         backref="post")
