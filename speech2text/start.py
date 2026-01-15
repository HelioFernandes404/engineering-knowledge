#!/usr/bin/env python3
"""
Automated script: record system audio and transcribe automatically
Usage: python start.py [--duration SECONDS]
"""
import argparse
import os
import sys
from datetime import datetime
from src.audio_recorder import record_system_audio
from src.processor import process_input
from src.transcriber import ModelSize, DeviceType, ComputeType
from src.logger import logger


class Args:
    """Helper class for arguments"""

    def __init__(
        self,
        input_file: str,
        output_file: str,
        model: ModelSize,
        device: DeviceType,
        compute_type: ComputeType,
        keep_wav: bool,
    ) -> None:
        self.input = input_file
        self.output = output_file
        self.model = model
        self.device = device
        self.compute_type = compute_type
        self.keep_wav = keep_wav


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Automatic system audio recording and transcription"
    )

    parser.add_argument("--duration", "-d", type=int, default=30,
                        help="Recording duration in seconds (default: 30)")

    parser.add_argument("--model", "-m", default="large-v3",
                        choices=["tiny", "base", "small", "medium", "large-v3"],
                        help="Whisper model (default: large-v3)")

    parser.add_argument("--device", default="cpu",
                        choices=["cpu", "cuda"],
                        help="Processing device (default: cpu)")

    parser.add_argument("--compute-type", default="int8",
                        choices=["int8", "int8_float16", "float16", "float32"],
                        help="Quantization type (default: int8)")

    parser.add_argument("--keep-audio", action="store_true",
                        help="Keep audio file after transcription")

    parser.add_argument("--output-dir", default="output",
                        help="Directory to save files (default: output/)")

    args = parser.parse_args()

    # Create output directory if it doesn't exist
    os.makedirs(args.output_dir, exist_ok=True)

    # Generate filenames with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    audio_file = os.path.join(args.output_dir, f"audio_{timestamp}.wav")
    text_file = os.path.join(args.output_dir, f"transcription_{timestamp}.txt")

    logger.info("=" * 60)
    logger.info("AUTOMATIC RECORDING AND TRANSCRIPTION")
    logger.info("=" * 60)
    logger.info(f"Duration: {args.duration} seconds")
    logger.info(f"Model: {args.model}")
    logger.info(f"Saving to: {args.output_dir}/")
    logger.info("=" * 60)

    try:
        # Step 1: Record audio
        logger.info("STEP 1/2: Recording system audio...")
        success = record_system_audio(
            audio_file,
            duration=args.duration,
            sample_rate=16000
        )

        if not success:
            logger.error("Recording failed!")
            sys.exit(1)

        # Step 2: Transcribe
        logger.info("STEP 2/2: Transcribing audio...")

        # Create args object for processor
        proc_args = Args(
            input_file=audio_file,
            output_file=text_file,
            model=args.model,
            device=args.device,
            compute_type=args.compute_type,
            keep_wav=args.keep_audio
        )

        process_input(proc_args)

        # Show results
        logger.info("=" * 60)
        logger.success("PROCESSING COMPLETED!")
        logger.info("=" * 60)

        with open(text_file, 'r', encoding='utf-8') as f:
            transcription = f.read()

        logger.info(f"Transcription ({len(transcription.split())} words):")
        logger.info("-" * 60)
        logger.info(transcription)
        logger.info("-" * 60)

        logger.info("Saved files:")
        if args.keep_audio or os.path.exists(audio_file):
            logger.info(f"   Audio: {audio_file}")
        logger.info(f"   Text: {text_file}")

        logger.success("Process completed successfully!")

    except KeyboardInterrupt:
        logger.warning("Process interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
