# syntax=docker/dockerfile:1
FROM python:3.10-slim AS builder

# Install system dependencies in a separate layer for better caching
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked \
    apt-get update && \
    apt-get install -y --no-install-recommends \
    git \
    openssh-client \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/app

# Configure SSH for git operations (using SSH mount)
RUN mkdir -p /root/.ssh && \
    chmod 700 /root/.ssh && \
    ssh-keyscan github.com >> /root/.ssh/known_hosts && \
    chmod 644 /root/.ssh/known_hosts

# Copy requirements first
COPY requirements.txt .

# Install dependencies with pip and SSH cache mounts
RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=ssh \
    pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy setup files for package installation (better caching when only source code changes)
COPY setup.py .
COPY README.rst .
COPY HISTORY.rst .

# Install package without source code first (dependencies only)
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --no-deps .

# Now copy source code and install with dependencies
COPY webhook_glpi/ webhook_glpi/
RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=ssh \
    pip install .

# Copy application files
COPY app.py .

# Production stage
FROM python:3.10-slim
WORKDIR /app
COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin
COPY --from=builder /usr/src/app/app.py .
COPY --from=builder /usr/src/app/webhook_glpi ./webhook_glpi

EXPOSE 5000
CMD ["python", "app.py"]