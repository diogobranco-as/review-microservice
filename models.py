from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime, func
from sqlalchemy.orm import relationship
from database import Base

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    entity_id = Column(Integer, ForeignKey("entities.id"), nullable=False, index=True)  # Foreign key to an entity which can be reviewed
    rating = Column(Float, nullable=False)
    comment = Column(String, nullable=True)
    timestamp = Column(DateTime, default=func.now())

    # Many-to-One: Each review belongs to one entity
    entity = relationship("Entity", back_populates="reviews")

class Entity(Base):
    __tablename__ = "entities"

    id = Column(Integer, primary_key=True, index=True)
    entity_type = Column(String, nullable=False)
    entity_price = Column(Float, nullable=False)
    entity_seller = Column(String, nullable=False)
    entity_name = Column(String, nullable=False)

    reviews = relationship("Review", back_populates="entity") # one to many relationship with reviews
