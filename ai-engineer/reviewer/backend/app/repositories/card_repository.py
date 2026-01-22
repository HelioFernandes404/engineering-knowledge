from sqlalchemy.orm import Session
from app.models.card import Card
from datetime import date

class CardRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, question: str, month_id: int = None, current_stage: int = 0, next_review_date: date = None):
        if next_review_date is None:
            next_review_date = date.today()
        card = Card(question=question, month_id=month_id, current_stage=current_stage, next_review_date=next_review_date)
        self.db.add(card)
        self.db.commit()
        self.db.refresh(card)
        return card

    def get_all(self):
        return self.db.query(Card).all()

    def get_pending(self):
        return self.db.query(Card).filter(Card.next_review_date <= date.today()).all()

    def get_by_id(self, card_id: int):
        return self.db.query(Card).filter(Card.id == card_id).first()

    def update(self, card: Card):
        self.db.commit()
        self.db.refresh(card)
        return card
        
    def delete(self, card_id: int):
        card = self.get_by_id(card_id)
        if card:
            self.db.delete(card)
            self.db.commit()
        return card
