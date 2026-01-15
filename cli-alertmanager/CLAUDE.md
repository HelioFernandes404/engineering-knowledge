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

- **Flask App** (`app.py`): Main application entry point with route handlers and global exception handling
- **Core Logic** (`webhook_glpi/scripts/`):
  - `glpi.py`: Main GLPI integration logic with fingerprinting and deduplication
  - `discord.py`: Discord webhook integration
  - `twilio.py`: Voice/SMS notification handling
  - `create_incident.py`: ServiceNow incident management with LaunchDarkly feature flags
  - `utils.py`: Common utilities for GLPI API operations (authentication, entity lookups, problem management)
  - `metrics.py`: OpenTelemetry metrics via `sf_common.metrics.MetricManager`
  - `config.py`: Centralized configuration and LaunchDarkly client initialization
- **Credentials** (`webhook_glpi/credential.py`, `webhook_glpi/utils.py`): API token and configuration retrieval

## Key Features

- **Alert Fingerprinting**: Generates SHA256 fingerprints from alert metadata to prevent duplicates
  - Fingerprint stored in GLPI problem content and used for lookups
  - Redis-backed memoization cache (`@m.redis()`) for duplicate detection
- **Multi-entity Support**: Handles different GLPI entities based on alert labels
  - Dynamic entity resolution via `get_entities_name()` and `get_sub_entities()`
- **Auto-resolution**: Automatically closes GLPI problems when alerts resolve
  - Status `5` (solved) + solution with resolved timestamp
- **Feature Flags**: Uses LaunchDarkly for conditional ServiceNow incident creation
  - Context-based evaluation (customer, incident availability)
- **Metrics Collection**: OpenTelemetry counters via `sf_common` package
  - Tracks: problems created, notifications sent, app lifecycle, crashes, errors

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

# With Docker Compose (includes redis, otel-collector, victoriametrics)
docker-compose up

# Build Docker image (requires SSH key for private dependencies)
DOCKER_BUILDKIT=1 docker build --ssh default -t webhooks-alertmanager .
```

### Testing
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=webhook_glpi --cov-report=html

# Run specific test markers
pytest -m unit          # Unit tests only
pytest -m integration   # Integration tests only
pytest -m "not slow"    # Skip slow tests

# Run single test file
pytest tests/test_glpi.py

# Run with verbose output
pytest -v
```

### Linting
```bash
# Check code style
flake8

# Check type hints (Pylance diagnostics in editor)
# Uses type annotations throughout glpi.py and utils.py
```

## Configuration

### Credentials Management
- Credentials stored in `webhook_glpi/credentials.json` (use `credentials-example.json` as template)
- Environment variables loaded via `.env` file (see `webhook_glpi/scripts/config.py`)
- GLPI entity mapping handled dynamically based on alert labels

### Key Environment Variables
- `FATAL_ON_ERROR`: Controls whether unhandled exceptions terminate the process (default: `true`)
- `LAUNCHDARKLY_SDK_KEY`: Feature flag management (ServiceNow incident creation)
- `SERVICENOW_INSTANCE`, `SERVICENOW_API_KEY`: ServiceNow integration credentials
- Redis connection for memoization cache (default: `localhost:6379`)

### Infrastructure Dependencies
- **Redis**: Required for `memoizit` caching (fingerprint deduplication)
- **OpenTelemetry Collector**: Optional metrics export (OTLP protocol on ports 4317/4318)
- **VictoriaMetrics**: Optional metrics storage and querying (port 8428)

## Error Handling & Fatal Behavior

The application has configurable error handling via `FATAL_ON_ERROR`:
- When `true` (default): Unhandled exceptions increment `app_crash_counter`, flush logs for 15s, then exit with code 1
- When `false`: Returns 500 JSON response but continues running
- Prevents zombie containers in Kubernetes/ECS that fail silently

## Deployment

### CI/CD Workflows
- `.github/workflows/deploy-main.yaml`: Auto-deploys to AWS ECR on pushes to `main` branch
  - Uses Commitizen to auto-bump version and create git tags
  - Builds multi-stage Docker image with BuildKit cache (S3)
- `.github/workflows/deploy-tag.yaml`: Deploys on manual git tags
- `.github/workflows/test.yaml`: Runs pytest on pull requests

### Docker Build Notes
- Multi-stage build: builder stage (with git/ssh) → slim production image
- Requires SSH key for private dependency: `sf_common @ git+ssh://git@github.com/systemframe/systemframe-common.git`
- Use `--ssh default` flag and ensure SSH agent has the key loaded

## Working with the Codebase

### Alert Processing Flow
1. Alertmanager sends POST request to `/glpi`, `/discord`, or `/twilio` endpoint
2. Request handler extracts alerts from JSON payload
3. For each alert:
   - Generate fingerprint from labels/annotations (`generate_fingerprint()`)
   - Check if problem already exists in GLPI (`get_problem_by_fingerprint()`)
   - If alert is `resolved`: close existing problem (`close_problem()`)
   - If alert is `firing` and new: create GLPI problem with formatted content
4. Optionally create ServiceNow incident if feature flag enabled
5. Return JSON response with created problem IDs

### GLPI API Integration Patterns
- Authentication: Session-based with `App-Token` + `user_token` → `Session-Token`
- All GLPI operations in `utils.py` follow pattern: `get_auth_token()` → API call → return data
- Entity resolution: SF ID (from alert labels) → DynamoDB lookup → GLPI entity ID
- Memoization: Heavy use of `@m.redis()` decorator for caching expensive lookups

### Adding New Alert Handlers
1. Create handler function in `webhook_glpi/scripts/` (e.g., `my_service.py`)
2. Add route in `app.py`: `@app.route('/my-service', methods=['POST'])`
3. Parse alert payload and call your handler
4. Add metrics counters in `metrics.py` if tracking needed
5. Update CLAUDE.md with new endpoint documentation

## Git Conventions

### Commit Messages

**Format:** Use conventional commits without AI attribution signatures

```
<type>: <description>

<detailed explanation if needed>
```

**Do NOT include:**
- Generated by Claude Code signatures
- Co-Authored-By lines for AI tools
- AI attribution footers

**Why:** Maintains clean commit history that represents human authorship and intentionality

**Example (Good):**
```
fix: fix GLPI fingerprint custom field API integration with configurable container ID

Previously, the fingerprint was not being stored correctly because:
1. The API endpoint required plugin_fields_containers_id parameter
2. The function used POST when it should only create new records
3. The container ID was hardcoded

Changes:
- Add GLPI_FINGERPRINT_CONTAINER_ID as configurable environment variable
- Fix update_problem_fingerprint() to properly create records
- Include plugin_fields_containers_id in the API request payload
```

**Example (Bad):**
```
🤖 Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>
```