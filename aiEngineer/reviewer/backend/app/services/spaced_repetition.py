import os
from datetime import datetime, timedelta

CYCLE = [0, 2, 7, 14, 30]

def calculate_next_review(current_stage: int, success: bool, review_reset_to: str = "D2"):
    if success:
        next_stage = current_stage + 1
        if next_stage >= len(CYCLE):
            next_stage = len(CYCLE) - 1
    else:
        # Reset
        if review_reset_to == "D0":
            next_stage = 0
        else:
            next_stage = 1 # D2

    days_to_add = CYCLE[next_stage]
    next_date = datetime.now().date() + timedelta(days=days_to_add)
    
    return next_stage, next_date
