# K9s Multi-Context Manager Makefile
# Simple workflow: just run `make run` and everything works

# Configuration
PROJECT_DIR := $(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))
PYTHON_SCRIPT := $(PROJECT_DIR)/fetch_k3s_config.py
TUNNEL_SCRIPT := $(PROJECT_DIR)/k9s-with-tunnel.sh
CONFIG_DIR := $(HOME)/.k9s-config
LOG_DIR := $(HOME)/.local/state/k9s

# Colors for output
RED := \033[0;31m
GREEN := \033[0;32m
YELLOW := \033[1;33m
NC := \033[0m # No Color

.PHONY: help run k9s tunnel-list tunnel-kill tunnel-kill-all clean logs config test

## help: Show this help message
help:
	@echo "$(GREEN)K9s Multi-Context Manager$(NC)"
	@echo ""
	@echo "Usage: make [target]"
	@echo ""
	@echo "Main command: $(YELLOW)make run$(NC) (sets up everything and starts)"
	@echo ""
	@echo "Targets:"
	@awk '/^##/ { \
		helpMessage = substr($$0, 4); \
		split(helpMessage, parts, ":"); \
		printf "  $(YELLOW)%-20s$(NC) %s\n", parts[1], parts[2]; \
	}' $(MAKEFILE_LIST)

## run: Start the project (auto-setup and run)
run:
	@echo "$(GREEN)Starting K9s Multi-Context Manager...$(NC)"
	@uv run python3 $(PYTHON_SCRIPT)

## k9s: Start k9s with tunnel verification
k9s:
	@echo "$(GREEN)Starting k9s...$(NC)"
	@bash $(TUNNEL_SCRIPT)

## tunnel-list: List all active SSH tunnels
tunnel-list:
	@bash $(TUNNEL_SCRIPT) list

## tunnel-kill: Kill tunnel for specific context (usage: make tunnel-kill CONTEXT=name)
tunnel-kill:
ifndef CONTEXT
	@echo "$(RED)Error: CONTEXT parameter required$(NC)"
	@echo "Usage: make tunnel-kill CONTEXT=your-context-name"
	@exit 1
endif
	@bash $(TUNNEL_SCRIPT) kill $(CONTEXT)

## tunnel-kill-all: Kill all SSH tunnels
tunnel-kill-all:
	@bash $(TUNNEL_SCRIPT) kill-all

## clean: Remove generated kubeconfig files
clean:
	@echo "$(YELLOW)Removing generated kubeconfig files...$(NC)"
	@rm -f $(PROJECT_DIR)/*.yml
	@echo "$(GREEN)✓ Cleaned generated files$(NC)"

## logs: Show k9s logs (tail -f)
logs:
	@echo "$(GREEN)Showing k9s logs...$(NC)"
	@echo "Log file: $(LOG_DIR)/k9s.log"
	@echo "Press Ctrl+C to exit"
	@tail -f $(LOG_DIR)/k9s.log

## config: Open config file in default editor
config:
	@if [ ! -f "$(CONFIG_DIR)/config.yaml" ]; then \
		echo "$(RED)Config file not found. Run 'make run' first.$(NC)"; \
		exit 1; \
	fi
	@$${EDITOR:-nano} $(CONFIG_DIR)/config.yaml

## test: Run all tests with uv
test:
	@echo "$(GREEN)Running tests...$(NC)"
	@uv run python -m pytest tests/ -v

# Default target
.DEFAULT_GOAL := run
