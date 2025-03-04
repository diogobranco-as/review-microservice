from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
import schemas, crud

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/v1/reviews", response_model=schemas.ReviewResponse)
def create_review(review: schemas.ReviewCreate, db: Session = Depends(get_db)):
    return crud.create_review(db, review)

@router.get("/v1/reviews/product/{product_id}", response_model=list[schemas.ReviewResponse])
def get_reviews(product_id: str, db: Session = Depends(get_db)):
    return crud.get_reviews_by_product(db, product_id)

@router.delete("/v1/reviews/{review_id}")
def delete_review(review_id: int, db: Session = Depends(get_db)):
    review = crud.delete_review(db, review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    return {"message": "Review deleted successfully"}

@router.put("/v1/reviews/{review_id}", response_model=schemas.ReviewResponse)
def update_review(review_id: int, review: schemas.ReviewUpdate, db: Session = Depends(get_db)):
    updated_review = crud.update_review(db, review_id, review)
    if not updated_review:
        raise HTTPException(status_code=404, detail="Review not found")
    return updated_review
