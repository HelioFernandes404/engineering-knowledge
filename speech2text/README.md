# Speech2text - Faster Whisper

High-performance audio transcription using faster-whisper (up to 4x faster than standard Whisper).

## Features
- **Record system audio** (capture PC output) or microphone
- Convert audio (MP3/WAV) to text with optimal speed
- CPU optimized with int8 quantization
- GPU support with float16
- Automatic audio resampling to 16kHz

## Stack
- Python + faster-whisper (CTranslate2)
- ffmpeg for audio conversion
- Ubuntu

## Installation

### Using uv (recommended)
```bash
git clone git@github.com:HelioFernandes404/speech2text.git
cd speech2text

# Install uv if not already installed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create virtual environment and install dependencies
uv venv
uv pip install -e ".[dev]"
```

### Using pip
```bash
git clone git@github.com:HelioFernandes404/speech2text.git
cd speech2text
pip install -r requirements.txt

# For development
pip install -r requirements-dev.txt
```

### System dependencies
```bash
# Ubuntu/Debian
sudo apt-get install ffmpeg portaudio19-dev
```

## Usage

### 1. Record Audio

```bash
# Record system audio (what's playing on PC)
python record.py --mode system --duration 30

# Record from microphone
python record.py --mode microphone --duration 10

# List available audio devices
python record.py --list-devices

# Record with custom device and output
python record.py --mode system --device 5 --output my_recording.wav --duration 60
```

### 2. Transcribe Audio

```bash
# Basic transcription (CPU, int8)
python main.py --input audio.mp3 --output transcription.txt

# GPU with float16
python main.py --input audio.mp3 --device cuda --compute-type float16

# Options
--model         # Model size: tiny, base, small, medium, large-v3 (default)
--device        # cpu or cuda
--compute-type  # int8 (CPU), float16 (GPU), int8_float16, float32
--keep-wav      # Keep WAV file after conversion
```

### 3. Automated Workflow (Record + Transcribe)

```bash
# Automatic: record system audio and transcribe
python start.py --duration 30 --model large-v3

# With custom output directory
python start.py --duration 60 --output-dir ./recordings --keep-audio

# Options
--duration      # Recording duration in seconds (default: 30)
--model         # Whisper model (default: large-v3)
--device        # cpu or cuda (default: cpu)
--compute-type  # int8, float16, etc. (default: int8)
--keep-audio    # Keep audio file after transcription
--output-dir    # Output directory (default: output/)
```

### 4. Manual Workflow

```bash
# Record + Transcribe step by step
python record.py --mode system --duration 30 --output meeting.wav
python main.py --input meeting.wav --output meeting.txt
```

## Project Structure
```bash
.
├── src/
│   ├── audio_converter.py    # MP3→WAV conversion
│   ├── audio_recorder.py     # System/microphone recording
│   ├── processor.py          # Main workflow orchestration
│   ├── transcriber.py        # Faster-whisper integration
│   └── logger.py             # Structured logging (loguru)
├── tests/
│   ├── test_audio_converter.py
│   └── test_audio_recorder.py
├── main.py                   # CLI for transcription
├── record.py                 # CLI for audio recording
├── start.py                  # Automated workflow (record + transcribe)
├── requirements.txt          # Production dependencies
├── requirements-dev.txt      # Development dependencies
├── pyproject.toml            # Modern Python project configuration
└── README.md
```

## Performance Tips
- **CPU**: Use int8 quantization (default)
- **GPU**: Use float16 for small/medium models
- **Large models**: May be slower on GPU (3x) vs CPU
- **Audio**: Automatically resampled to 16kHz mono

## Recording Tips (Linux)
- **System audio**: Uses PulseAudio/PipeWire monitor device
- **If recording fails**: Run `python record.py --list-devices` to find monitor device
- **Monitor device**: Usually has "monitor" or "loopback" in the name
- **Sample rate**: 16kHz is optimal for Whisper (smaller files, same accuracy)

## Development

### Running tests
```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=src --cov-report=html

# Run specific test file
uv run pytest tests/test_audio_converter.py
```

### Code quality
```bash
# Lint with ruff
uv run ruff check .

# Format code
uv run ruff format .

# Type checking with mypy
uv run mypy src/
```

### CI/CD
The project includes GitHub Actions workflows that automatically:
- ✅ Run linting and formatting checks
- ✅ Execute type checking with mypy
- ✅ Run tests across Python 3.10, 3.11, 3.12
- ✅ Generate coverage reports

## Recent Improvements
- ✨ Migrated to modern `pyproject.toml` configuration
- 🔧 Added comprehensive type hints with `typing` module
- 📊 Implemented structured logging with loguru
- 🧪 Improved test coverage with mocks
- 🌍 Standardized codebase to 100% English
- ⚡ Added CI/CD with GitHub Actions
- 📦 Support for `uv` package manager

