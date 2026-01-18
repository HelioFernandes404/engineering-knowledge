from sqlalchemy import Column, Integer, Boolean, Date
from app.db.session import Base

class WeeklyCheckIn(Base):
    __tablename__ = "weekly_checkins"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False, index=True)
    q1 = Column(Boolean, default=False)
    q2 = Column(Boolean, default=False)
    q3 = Column(Boolean, default=False)
    q4 = Column(Boolean, default=False)
    q5 = Column(Boolean, default=False)
