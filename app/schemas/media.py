from pydantic import BaseModel
from datetime import datetime

class MediaOut(BaseModel):
    id: int
    url: str
    created_at: datetime
    entity_type: str
    entity_id: int
    
    class Config:
        orm_mode = True
