from sqlalchemy import Column, Integer, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.session import Base

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    card_id = Column(Integer, ForeignKey("cards.id"), nullable=False)
    stage = Column(Integer, nullable=False)
    reviewed_at = Column(DateTime(timezone=True), server_default=func.now())
    success = Column(Boolean, nullable=False)

    card = relationship("Card")
