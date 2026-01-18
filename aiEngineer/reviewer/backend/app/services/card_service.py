import os
from sqlalchemy.orm import Session
from app.repositories.card_repository import CardRepository
from app.repositories.review_repository import ReviewRepository
from app.services.spaced_repetition import calculate_next_review

class CardService:
    def __init__(self, db: Session):
        self.card_repo = CardRepository(db)
        self.review_repo = ReviewRepository(db)
        self.reset_to = os.getenv("REVIEW_RESET_TO", "D2")

    def create_card(self, question: str, month_id: int = None, current_stage: int = 0):
        from app.services.spaced_repetition import CYCLE
        from datetime import datetime, timedelta
        
        days_to_add = 0
        if 0 <= current_stage < len(CYCLE):
            days_to_add = CYCLE[current_stage]
        
        next_review_date = datetime.now().date() + timedelta(days=days_to_add)
        return self.card_repo.create(question, month_id, current_stage, next_review_date)

    def get_all_cards(self):
        return self.card_repo.get_all()

    def get_pending_cards(self):
        return self.card_repo.get_pending()

    def process_review(self, card_id: int, success: bool):
        card = self.card_repo.get_by_id(card_id)
        if not card:
            return None

        # Log review
        self.review_repo.create(card_id=card.id, stage=card.current_stage, success=success)

        # Calculate next
        next_stage, next_date = calculate_next_review(card.current_stage, success, self.reset_to)

        # Update card
        card.current_stage = next_stage
        card.next_review_date = next_date
        return self.card_repo.update(card)
        
    def delete_card(self, card_id: int):
        return self.card_repo.delete(card_id)

    def update_card_question(self, card_id: int, question: str):
        card = self.card_repo.get_by_id(card_id)
        if card:
            card.question = question
            return self.card_repo.update(card)
        return None