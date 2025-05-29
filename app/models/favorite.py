from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base

class Favorite(Base):
    __tablename__ = 'favorites'
    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey('post.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    # Relationships
    post = relationship('Post', back_populates='favorites')
    user = relationship('User', back_populates='favorites')
