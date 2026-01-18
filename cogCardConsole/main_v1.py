import torch
from TTS.api import TTS
from datetime import datetime, timedelta
import time
import random
import os  # Added for file existence check

class TTSWrapper:
    def __init__(self, model_name: str, progress_bar: bool = False, device: str = None):
        self.device = device if device is not None else self._get_device()
        self.model_name = model_name
        self.tts = self._initialize_tts(model_name, progress_bar)
    
    def _get_device(self) -> str:
        return "cuda" if torch.cuda.is_available() else "cpu"
    
    def _initialize_tts(self, model_name: str, progress_bar: bool) -> TTS:
        return TTS(model_name=model_name, progress_bar=progress_bar).to(self.device)

    @staticmethod
    def list_available_models() -> list:
        return TTS().list_models()

    def list_available_speakers(self) -> list:
        try:
            return self.tts.speakers
        except AttributeError:
            return []

    def _is_multilingual(self) -> bool:
        try:
            if hasattr(self.tts.synthesizer.tts_model, "language_manager") and self.tts.synthesizer.tts_model.language_manager:
                return self.tts.synthesizer.tts_model.language_manager.num_languages > 1
        except AttributeError:
            return "multilingual" in self.model_name

    def synthesize_speech(self, text: str, speaker: str = None, file_path: str = "output.wav", **kwargs) -> str:
        if speaker is None:
            available_speakers = self.list_available_speakers()
            if available_speakers:
                speaker = available_speakers[0]  # default to the first speaker available
            else:
                raise ValueError("This model is multi-speaker but no speakers are available.")
        self.tts.tts_to_file(text=text, speaker=speaker, file_path=file_path, **kwargs)
        return file_path


class Flashcard:
    def __init__(self, front: str, back: str, tts_wrapper: TTSWrapper):
        self.front_text = front
        self.back_text = back
        self.tts = tts_wrapper
        
        # Spaced repetition parameters
        self.interval = 1
        self.ease_factor = 2.5
        self.repetitions = 0
        self.due_date = datetime.now()
        
        # Audio file paths
        self.front_audio = f"audio/front_{hash(front)}.wav"
        self.back_audio = f"audio/back_{hash(back)}.wav"
        
        # Generate front audio only
        self._generate_front_audio()

    def _generate_front_audio(self):
        """Generate TTS audio for front side only"""
        available_speakers = self.tts.list_available_speakers()
        if available_speakers:
            chosen_speaker = available_speakers[0]  # or select another speaker as needed
            self.tts.synthesize_speech(self.front_text, speaker=chosen_speaker, file_path=self.front_audio)
        else:
            raise ValueError("No available speakers to choose from!")
        
    def generate_back_audio(self):
        """Generate back audio if not exists"""
        if not os.path.exists(self.back_audio):
            self.tts.synthesize_speech(self.back_text, file_path=self.back_audio)

    def update_schedule(self, quality: int):
        if quality < 3:
            self.interval = 1
            self.repetitions = 0
        else:
            if self.repetitions == 0:
                self.interval = 1
            elif self.repetitions == 1:
                self.interval = 6
            else:
                self.interval = int(self.interval * self.ease_factor)
            
            self.ease_factor = max(1.3, self.ease_factor + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02)))
            self.repetitions += 1
        
        self.due_date = datetime.now() + timedelta(days=self.interval)

class SpacedRepetitionScheduler:
    def __init__(self):
        self.cards = []
    
    def add_card(self, card: Flashcard):
        self.cards.append(card)
    
    def get_due_cards(self):
        return [card for card in self.cards if card.due_date <= datetime.now()]
    
    def update_card(self, card: Flashcard, quality: int):
        card.update_schedule(quality)

class ReviewSession:
    def __init__(self, scheduler: SpacedRepetitionScheduler):
        self.scheduler = scheduler
    
    def start_session(self):
        due_cards = self.scheduler.get_due_cards()
        if not due_cards:
            print("No cards due for review today!")
            return
        
        random.shuffle(due_cards)
        print(f"Starting review session with {len(due_cards)} cards")
        
        for card in due_cards:
            self._present_card(card)
    
    def _present_card(self, card: Flashcard):
        print("\nFront Text:", card.front_text)
        print("Playing front audio...")
        
        input("Press Enter to reveal answer...")
        
        print("\nBack Text:", card.back_text)
        print("Generating and playing back audio...")
        card.generate_back_audio()  # Generate on demand
        
        while True:
            try:
                quality = int(input("Rate your recall (0-5 where 5=perfect): "))
                if 0 <= quality <= 5:
                    break
                print("Please enter a number between 0-5")
            except ValueError:
                print("Invalid input. Please enter a number.")
        
        self.scheduler.update_card(card, quality)

def main():
    print(TTSWrapper.list_available_models())
    model_name = "tts_models/en/vctk/vits"
    tts_wrapper = TTSWrapper(model_name=model_name, progress_bar=True)
    
    scheduler = SpacedRepetitionScheduler()
    
    cards = [
        Flashcard("Photosynthesis", "Process by which plants convert light energy to chemical energy", tts_wrapper),
        Flashcard("Mitochondria", "Powerhouse of the cell", tts_wrapper),
        Flashcard("Newton's First Law", "An object in motion stays in motion unless acted upon by an external force", tts_wrapper)
    ]
    
    for card in cards:
        scheduler.add_card(card)
    
    session = ReviewSession(scheduler)
    session.start_session()

if __name__ == "__main__":
    main()