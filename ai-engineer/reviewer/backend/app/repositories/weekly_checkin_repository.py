from sqlalchemy.orm import Session
from app.models.weekly_checkin import WeeklyCheckIn
from datetime import date

class WeeklyCheckInRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, date_val: date, answers: dict):
        checkin = WeeklyCheckIn(
            date=date_val,
            q1=answers.get('q1', False),
            q2=answers.get('q2', False),
            q3=answers.get('q3', False),
            q4=answers.get('q4', False),
            q5=answers.get('q5', False)
        )
        self.db.add(checkin)
        self.db.commit()
        self.db.refresh(checkin)
        return checkin

    def get_by_date(self, date_val: date):
        return self.db.query(WeeklyCheckIn).filter(WeeklyCheckIn.date == date_val).first()

    def get_all(self):
        return self.db.query(WeeklyCheckIn).order_by(WeeklyCheckIn.date.desc()).all()
