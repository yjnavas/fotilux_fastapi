from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    user_name = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    address = Column(String, nullable=True)
    bio = Column(String, nullable=True)
    mail = Column(String, unique=True, nullable=False, index=True)
    password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    # Relationships
    posts = relationship('Post', back_populates='user')
    comments = relationship('Comment', back_populates='user')
    likes = relationship('Like', back_populates='user')
    favorites = relationship('Favorite', back_populates='user')
    media = relationship('Media', 
                         primaryjoin="and_(Media.entity_id==User.id, Media.entity_type=='user')", 
                         foreign_keys="[Media.entity_id]", 
                         backref="user_profile")
    # followers/following handled in Follow

class Follow(Base):
    __tablename__ = 'follow'
    following_user_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    followed_user_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow)
