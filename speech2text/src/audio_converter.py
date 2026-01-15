import os
import subprocess

from .logger import logger


def converter_mp3_to_wav(input_mp3: str, output_wav: str) -> bool:
    """Converts MP3 file to WAV with optimized configuration for transcription"""
    try:
        if not os.path.exists(input_mp3):
            logger.error(f"File {input_mp3} not found!")
            return False

        logger.info("Converting MP3 to WAV...")

        cmd = [
            'ffmpeg',
            '-i', input_mp3,
            '-ar', '16000',
            '-ac', '1',
            '-acodec', 'pcm_s16le',
            '-loglevel', 'error',
            '-y',
            output_wav
        ]

        subprocess.run(cmd, check=True, capture_output=True, text=True)
        logger.success(f"Conversion completed: {output_wav} (16kHz, mono, 16-bit)")
        return True

    except subprocess.CalledProcessError as e:
        logger.error(f"Error in conversion:\n{e.stderr}")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")

    return False


def verify_audio(wav_path: str) -> bool:
    """Verify the properties of the generated WAV file"""
    try:
        if not os.path.exists(wav_path):
            logger.error(f"WAV file not found: {wav_path}")
            return False

        logger.info("Verifying WAV file...")
        cmd = [
            'ffprobe',
            '-v', 'error',
            '-show_entries', 'stream=sample_rate,channels,bits_per_sample',
            '-of', 'default=noprint_wrappers=1',
            wav_path
        ]
        resultado = subprocess.run(cmd, capture_output=True, text=True, check=True)
        logger.debug(resultado.stdout)
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Error verifying audio: {e.stderr}")
        return False
    except Exception as e:
        logger.error(f"Error during checking: {str(e)}")
        return False