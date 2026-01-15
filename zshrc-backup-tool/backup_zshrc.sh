#!/bin/bash

# Script to backup and restore .zshrc configuration

BACKUP_DIR="$HOME/heliofernandes404/zshrc_config"
ZSHRC_PATH="$HOME/.zshrc"

# Create backup directory if it doesn't exist
mkdir -p "$BACKUP_DIR"

case "$1" in
    backup|b)
        if [[ ! -f "$ZSHRC_PATH" ]]; then
            echo "Error: .zshrc not found at $ZSHRC_PATH"
            exit 1
        fi
        
        TIMESTAMP=$(date +%Y%m%d_%H%M%S)
        BACKUP_FILE="$BACKUP_DIR/zshrc_backup_$TIMESTAMP"
        
        cp "$ZSHRC_PATH" "$BACKUP_FILE"
        cp "$ZSHRC_PATH" "$HOME/.zshrc.backup.$TIMESTAMP"
        
        echo "✅ .zshrc backed up to:"
        echo "   - $BACKUP_FILE"
        echo "   - $HOME/.zshrc.backup.$TIMESTAMP"
        ;;
        
    restore|r)
        if [[ -z "$2" ]]; then
            echo "Available backups:"
            ls -1t "$BACKUP_DIR"/zshrc_backup_* 2>/dev/null | head -10
            echo ""
            echo "Usage: $0 restore <backup_file>"
            echo "Example: $0 restore zshrc_backup_20250822_155435"
            exit 1
        fi
        
        BACKUP_FILE="$BACKUP_DIR/$2"
        if [[ ! -f "$BACKUP_FILE" ]]; then
            echo "Error: Backup file not found: $BACKUP_FILE"
            exit 1
        fi
        
        cp "$ZSHRC_PATH" "$HOME/.zshrc.backup.before_restore.$(date +%Y%m%d_%H%M%S)"
        cp "$BACKUP_FILE" "$ZSHRC_PATH"
        
        echo "✅ .zshrc restored from $2"
        echo "Previous .zshrc backed up as .zshrc.backup.before_restore.*"
        ;;
        
    list|l)
        echo "Available backups:"
        ls -1t "$BACKUP_DIR"/zshrc_backup_* 2>/dev/null | head -10
        ;;
        
    *)
        echo "Usage: $0 {backup|restore|list}"
        echo ""
        echo "Commands:"
        echo "  backup, b          - Create backup of current .zshrc"
        echo "  restore, r <file>  - Restore .zshrc from backup"
        echo "  list, l            - List available backups"
        echo ""
        echo "Examples:"
        echo "  $0 backup"
        echo "  $0 restore zshrc_backup_20250822_155435"
        echo "  $0 list"
        exit 1
        ;;
esac