from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.session import Base

class StudyMonth(Base):
    __tablename__ = "study_months"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    number = Column(Integer, unique=True, nullable=False)
    
    cards = relationship("Card", back_populates="month")
