# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a lab environment for running Windows Server 2012 R2 in a Docker container, collecting Windows Event Logs via OpenTelemetry Collector, and storing them in a VictoriaLogs cluster running on K3S.

## Architecture

**Three-tier log collection system:**

1. **Windows Server 2012 R2 Container** (172.30.0.3)
   - Runs via dockurr/windows (KVM/QEMU)
   - OpenTelemetry Collector 0.88.0 (contrib) installed at `C:\OpenTelemetry\`
   - Service: `otelcol` (auto-start, Windows service)

2. **Network Bridge**
   - Windows container → Host Linux network
   - OTLP/HTTP endpoint: `http://192.168.100.12:31281/insert/opentelemetry/v1/logs`

3. **VictoriaLogs Cluster (K3S)**
   - Namespace: `logging`
   - Components: vlinsert (ingest), vlstorage (storage), vlselect (query)
   - NodePort 31281 exposes vlinsert externally

## Critical Compatibility Constraint

**OpenTelemetry Collector version MUST be 0.88.0 or earlier for Windows Server 2012 R2:**
- Go 1.21+ (used in OTEL 0.89+) does not support Windows Server 2012 R2
- Go 1.20 (used in OTEL 0.88.0) is the last compatible version
- Always use the **contrib** build for `windowseventlog` receiver support

## Common Commands

### Environment Management

```bash
# Start Windows Server container
docker-compose up -d

# Stop Windows Server (with graceful shutdown)
docker-compose down

# Access Windows via SSH
ssh -p 2222 docker@localhost  # password: admin

# Access via SSH and run commands
ssh -p 2222 docker@localhost "sc.exe query otelcol"
```

### OpenTelemetry Management (Windows)

```bash
# Check service status
ssh -p 2222 docker@localhost "sc.exe query otelcol"

# Start service
ssh -p 2222 docker@localhost "sc.exe start otelcol"

# Stop service
ssh -p 2222 docker@localhost "sc.exe stop otelcol"

# View process
ssh -p 2222 docker@localhost "tasklist | findstr otelcol"

# Check metrics endpoint (from host Linux)
curl http://172.30.0.3:8888/metrics | grep -E "sent_log_records|queue"

# Restart after config change
ssh -p 2222 docker@localhost "taskkill /F /IM otelcol-contrib.exe && sc.exe start otelcol"
```

### VictoriaLogs Management (K3S)

```bash
# Verify cluster status
kubectl get pods -n logging
kubectl get svc -n logging

# Check vlinsert logs (ingestion)
kubectl logs -n logging -l app=vlinsert --tail=50

# Check vlstorage logs (storage)
kubectl logs -n logging -l app=vlstorage --tail=50

# Port-forward for queries (vlselect)
kubectl port-forward -n logging svc/vlc-victoria-logs-cluster-vlselect 9471:9471

# Query logs via API
curl 'http://localhost:9471/select/logsql/query?query=host.name:DOCKERW*'

# Access web UI (after port-forward)
# http://localhost:9471/select/vmui/

# Check NodePort status
kubectl get svc vlinsert-external -n logging
```

### Troubleshooting

```bash
# Check Windows Event Log for OTEL errors
ssh -p 2222 docker@localhost "wevtutil qe Application /c:10 /rd:true /f:text /q:\"*[System[Provider[@Name='otelcol']]]\""

# Check Service Control Manager errors
ssh -p 2222 docker@localhost "wevtutil qe System /c:10 /rd:true /f:text /q:\"*[System[Provider[@Name='Service Control Manager'] and EventID=7023]]\""

# Verify network connectivity from Windows to K3S
# (from Windows container)
Test-NetConnection -ComputerName 192.168.100.12 -Port 31281

# Check VictoriaLogs ingestion errors
kubectl logs -n logging -l app=vlinsert --tail=100 | grep -i error

# Monitor OTEL metrics in real-time
watch -n 2 'curl -s http://172.30.0.3:8888/metrics | grep exporter_sent_log_records_total'
```

## Configuration Files

### OpenTelemetry Config (Inside Windows)

**Location:** `C:\OpenTelemetry\config.yaml`

**Key configuration points:**
- Use `logs_endpoint` (NOT `endpoint`) for otlphttp exporter to avoid path duplication
- Endpoint format: `http://192.168.100.12:31281/insert/opentelemetry/v1/logs`
- Receivers collect from: Application, System, Security Event Logs
- Batch size: 8192 logs, timeout 200ms
- Queue: 5000 logs, 10 workers
- Compression: gzip enabled

**After modifying config:**
1. Test manually first: `cd C:\OpenTelemetry && otelcol-contrib.exe --config config.yaml`
2. If valid, restart service: `sc.exe stop otelcol && sc.exe start otelcol`

