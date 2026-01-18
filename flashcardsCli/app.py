import csv
import io
import logging
import os
import re
import requests
import simpleaudio as sa
import pygame
from datetime import date, timedelta, datetime

# ————— CONFIG —————
API_URL      = "http://localhost:5002/api/tts"
TXT_FILE     = "ingles.txt"
CSV_FILE     = "ingles_data_v1.csv"
DATE_FMT     = "%Y-%m-%d"

# SM‑2 defaults (add STRETCH_FACTOR)
INITIAL_EASINESS = 2.5
MIN_EASINESS     = 2.1 # minimum easiness
STRETCH_FACTOR   = 1.8 # stretch factor for interval

# ————— LOGGING —————
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


# ————— TTS & PLAYBACK (unchanged) —————
def tts_bytes(text, speaker_id="p258", language_id="", style_wav=""):
    logging.info("TTS: %r", text)
    params = {"text": text, "speaker_id": speaker_id,
              "language_id": language_id, "style_wav": style_wav}
    resp = requests.get(API_URL, params=params)
    resp.raise_for_status()
    return resp.content

def play_wav_bytes(wav_bytes):
    pygame.mixer.init()
    sound = pygame.mixer.Sound(io.BytesIO(wav_bytes))
    sound.play()
    while pygame.mixer.get_busy():
        pygame.time.delay(100)
    pygame.mixer.quit()


# ————— 1) TXT PARSING —————
def parse_txt():
    """Return list of (front, back) from ingles.txt."""
    with open(TXT_FILE, encoding="utf-8") as f:
        content = f.read()
    # match: " ... " <tab> back
    pattern = r'"([\s\S]*?)"\s+([^\n]+)'
    matches = re.findall(pattern, content)
    cards = []
    for front_raw, back in matches:
        front = "\n".join(line.strip()
                          for line in front_raw.strip().splitlines()
                          if line.strip())
        cards.append((front, back.strip()))
    logging.info("Parsed %d cards from TXT", len(cards))
    return cards


# ————— 2) CSV STORAGE & SM‑2 —————
def init_csv():
    """If CSV missing, seed it from the TXT with default SM‑2 fields."""
    if os.path.exists(CSV_FILE):
        logging.info("CSV already exists.")
        return
    headers = ["id", "front", "back", "repetition", "interval", "easiness",
            "last_review", "next_review", "lapses"]
    cards = parse_txt()
    today = date.today().strftime(DATE_FMT)
    with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        for idx, (front, back) in enumerate(cards, start=1):
            writer.writerow({
                "id": idx,
                "front": front,
                "back": back,
                "repetition": 0,
                "interval": 0,
                "easiness": INITIAL_EASINESS,
                "last_review": "",
                "next_review": today,
                "lapses": 0
            })
    logging.info("Seeded CSV with %d cards.", len(cards))

