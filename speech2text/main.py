import argparse
from src.processor import process_input
from src.logger import logger


def main() -> None:
    parser = argparse.ArgumentParser(description="Convert MP3 to text with faster-whisper")
    parser.add_argument("--input", required=True, help="Input file path (MP3/WAV)")
    parser.add_argument("--output", dest="output", default="transcription.txt", help="Output file for transcription")
    parser.add_argument("--model", dest="model", default="large-v3", help="Whisper model (tiny, base, small, medium, large-v3)")
    parser.add_argument("--device", dest="device", default="cpu", choices=["cpu", "cuda"], help="Processing device")
    parser.add_argument("--compute-type", dest="compute_type", default="int8",
                        choices=["int8", "int8_float16", "float16", "float32"],
                        help="Quantization type (int8 recommended for CPU, float16 for GPU)")
    parser.add_argument("--keep-wav", dest="keep_wav", action="store_true", help="Keep WAV file after conversion")
    
    args = parser.parse_args()

    try:
        process_input(args)
        logger.success(f"Transcription completed! Result saved to: {args.output}")
    except Exception as e:
        logger.error(f"Processing failed: {str(e)}")
        exit(1)
        

if __name__ == "__main__":
    main()