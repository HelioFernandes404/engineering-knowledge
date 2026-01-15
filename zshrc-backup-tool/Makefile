.PHONY: backup restore list apply help

# Default target
help:
	@echo "Zsh Configuration Management"
	@echo ""
	@echo "Available commands:"
	@echo "  make backup    - Create backup of current .zshrc"
	@echo "  make restore   - Restore .zshrc from backup (interactive)"
	@echo "  make list      - List available backups"
	@echo "  make apply     - Apply backed up config (same as restore)"
	@echo "  make help      - Show this help message"

backup:
	@echo "Creating backup of .zshrc..."
	@./backup_zshrc.sh backup

restore:
	@echo "Available backups:"
	@./backup_zshrc.sh list
	@echo ""
	@echo "Enter backup filename to restore:"
	@read -p "Backup file: " backup_file; \
	if [ -n "$$backup_file" ]; then \
		./backup_zshrc.sh restore "$$backup_file"; \
	else \
		echo "No backup file specified."; \
	fi

apply: restore

list:
	@./backup_zshrc.sh list