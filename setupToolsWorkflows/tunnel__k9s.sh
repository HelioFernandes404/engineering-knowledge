#!/bin/bash

# Improved k8s tunnel setup script with better error handling and auto-launch k9s
# Now without kubectl dependency

# Configuration
REMOTE_HOST="granado-linux-cd"
LOCAL_KUBECONFIG="${HOME}/.kube/config"
REMOTE_KUBECONFIG="/etc/rancher/k3s/k3s.yaml"
PID_FILE="/tmp/k8s-tunnel.pid"
LOG_FILE="/tmp/k8s-tunnel.log"
SSH_PORT=22  # Default SSH port, change if needed
TUNNEL_PORT=6443
K9S_TIMEOUT=5  # Seconds to wait for tunnel before launching k9s

# Colors for better output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

function cleanup() {
    echo -e "${YELLOW}Cleaning up...${NC}"
    if [[ -f "${PID_FILE}" ]]; then
        local pid=$(cat "${PID_FILE}")
        if ps -p "${pid}" > /dev/null; then
            echo -e "Stopping tunnel (PID: ${pid})..."
            kill "${pid}" 2>/dev/null && rm -f "${PID_FILE}"
        else
            rm -f "${PID_FILE}"
        fi
    fi
    
    # Kill any orphaned SSH processes
    pkill -f "ssh -N -L ${TUNNEL_PORT}:localhost:${TUNNEL_PORT} ${REMOTE_HOST}" 2>/dev/null
}

function check_dependencies() {
    local missing=()
    for cmd in ssh scp sed k9s; do
        if ! command -v "${cmd}" >/dev/null 2>&1; then
            missing+=("${cmd}")
        fi
    done
    
    if [[ ${#missing[@]} -gt 0 ]]; then
        echo -e "${RED}Missing dependencies:${NC} ${missing[*]}"
        exit 1
    fi
}

function is_port_open() {
    local port=$1
    local timeout=1  # second
    
    # Try different methods depending on available commands
    if command -v nc >/dev/null; then
        if nc -z -w "$timeout" localhost "$port"; then
            return 0
        fi
    elif command -v bash >/dev/null; then
        if bash -c "echo >/dev/tcp/localhost/$port" &>/dev/null; then
            return 0
        fi
    fi
    
    return 1
}

function setup_tunnel() {
    echo -e "${YELLOW}Copying kubeconfig from ${REMOTE_HOST}...${NC}"
    if ! scp -P "${SSH_PORT}" "${REMOTE_HOST}:${REMOTE_KUBECONFIG}" "${LOCAL_KUBECONFIG}"; then
        echo -e "${RED}Failed to copy kubeconfig${NC}"
        exit 1
    fi

    # Modify the server address in the kubeconfig (cross-platform sed)
    if sed -i'.bak' -e "s|server: https://127.0.0.1:${TUNNEL_PORT}|server: https://localhost:${TUNNEL_PORT}|" "${LOCAL_KUBECONFIG}" 2>/dev/null; then
        rm -f "${LOCAL_KUBECONFIG}.bak"
    elif sed -i '' "s|server: https://127.0.0.1:${TUNNEL_PORT}|server: https://localhost:${TUNNEL_PORT}|" "${LOCAL_KUBECONFIG}"; then
        # macOS fallback
        true
    else
        echo -e "${RED}Failed to modify kubeconfig${NC}"
        exit 1
    fi

    echo -e "${YELLOW}Setting up SSH tunnel...${NC}"
    if ! ssh -N -f -L "${TUNNEL_PORT}:localhost:${TUNNEL_PORT}" "${REMOTE_HOST}" -p "${SSH_PORT}" >"${LOG_FILE}" 2>&1; then
        echo -e "${RED}Failed to establish SSH tunnel.${NC}"
        echo -e "Check if port ${TUNNEL_PORT} is already in use or check ${LOG_FILE} for details."
        exit 1
    fi

    # Get and store PID
    pgrep -f "ssh -N -L ${TUNNEL_PORT}:localhost:${TUNNEL_PORT} ${REMOTE_HOST}" > "${PID_FILE}"
    echo -e "${GREEN}Tunnel is running in background (PID: $(cat "${PID_FILE}"))${NC}"
}

function launch_k9s() {
    echo -e "${YELLOW}Waiting for tunnel to stabilize...${NC}"
    local attempts=0
    while ! is_port_open "${TUNNEL_PORT}" && [[ ${attempts} -lt ${K9S_TIMEOUT} ]]; do
        sleep 1
        ((attempts++))
    done

    if is_port_open "${TUNNEL_PORT}"; then
        echo -e "${GREEN}Launching k9s...${NC}"
        k9s
    else
        echo -e "${RED}Failed to establish tunnel connection. Check ${LOG_FILE} for details.${NC}"
        cleanup
        exit 1
    fi
}

# Main execution
check_dependencies

# Handle --stop argument
if [[ "$1" == "--stop" ]]; then
    cleanup
    exit 0
fi

# Clean up any existing tunnel
cleanup

# Set up new tunnel
setup_tunnel

# Auto-launch k9s
launch_k9s

# Instructions
echo -e "\nTo stop the tunnel, run: ${YELLOW}$0 --stop${NC}"