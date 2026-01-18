#!/bin/bash
#
# init.sh - Initialize k9s-config project
#
# DESCRIPTION:
#   Sets up Python virtual environment and installs dependencies for the k9s-config project.
#   Optionally runs the main fetch_k3s_config.py script immediately after setup.
#
# USAGE:
#   ./init.sh               # Setup venv and run fetch script
#   source venv/bin/activate && python3 fetch_k3s_config.py  # Manual approach
#
# FEATURES:
#   - Creates isolated Python virtual environment (.venv)
#   - Installs all dependencies from requirements.txt
#   - Upgrades pip to latest version
#   - Runs fetch_k3s_config.py to fetch first kubeconfig
#
# ENVIRONMENT:
#   PROJECT_DIR: Detected automatically as script directory
#   VENV_DIR: Default .venv (can be modified below if needed)
#
# REQUIREMENTS:
#   - Python 3.8+
#   - pip (bundled with Python)
#
# EXIT CODES:
#   0: Success
#   1: Error (set -e enables this behavior)

set -e  # Exit immediately on any error

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$PROJECT_DIR/venv"
PYTHON_SCRIPT="$PROJECT_DIR/fetch_k3s_config.py"

echo "=== K3s Config Fetcher Setup ==="
echo "Project directory: $PROJECT_DIR"

# Create virtual environment if it doesn't exist
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment at $VENV_DIR..."
    python3 -m venv "$VENV_DIR"
else
    echo "Virtual environment already exists at $VENV_DIR"
fi

# Activate virtual environment
echo "Activating virtual environment..."
source "$VENV_DIR/bin/activate"

# Upgrade pip to latest version
echo "Upgrading pip..."
pip install --upgrade pip -q

# Install all dependencies
echo "Installing dependencies from requirements.txt..."
pip install -r "$PROJECT_DIR/requirements.txt" -q

# Create default config directory and copy example config
echo "Setting up configuration..."
CONFIG_DIR="$HOME/.k9s-config"
if [ ! -d "$CONFIG_DIR" ]; then
    mkdir -p "$CONFIG_DIR"
    if [ -f "$PROJECT_DIR/.k9s-config-example/config.yaml" ]; then
        cp "$PROJECT_DIR/.k9s-config-example/config.yaml" "$CONFIG_DIR/config.yaml"
        echo "Created default config at $CONFIG_DIR/config.yaml"
    fi
else
    echo "Config directory already exists at $CONFIG_DIR"
fi

# Create log directory for k9s-config
LOG_DIR="$HOME/.local/state/k9s"
if [ ! -d "$LOG_DIR" ]; then
    mkdir -p "$LOG_DIR"
    echo "Created log directory at $LOG_DIR"
fi

# Only run the script if SKIP_FETCH is not set
if [ -z "${SKIP_FETCH:-}" ]; then
    echo ""
    echo "Running fetch_k3s_config.py..."
    python3 "$PYTHON_SCRIPT"
fi

echo ""
echo "=== Setup Complete ==="
echo ""
echo "Next steps:"
echo "  1. Add inventory files to inventory/ directory"
echo "  2. Edit your config: $CONFIG_DIR/config.yaml"
echo "  3. Add cluster: make add-cluster (or: python3 fetch_k3s_config.py)"
echo "  4. Launch k9s: make k9s (or: $PROJECT_DIR/k9s-with-tunnel.sh)"
echo ""
echo "To view logs: make logs (or: tail -f $LOG_DIR/k9s-config.log)"
echo "To list tunnels: make tunnel-list (or: $PROJECT_DIR/k9s-with-tunnel.sh list)"
echo ""
echo "For all commands: make help"
echo "For config details: $PROJECT_DIR/docs/CONFIG.md"