### Docker Compose

**Location:** `./docker-compose.yaml`

**Critical settings:**
- Requires KVM support (`/dev/kvm`)
- RAM: 8GB, CPU: 4 cores, Disk: 80GB
- Volumes: `./win2012` (persistent VM), `./shared` (accessible in Windows as `C:\shared`)
- Stop grace period: 2 minutes (allows proper Windows shutdown)

## Network Architecture

```
Windows (172.30.0.3:8888 metrics)
    │
    ├─ OTLP/HTTP ──────────────────────────┐
    │                                       │
    └─ RDP (3389), SSH (2222), Web (8006)  │
                                            ▼
Host Linux (192.168.100.12)
    │
    └─ K3S NodePort 31281 ─────────────────┤
                                            │
K3S Cluster (namespace: logging)           │
    │                                       │
    ├─ vlinsert:9481 (ClusterIP) ◄─────────┘
    ├─ vlstorage (StatefulSet, PV 20Gi x2)
    └─ vlselect:9471 (ClusterIP, VMUI)
```

## SSH Access Pattern

All Windows management commands use SSH with sshpass pattern:
```bash
sshpass -p 'admin' ssh -p 2222 -o StrictHostKeyChecking=no docker@localhost "<command>"
```

Avoid interactive commands (`timeout /t`, input redirection) as they fail over SSH.

## Installation/Reinstallation Procedure

If OpenTelemetry needs to be reinstalled (documented in `OTEL_INSTALL_WIN2012R2.md`):

1. Download contrib 0.88.0: `otelcol-contrib_0.88.0_windows_amd64.tar.gz`
2. Extract using 7-Zip (Windows has 7-Zip at `C:\Program Files\7-Zip\7z.exe`)
3. Place in `C:\OpenTelemetry\`
4. Create `config.yaml` with K3S endpoint
5. Register as service: `sc.exe create otelcol ...`
6. Configure auto-restart on failure
7. Start service: `sc.exe start otelcol`

## Documentation Structure

- `README.md` - High-level overview, quick start commands
- `OTEL_INSTALL_WIN2012R2.md` - Complete OpenTelemetry installation guide
- `OTEL_CONFIGURACAO_ATUAL.md` - Current production configuration, detailed architecture, troubleshooting
- `CLAUDE.md` - This file (guidance for Claude Code instances)

## K3S Context Loading

Before running kubectl commands, ensure K3S context is loaded:
```bash
source ~/.zshrc  # Loads kubeconfig
kubectl cluster-info  # Verify connectivity
```

The K3S cluster runs on the host Linux machine (192.168.100.12).

## Common Issues

**Issue:** Service fails to start with error 1064
- **Cause:** Config syntax error or path duplication in OTLP endpoint
- **Fix:** Use `logs_endpoint` instead of `endpoint`, test config manually first

**Issue:** Logs not reaching VictoriaLogs
- **Symptom:** `unsupported path requested: "/insert/opentelemetry/v1/logs/v1/logs"` in vlinsert logs
- **Cause:** Path duplication when using `endpoint` parameter
- **Fix:** Use `logs_endpoint: http://192.168.100.12:31281/insert/opentelemetry/v1/logs`

**Issue:** Service stuck in STOP_PENDING
- **Fix:** `taskkill /F /IM otelcol-contrib.exe` then `sc.exe start otelcol`

**Issue:** Windows takes long to initialize
- **Expected:** 3-5 minutes for full boot
- **Wait for:** SSH port 2222 to become available

## Development Workflow

When working on this project:

1. Always verify Windows container is running: `docker ps | grep windows2012`
2. Check VictoriaLogs cluster health: `kubectl get pods -n logging`
3. Verify OpenTelemetry service: `ssh -p 2222 docker@localhost "sc.exe query otelcol"`
4. Monitor log flow: Check vlinsert logs for successful ingestion
5. Use port-forward to access VMUI for log verification

## Data Persistence

- **Windows VM disk:** `./win2012/` (80GB QCOW2 image)
- **VictoriaLogs storage:** K3S Persistent Volumes (20Gi per pod, 7-day retention)
- **Shared files:** `./shared/` maps to `C:\shared` inside Windows

Deleting `./win2012/` will reset Windows to initial state.

## Git Commit Guidelines

- **DO NOT** include Claude Code attribution in commit messages
- **DO NOT** add "Generated with Claude Code" or "Co-Authored-By: Claude"
- Write clear, descriptive commit messages focused on the changes made
- Use conventional commit format when appropriate (feat:, fix:, docs:, etc.)
- Keep commits focused and atomic (one logical change per commit)
- Use imperative mood in commit messages (e.g., "Add feature" not "Added feature")
