import argparse
from typing import Optional
from src.audio_recorder import record_system_audio, record_microphone, list_audio_devices
from src.logger import logger
from datetime import datetime
import os


def main() -> None:
    parser = argparse.ArgumentParser(description="Record system audio or microphone")

    parser.add_argument("--mode", dest="mode", default="system",
                        choices=["system", "microphone", "mic"],
                        help="Recording mode: 'system' for PC output, 'microphone'/'mic' for mic input")

    parser.add_argument("--output", dest="output", default=None,
                        help="Output WAV file (default: recording_TIMESTAMP.wav)")

    parser.add_argument("--duration", dest="duration", type=int, default=10,
                        help="Recording duration in seconds (default: 10)")

    parser.add_argument("--sample-rate", dest="sample_rate", type=int, default=16000,
                        help="Sample rate in Hz (default: 16000, optimal for Whisper)")

    parser.add_argument("--device", dest="device", type=int, default=None,
                        help="Audio device index (use --list-devices to see options)")

    parser.add_argument("--list-devices", dest="list_devices", action="store_true",
                        help="List all available audio devices and exit")

    args = parser.parse_args()

    # List devices and exit if requested
    if args.list_devices:
        list_audio_devices()
        return

    # Generate default output filename if not provided
    if args.output is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        args.output = f"recording_{timestamp}.wav"

    # Ensure output directory exists
    output_dir = os.path.dirname(args.output)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Record based on mode
    try:
        if args.mode == "system":
            success = record_system_audio(
                args.output,
                duration=args.duration,
                sample_rate=args.sample_rate,
                device=args.device
            )
        else:  # microphone or mic
            success = record_microphone(
                args.output,
                duration=args.duration,
                sample_rate=args.sample_rate
            )

        if success:
            logger.success("Recording completed successfully!")
            logger.info(f"File: {args.output}")
            logger.info("Transcribe it with:")
            logger.info(f"   python main.py --input {args.output}")
        else:
            exit(1)

    except KeyboardInterrupt:
        logger.warning("Recording interrupted by user")
        exit(1)
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        exit(1)


if __name__ == "__main__":
    main()
