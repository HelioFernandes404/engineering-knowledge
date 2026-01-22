from sqlalchemy import Column, Integer, String, DateTime, Date, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.session import Base

class Card(Base):
    __tablename__ = "cards"

    id = Column(Integer, primary_key=True, index=True)
    question = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    current_stage = Column(Integer, default=0)
    next_review_date = Column(Date, default=func.current_date())
    
    month_id = Column(Integer, ForeignKey("study_months.id"), nullable=True)
    month = relationship("StudyMonth", back_populates="cards")
