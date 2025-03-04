from sqlalchemy.orm import Session
import models, schemas

def create_review(db: Session, review_data: schemas.ReviewCreate):
    review = models.Review(**review_data.model_dump())
    db.add(review)
    db.commit()
    db.refresh(review)
    return review

def get_reviews_by_product(db: Session, product_id: str):
    return db.query(models.Review).filter(models.Review.product_id == product_id).all()

def delete_review(db: Session, review_id: int):
    review = db.query(models.Review).filter(models.Review.id == review_id).first()
    if review:
        db.delete(review)
        db.commit()
    return review

def update_review(db: Session, review_id: int, review_data: schemas.ReviewUpdate):
    review = db.query(models.Review).filter(models.Review.id == review_id).first()
    if review:
        for key, value in review_data.model_dump().items():
            setattr(review, key, value)
        db.commit()
        db.refresh(review)
    return review
