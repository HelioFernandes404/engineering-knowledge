# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python Flask webhook application that processes Alertmanager alerts and integrates with multiple external systems:
- **GLPI**: Creates problems/tickets for alert management  
- **Discord**: Sends alert notifications to Discord channels
- **Twilio**: Sends voice/SMS notifications for alerts
- **ServiceNow**: Creates incidents based on alert context

The application receives webhook POST requests from Prometheus Alertmanager and routes them to different endpoints (`/glpi`, `/discord`, `/twilio`) for processing.

## Architecture

- **Flask App** (`app.py`): Main application entry point with route handlers
- **Core Logic** (`webhook_glpi/scripts/`):
  - `glpi.py`: Main GLPI integration logic with fingerprinting and deduplication
  - `discord.py`: Discord webhook integration
  - `twilio.py`: Voice/SMS notification handling
  - `create_incident.py`: ServiceNow incident management
  - `utils.py`: Common utilities for GLPI API operations
  - `metrics.py`: Application metrics collection
- **Credentials** (`webhook_glpi/credential.py`, `webhook_glpi/utils.py`): API token and configuration management

## Key Features

- **Alert Fingerprinting**: Generates SHA256 fingerprints from alert metadata to prevent duplicates
- **Multi-entity Support**: Handles different GLPI entities based on alert labels
- **Auto-resolution**: Automatically closes GLPI problems when alerts resolve
- **Feature Flags**: Uses ServiceNow context evaluation for conditional processing
- **Metrics Collection**: Tracks problems created, notifications sent, and errors

## Development Commands

### Installation
```bash
pip install -r requirements.txt
pip install -e .
```

### Running the Application
```bash
# Development server
python app.py

# Flask development server
export FLASK_APP=app.py
flask run --host=0.0.0.0 --port=5000

# Docker
docker-compose up
```

### Testing
```bash
# Install test dependencies
pip install pytest pytest-cov

# Run tests (if present)
pytest
```

### Linting
```bash
# Install dev dependencies
pip install flake8

# Run linting
flake8
```

### Docker Build
```bash
docker build --build-arg SSH_PRIVATE_KEY="$SSH_PRIVATE_KEY" -t webhooks-alertmanager .
```

## Configuration

- Credentials stored in `webhook_glpi/credentials.json` (use `credentials-example.json` as template)
- Environment variables can be set in `.env` file for Docker deployment
- GLPI entity mapping handled dynamically based on alert labels

## Deployment

- GitHub Actions workflow (`.github/workflows/deploy.yaml`) automatically builds and pushes to AWS ECR
- Deployment triggered on pushes to `main` branch or git tags
- Uses multi-stage Docker build for optimized runtime image