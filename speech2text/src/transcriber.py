from typing import Literal

from faster_whisper import WhisperModel
from .logger import logger

ModelSize = Literal["tiny", "base", "small", "medium", "large-v3"]
DeviceType = Literal["cpu", "cuda"]
ComputeType = Literal["int8", "int8_float16", "float16", "float32"]


def transcribe_audio(
    audio_path: str,
    model: ModelSize = "large-v3",
    device: DeviceType = "cpu",
    compute_type: ComputeType = "int8",
) -> str:
    """Transcribe audio to text in Portuguese using faster-whisper

    Args:
        audio_path: Audio file path
        model: Model size (tiny, base, small, medium, large-v3)
        device: Processing device (cpu or cuda)
        compute_type: Quantization type (int8, int8_float16, float16, float32)
    """
    try:
        # Adjust compute_type based on device
        if device == "cpu" and compute_type == "float16":
            logger.warning("float16 not optimal for CPU. Using int8.")
            compute_type = "int8"

        logger.info(f"Loading model {model} ({device.upper()}, {compute_type})...")
        model = WhisperModel(model, device=device, compute_type=compute_type)

        logger.info("Starting transcription in Portuguese...")
        segments, info = model.transcribe(
            audio_path,
            language="pt",
            beam_size=5,
            best_of=5,
            temperature=0.0,
            compression_ratio_threshold=2.4,
            no_speech_threshold=0.6,
            vad_filter=True,
            vad_parameters=dict(min_silence_duration_ms=500)
        )

        # Combine all segments into full text
        transcription = " ".join([segment.text for segment in segments])

        logger.info(f"Detected language: {info.language} (confidence: {info.language_probability:.2%})")

        return transcription.strip()
    except Exception as e:
        logger.error(f"Transcription error: {str(e)}")
        raise RuntimeError(f"Transcription error: {str(e)}")