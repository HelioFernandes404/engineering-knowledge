from sqlalchemy.orm import Session
from app.models.review import Review

class ReviewRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, card_id: int, stage: int, success: bool):
        review = Review(card_id=card_id, stage=stage, success=success)
        self.db.add(review)
        self.db.commit()
        self.db.refresh(review)
        return review
