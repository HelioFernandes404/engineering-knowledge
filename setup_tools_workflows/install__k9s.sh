#!/bin/bash

# K9s Auto-Installer for Ubuntu/Debian
# Usage: ./install_k9s.sh

set -e  # Exit on error

echo "🔹 Installing K9s Kubernetes CLI..."

# Check if running as root
if [ "$(id -u)" -eq 0 ]; then
  echo "❌ Do not run this script as root! Run as a normal user."
  exit 1
fi

# Install dependencies (curl, tar)
echo "🔹 Installing required dependencies..."
sudo apt update && sudo apt install -y curl tar

# Download latest K9s binary
echo "🔹 Downloading K9s..."
K9S_LATEST_URL="https://github.com/derailed/k9s/releases/latest/download/k9s_Linux_amd64.tar.gz"
curl -sSL "$K9S_LATEST_URL" -o k9s.tar.gz

# Extract and move binary
echo "🔹 Installing K9s to /usr/local/bin (requires sudo)..."
tar -xzf k9s.tar.gz k9s
sudo mv k9s /usr/local/bin/
rm k9s.tar.gz  # Cleanup

# Verify installation
if command -v k9s &>/dev/null; then
  echo "✅ K9s installed successfully!"
  echo "ℹ️ Version: $(k9s version)"
else
  echo "❌ Installation failed. Check logs above."
  exit 1
fi

# Add ~/.local/bin to PATH (if not already present)
if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
  echo "🔹 Adding ~/.local/bin to PATH..."
  echo 'export PATH="$PATH:$HOME/.local/bin"' >> ~/.bashrc
  source ~/.bashrc
  echo "ℹ️ PATH updated. Restart your shell or run 'source ~/.bashrc'."
fi

echo "🎉 Done! Run 'k9s' to start."
