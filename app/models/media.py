from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base

class Media(Base):
    __tablename__ = 'media'
    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    entity_type = Column(String, nullable=False)  # 'user' or 'post'
    entity_id = Column(Integer, nullable=False)
    # Relationships
    # The relationships with Post and User are now defined in their respective models using backref
    # No need to define relationships here
