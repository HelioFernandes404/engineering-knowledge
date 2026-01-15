# TODO: double check on en-us
import os
from typing import Protocol

from .audio_converter import converter_mp3_to_wav, verify_audio
from .transcriber import transcribe_audio, ModelSize, DeviceType, ComputeType
from .logger import logger


class ProcessArgs(Protocol):
    """Protocol for process_input arguments"""

    input: str
    output: str
    model: ModelSize
    device: DeviceType
    compute_type: ComputeType
    keep_wav: bool


def process_input(args: ProcessArgs) -> None:
    """Main audio processing workflow"""
    # Verify input file
    if not os.path.exists(args.input):
        raise FileNotFoundError(f"File {args.input} not found!")

    path_audio = args.input
    wav_temp = None

    # Convert MP3 to WAV if necessary
    if args.input.lower().endswith(".mp3"):
        wav_temp = os.path.splitext(args.input)[0] + ".wav"
        if not converter_mp3_to_wav(args.input, wav_temp):
            raise RuntimeError("Failed to convert MP3 to WAV")
        verify_audio(wav_temp)
        path_audio = wav_temp
    # Transcribe audio
    text = transcribe_audio(path_audio, args.model, args.device, args.compute_type)

    # Save transcription
    with open(args.output, "w", encoding="utf-8") as f:
        f.write(text)

    # Clean temporary file
    if wav_temp and not args.keep_wav:
        try:
            os.remove(wav_temp)
            logger.info(f"Temporary file {wav_temp} removed")
        except Exception as e:
            logger.warning(f"Error removing temporary file: {str(e)}")
