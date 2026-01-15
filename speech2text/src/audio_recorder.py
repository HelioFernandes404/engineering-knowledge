from typing import Optional, Tuple, List, Any

import sounddevice as sd
import soundfile as sf
import numpy as np
from datetime import datetime
from .logger import logger


def list_audio_devices() -> List[Any]:
    """List all available audio devices"""
    logger.info("Available audio devices:")
    devices = sd.query_devices()
    for i, device in enumerate(devices):
        logger.info(f"  [{i}] {device['name']} (in: {device['max_input_channels']}, out: {device['max_output_channels']})")
    return devices


def find_monitor_device() -> Tuple[int, str]:
    """Find PulseAudio/PipeWire monitor device for system audio capture"""
    devices = sd.query_devices()

    # Look for monitor devices (system audio output)
    for i, device in enumerate(devices):
        name_lower = device['name'].lower()
        if ('monitor' in name_lower or 'loopback' in name_lower) and device['max_input_channels'] > 0:
            return i, device['name']

    # If no monitor found, return default input
    default_input = sd.query_devices(kind='input')
    return default_input['index'], default_input['name']


def record_system_audio(
    output_file: str,
    duration: int = 10,
    sample_rate: int = 16000,
    device: Optional[int] = None,
) -> bool:
    """Record system audio output (what's playing on your computer)

    Args:
        output_file: Path to save the recording (WAV format)
        duration: Recording duration in seconds
        sample_rate: Sample rate in Hz (16000 recommended for Whisper)
        device: Audio device index (None = auto-detect monitor)

    Returns:
        True if recording successful, False otherwise
    """
    try:
        if device is None:
            device, device_name = find_monitor_device()
            logger.info(f"Auto-detected device: {device_name}")
        else:
            device_name = sd.query_devices(device)['name']
            logger.info(f"Using device: {device_name}")

        logger.info(f"Recording system audio for {duration} seconds...")
        logger.debug(f"Sample rate: {sample_rate}Hz")

        # Record audio
        recording = sd.rec(
            int(duration * sample_rate),
            samplerate=sample_rate,
            channels=1,
            device=device,
            dtype='float32'
        )

        sd.wait()  # Wait until recording is finished

        # Save to file
        sf.write(output_file, recording, sample_rate)

        logger.success(f"Recording saved: {output_file}")
        return True

    except Exception as e:
        logger.error(f"Recording failed: {str(e)}")
        logger.info("Tip: Try listing devices with --list-devices to find the correct monitor device")
        return False


def record_microphone(output_file: str, duration: int = 10, sample_rate: int = 16000) -> bool:
    """Record from microphone

    Args:
        output_file: Path to save the recording (WAV format)
        duration: Recording duration in seconds
        sample_rate: Sample rate in Hz

    Returns:
        True if recording successful, False otherwise
    """
    try:
        logger.info(f"Recording from microphone for {duration} seconds...")
        logger.debug(f"Sample rate: {sample_rate}Hz")

        # Use default input device
        recording = sd.rec(
            int(duration * sample_rate),
            samplerate=sample_rate,
            channels=1,
            dtype='float32'
        )

        sd.wait()

        sf.write(output_file, recording, sample_rate)

        logger.success(f"Recording saved: {output_file}")
        return True

    except Exception as e:
        logger.error(f"Recording failed: {str(e)}")
        return False
