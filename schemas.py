from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class ReviewCreate(BaseModel):
    entity_id: int
    rating: float
    comment: str | None = None

class ReviewResponse(BaseModel):
    id: int
    entity_id: int
    rating: float
    comment: str | None
    timestamp: datetime

    class Config:
        from_attributes = True

class EntityCreate(BaseModel):
    entity_type: str
    entity_price: float
    entity_seller: str
    entity_name: str

class EntityResponse(BaseModel):
    id: int
    entity_type: str
    entity_price: float
    entity_seller: str
    entity_name: str
    reviews: List[int] = []

    class Config:
        from_attributes = True

class ReviewUpdate(BaseModel):
    rating: Optional[float] = None
    comment: Optional[str] = None