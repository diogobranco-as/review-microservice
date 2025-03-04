from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime, func
from database import Base

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(String, index=True)  # Foreign key to Product Service
    rating = Column(Float, nullable=False)
    comment = Column(String, nullable=True)
    timestamp = Column(DateTime, default=func.now())
