#!/bin/bash

# Quick script to clone all systemframe repositories
# This is a convenience wrapper around clone_repos.sh

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Default to current directory, or you can set a custom path
TARGET_DIR="${1:-.}"

echo "Cloning all systemframe repositories to: $TARGET_DIR"
echo ""

"$SCRIPT_DIR/clone_repos.sh" \
    --no-forks \
    -d "$TARGET_DIR" \
    -p 8 \
    systemframe
