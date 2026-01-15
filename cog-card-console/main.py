import torch
from TTS.api import TTS

class TTSWrapper:
    def __init__(self, model_name: str, progress_bar: bool = False, device: str = None):
        """
        Initialize the TTSWrapper with a chosen TTS model.
        
        Args:
            model_name (str): The name of the TTS model to load.
            progress_bar (bool): Whether to display a progress bar during model download.
            device (str): 'cuda' or 'cpu'. If None, the device will be determined automatically.
        """
        self.device = device if device is not None else self._get_device()
        self.model_name = model_name
        self.tts = self._initialize_tts(model_name, progress_bar)
    
    def _get_device(self) -> str:
        """
        Determine and return the device string.
        Returns:
            str: 'cuda' if GPU is available, otherwise 'cpu'.
        """
        return "cuda" if torch.cuda.is_available() else "cpu"
    
    def _initialize_tts(self, model_name: str, progress_bar: bool) -> TTS:
        """
        Load the TTS model with the given name and move it to the selected device.
        
        Args:
            model_name (str): TTS model name.
            progress_bar (bool): Whether to show a progress bar while downloading.
            
        Returns:
            TTS: The loaded TTS model.
        """
        tts_model = TTS(model_name=model_name, progress_bar=progress_bar).to(self.device)
        return tts_model

    @staticmethod
    def list_available_models() -> list:
        """
        List all available TTS model names.
        
        Returns:
            list: A list of available model names.
        """
        tts_instance = TTS()
        return tts_instance.list_models()

    def list_available_speakers(self) -> list:
        """
        List available speakers for the loaded TTS model.
        
        Returns:
            list: A list of speaker IDs (or names). If the model is not multi-speaker, returns an empty list.
        """
        try:
            return self.tts.speakers
        except AttributeError:
            return []

    def _is_multilingual(self) -> bool:
        """
        Determine if the loaded TTS model supports multiple languages.
        
        Returns:
            bool: True if the model is multi-lingual; otherwise, False.
        """
        # Try to check if the model has a language manager attribute.
        try:
            if hasattr(self.tts.synthesizer.tts_model, "language_manager") and self.tts.synthesizer.tts_model.language_manager:
                return self.tts.synthesizer.tts_model.language_manager.num_languages > 1
        except AttributeError:
            pass
        # If not explicitly detectable, infer from the model name.
        return "multilingual" in self.model_name

    def synthesize_speech(self, text: str, speaker: str = None, file_path: str = "output.wav", **kwargs) -> str:
        """
        Synthesize speech from text using the loaded TTS model.
        
        Args:
            text (str): The text to be synthesized.
            speaker (str): The speaker to use for synthesis.
            file_path (str): The output file path for the generated audio.
            **kwargs: Additional keyword arguments passed to tts.tts_to_file().
                      (Note: If your model is not multi-lingual, the 'language' key will be ignored.)
        
        Returns:
            str: The path to the saved audio file.
        """
        # If the model is not multi-lingual and 'language' is passed, remove it.
        if not self._is_multilingual() and 'language' in kwargs:
            kwargs.pop('language')
        self.tts.tts_to_file(text=text, speaker=speaker, file_path=file_path, **kwargs)
        return file_path

def main():
    # Print available models.
    print("Available TTS models:")
    available_models = TTSWrapper.list_available_models()
    print(available_models)
    
    # Define the model name for an English multi-speaker (non-multi-lingual) model.
    model_name = "tts_models/en/vctk/vits"
    tts_wrapper = TTSWrapper(model_name=model_name, progress_bar=False)
    
    # List available speakers.
    speakers = tts_wrapper.list_available_speakers()
    print("Available speakers:", speakers)
    
    # Define synthesis parameters.
    text = "This is synthesized English speech using Coqui TTS with an object-oriented design."
    speaker = "p225"  # Choose one of the available speaker IDs.
    output_file = "output.wav"
    
    # Synthesize and save speech.
    result_path = tts_wrapper.synthesize_speech(text=text, speaker=speaker, file_path=output_file, language="en")
    print(f"Synthesized speech saved to: {result_path}")

if __name__ == "__main__":
    main()
