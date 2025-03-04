from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ReviewCreate(BaseModel):
    product_id: str
    rating: float
    comment: str | None = None

class ReviewResponse(BaseModel):
    id: int
    product_id: str
    rating: float
    comment: str | None
    timestamp: datetime

    class Config:
        from_attributes = True

class ReviewUpdate(BaseModel):
    rating: Optional[float] = None
    comment: Optional[str] = None