def load_all():
    """Return list of row‑dicts from CSV."""
    with open(CSV_FILE, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    for r in rows:
        if "lapses" not in r:
            r["lapses"] = '0'
    return rows

def save_all(rows):
    """Overwrite CSV with given list of row‑dicts."""
    if not rows: return
    with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

def sm2_update(card, quality):
    """
    Update a single card (dict) per SM‑2 rules based on quality (0–5).
    Returns updated card dict.
    """
    q = int(quality)
    if q < 0 or q > 5:
        raise ValueError("Quality must be 0–5")
    prev_rep = int(card["repetition"])
    prev_int = int(card["interval"])
    easiness  = float(card["easiness"])
    today     = date.today()

    if q < 3:
        rep = 0
        interval = 1
        if prev_rep >= 2:
            easiness = max(MIN_EASINESS, easiness - 0.1)
    else:
        rep = prev_rep + 1
        if rep == 1:
            interval = 1
        elif rep > 2:
            interval = round(prev_int * easiness * STRETCH_FACTOR)
        else:
            interval = round(prev_int * easiness)

    lapses = int(card.get("lapses", 0))
    if q < 3 and prev_rep >= 2:
        lapses += 1
    card["lapses"] = lapses

    # update easiness
    easiness = max(
        MIN_EASINESS,
        easiness + (0.1 - (5 - q) * (0.08 + (5 - q) * 0.02))
    )

    next_review = today + timedelta(days=interval)

    card.update({
        "repetition": rep,
        "interval": interval,
        "easiness":  f"{easiness:.2f}",
        "last_review": today.strftime(DATE_FMT),
        "next_review": next_review.strftime(DATE_FMT)
    })
    return card


# ————— 3) REVIEW with edit/delete —————
def review_flashcards():
    rows = load_all()
    today = date.today().strftime(DATE_FMT)
    due = [r for r in rows if r["next_review"] <= today]
    if not due:
        print("No cards due for review.")
        return

    # classify by previous interval (or days until due)
    soon = [r for r in due if int(r["interval"]) <= 7]
    long = [r for r in due if int(r["interval"]) > 3]
    print(f"\nReview options:")
    print(f"  [S] Soon-only     ({len(soon)} cards, interval ≤ 7 days)")
    print(f"  [L] Long-term     ({len(long)} cards, interval > 3 days)")
    print(f"  [A] All due       ({len(due)} cards total)")
    choice = input("Choose review scope [S/L/A]: ").strip().upper()
    to_review = {"S": soon, "L": long, "A": due}.get(choice, due)

    for card in to_review:
        print("\n--- FLASHCARD ---")
        print(card["front"])
        # 1) Fetch and play the front-card audio once
        try:
            audio = tts_bytes(card["front"])
            play_wav_bytes(audio)
        except Exception as e:
            print("TTS error:", e)

        # 2) Let user replay as many times as they like before reveal
        while True:
            choice = input("Press 'r' to replay audio, or Enter to reveal answer: ").strip().lower()
            if choice == 'r':
                try:
                    play_wav_bytes(audio)
                except Exception as e:
                    print("TTS error:", e)
            else:
                break

        logging.info("TTS: %r", card["back"])

        # 3) Also allow replay before grading (so they can hear the prompt again)
        while True:
            choice = input("Press 'r' to replay audio again, or Enter to grade: ").strip().lower()
            if choice == 'r':
                try:
                    play_wav_bytes(audio)
                except Exception as e:
                    print("TTS error:", e)
            else:
                break

        # 1) Quality grading
        while True:
            q = input(f'TTS: {card["front"]!r}: Quality (0-5)').strip()
            if q.isdigit() and 0 <= int(q) <= 5:
                break
            print("Enter an integer 0 through 5.")
        sm2_update(card, q)
        logging.info("Card %s updated via SM-2 (Q=%s) | Next review: %s", 
                    card["id"], q, card["next_review"])


        # 2) Edit?
        if input("Edit this card? (y/N): ").lower() == "y":
            new_front = input(" New front (blank=keep): ").strip()
            new_back  = input(" New back  (blank=keep): ").strip()
            if new_front:
                card["front"] = new_front
            if new_back:
                card["back"]  = new_back
            # reset review to today to retrain
            card["next_review"] = date.today().strftime(DATE_FMT)
            logging.info("Card %s edited.", card["id"])

        # 3) Delete?
        if input("Delete this card? (y/N): ").lower() == "y":
            rows = [r for r in rows if r["id"] != card["id"]]
            logging.info("Card %s deleted.", card["id"])
            # also remove from TXT: rebuild txt from remaining rows
            rebuild_txt_from(rows)
            continue

        # Save after each card
        save_all(rows)

    print("\nReview session complete.")
    logging.info("Review session finished.")

# ————— 4) CREATE NEW CARD —————
def create_flashcard():
    front = input("Enter English front: ").strip()
    back  = input("Enter Portuguese back: ").strip()
    if not front or not back:
        print("Both front and back required.")
        return

    # 4a) Append to TXT
    entry = '\n"\n' + front + '\n"\t' + back + '\n'
    with open(TXT_FILE, "a", encoding="utf-8", newline="\n") as f:
        f.write(entry)

    # 4b) Append to CSV
    rows = load_all()
    new_id = max(int(r["id"]) for r in rows) + 1
    today = date.today().strftime(DATE_FMT)
    rows.append({
        "id": new_id,
        "front": front,
        "back": back,
        "repetition": 0,
        "interval": 0,
        "easiness": f"{INITIAL_EASINESS:.2f}",
        "last_review": "",
        "next_review": today,
        "lapses": 0
    })
    save_all(rows)
    print("New flashcard added & scheduled for today.")

# ————— 5) HELPERS —————
def rebuild_txt_from(rows):
    """Rebuild ingles.txt from given CSV rows."""
    header = "#separator:tab\n#html:true\n\n"
    with open(TXT_FILE, "w", encoding="utf-8", newline="\n") as f:
        f.write(header)
        for r in rows:
            f.write('"\n' + r["front"] + '\n"\t' + r["back"] + '\n')
    logging.info("Rebuilt TXT from %d cards.", len(rows))

# ————— 6) STATS —————
def count_due():
    """Return the number of cards whose next_review ≤ today."""
    rows = load_all()
    today = date.today().strftime(DATE_FMT)
    return sum(1 for r in rows if r["next_review"] <= today)


def show_stats():
    rows = load_all()
    today = date.today()
    days_until = [ (datetime.strptime(r["next_review"], DATE_FMT).date() - today).days
                   for r in rows ]
    total    = len(rows)
    due_now  = sum(1 for d in days_until if d <= 0)
    soon     = sum(1 for d in days_until if 1 <= d <= 7)
    longterm = sum(1 for d in days_until if d > 7)
    avg_days = sum(days_until) / total

    print(f"Total cards:      {total}")
    print(f"Due now:          {due_now}")
    print(f"Due soon (≤7d):   {soon}")
    print(f"Long‑term (>=3d):  {longterm}")
    print(f"Avg days to due:  {avg_days:.1f}")

    hardest = sorted(rows, key=lambda r: int(r.get("lapses",0)), reverse=True)[:5]
    print("\nTop 5 hardest (by lapses):")
    for c in hardest:
        laps = int(c.get("lapses", 0))
        print(f"  [{laps:2}] {c['front'][:30]}…")

# ————— MAIN MENU —————
def main_menu():
    init_csv()
    while True:
        due = count_due()
        show_stats()
        print(f"\nYou have {due} card{'s' if due != 1 else ''} due for review today.")
        print("1) Create new flashcard")
        print("2) Review flashcards")
        print("3) Exit")
        choice = input("Choice: ").strip()
        if choice == "1":
            create_flashcard()
        elif choice == "2":
            review_flashcards()
        elif choice == "3":
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main_menu()
