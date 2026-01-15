# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

InfranGen is a Python-based system metrics collection and observability platform built using hexagonal architecture (ports and adapters pattern). The application collects system metrics (CPU, memory, disk, network) and exports them via multiple channels: Prometheus metrics endpoint, OpenTelemetry (OTLP), VictoriaLogs, and JSON files.

## Architecture

The codebase follows hexagonal architecture with strict separation of concerns:

- **Domain Layer** (`src/domain/`): Core business logic, framework-agnostic
  - `models.py`: Data models (SystemMetrics, ApplicationMetrics, MetricsSnapshot)
  - `services.py`: MetricsService orchestrates collection and export workflows
  - `types.py`: Type definitions and custom types

- **Ports** (`src/ports/`): Interfaces defining contracts between layers
  - `config_port.py`: Configuration abstraction
  - `metrics_collector_port.py`: Metrics collection interface
  - `metrics_exporter_port.py`: Generic export interface
  - `otlp_exporter_port.py`: OpenTelemetry export interface

- **Adapters** (`src/adapters/`): Concrete implementations of ports
  - **Input Adapters** (`input/`):
    - `cli_adapter.py`: Command-line interface, handles `--once` mode and continuous mode with signal handling
    - `http_server_adapter.py`: HTTP server exposing `/metrics` (Prometheus) and `/health` endpoints
  - **Output Adapters** (`out/`):
    - `config_adapter.py`: Environment variable-based configuration
    - `system_metrics_adapter.py`: System metrics collection via psutil
    - `prometheus_metrics_adapter.py`: Prometheus metrics exposition
    - `otlp_exporter_adapter.py`: OpenTelemetry OTLP gRPC exporter
    - `victorialogs_adapter.py`: VictoriaLogs integration for structured logging

## Application Flow

1. **main.py** wires dependencies: ConfigAdapter → SystemMetricsAdapter → PrometheusMetricsAdapter → OTLPExporterAdapter → MetricsService → CLIAdapter
2. **CLIAdapter** starts HTTPServerAdapter (continuous mode) or runs once (`--once` flag)
3. **MetricsService** collects metrics on interval, updates Prometheus gauges, exports to OTLP if enabled
4. **HTTPServerAdapter** serves Prometheus metrics at `:8000/metrics` (configurable via `METRICS_SERVER_PORT`)

## Development Commands

### Environment Setup
```bash
# Create and activate virtual environment
make venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Running Locally
```bash
# Continuous mode (default) - runs HTTP server on :8000 with /metrics and /health endpoints
python main.py

# One-shot mode - collect once and exit
python main.py --once
```

### Docker
```bash
# Build and run
docker build -t infragen:latest .
docker run infragen:latest

# Or use docker-compose (includes full stack: app, VictoriaMetrics, VMAgent, VictoriaLogs, OTLP collector)
docker-compose up
```

### Kubernetes
```bash
# Deploy to Kubernetes (includes VictoriaMetrics stack)
kubectl apply -f InfranGen.yaml
kubectl get pods -n monitoring

# Access VictoriaMetrics UI
kubectl port-forward -n monitoring svc/victoriametrics 8428:8428
# Then visit http://localhost:8428

# The application also supports Helm deployment (see kubernetes/ directory)
# - kubernetes/default/values.yaml: Default Helm values
# - kubernetes/vmstack/vmstack-values.yaml: VictoriaMetrics stack configuration
# - kubernetes/custom/vm-operator-values.yaml: Custom VictoriaMetrics operator values
```

## Configuration

Environment variables (see `.env.example`):

**Application Settings:**
- `APP_NAME`, `APP_VERSION`, `ENVIRONMENT`: Application metadata
- `METRICS_INTERVAL_SECONDS`: Collection interval for continuous mode (default: 60)
- `METRICS_SERVER_PORT`: HTTP server port (default: 8000)

**Metrics Collection:**
- `COLLECT_CPU_METRICS`, `COLLECT_MEMORY_METRICS`, `COLLECT_DISK_METRICS`, `COLLECT_NETWORK_METRICS`: Enable/disable specific collectors

**Observability Integrations:**
- `ENABLE_OTLP`: Enable OpenTelemetry export (default: false)
- `OTEL_EXPORTER_OTLP_ENDPOINT`: OTLP collector endpoint (default: http://localhost:4317)
- `ENABLE_VICTORIALOGS`: Enable VictoriaLogs integration (default: false)
- `VICTORIALOGS_URL`: VictoriaLogs endpoint (default: http://localhost:9428)

**Logging:**
- `LOG_LEVEL`: Logging level (INFO, DEBUG, WARNING, ERROR)
- `LOG_FORMAT`: Log format (json or text)

## Key Dependencies

- `psutil`: System metrics collection
- `prometheus_client`: Prometheus metrics exposition
- `opentelemetry-*`: OpenTelemetry OTLP export
- `requests`: HTTP client for VictoriaLogs
- `python-dotenv`: Environment variable loading

## Observability Stack

The docker-compose and Kubernetes deployments include a complete observability stack:

- **Prometheus Metrics**: Exposed at `:8000/metrics`, scraped by VMAgent
- **VictoriaMetrics**: Time-series database for metrics storage (`:8428`)
- **VMAgent**: Prometheus scraper with remote write to VictoriaMetrics (`:8429`)
- **VictoriaLogs**: Structured log aggregation (`:9428`)
- **OTLP Collector**: OpenTelemetry collector for traces/metrics (`:4317` gRPC, `:13133` health)

## Git Commit Guidelines

When creating git commits for this repository:

- **DO NOT** add AI-generated signatures or co-authorship information
- **DO NOT** include footers like "🤖 Generated with [Claude Code]" or "Co-Authored-By: Claude <noreply@anthropic.com>"
- Keep commit messages clean and professional, following conventional commit format
- The repository should show only human contributors (Helio Fernandes)
- Focus on clear, concise commit messages that describe the changes made