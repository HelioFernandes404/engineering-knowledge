# -*- coding: utf-8 -*-
"""Configuration management for GLPI CLI.

Loads configuration from environment variables (priority) or config file.
"""
import os
from pathlib import Path
from typing import Optional
import yaml


class Config:
    """GLPI CLI configuration."""

    def __init__(self):
        """Initialize configuration from env vars or file."""
        self.url: Optional[str] = None
        self.app_token: Optional[str] = None
        self.user_token: Optional[str] = None
        self._load()

    def _load(self):
        """Load configuration with priority: env vars > config file."""
        # Try environment variables first (highest priority)
        self.url = os.getenv("GLPI_URL")
        self.app_token = os.getenv("GLPI_APP_TOKEN")
        self.user_token = os.getenv("GLPI_USER_TOKEN")

        # If any value is missing, try config file
        if not all([self.url, self.app_token, self.user_token]):
            self._load_from_file()

    def _load_from_file(self):
        """Load configuration from ~/.config/glpi/config.yml."""
        config_path = Path.home() / ".config" / "glpi" / "config.yml"

        if not config_path.exists():
            return

        try:
            with open(config_path, "r") as f:
                data = yaml.safe_load(f)

            # Only use file values if env var is not set
            if not self.url:
                self.url = data.get("url")
            if not self.app_token:
                self.app_token = data.get("app_token")
            if not self.user_token:
                self.user_token = data.get("user_token")
        except Exception as e:
            # Silently ignore file errors, env vars might be enough
            pass

    def validate(self) -> tuple[bool, Optional[str]]:
        """Validate that all required config values are present.

        Returns:
            Tuple of (is_valid, error_message)
        """
        if not self.url:
            return False, "GLPI_URL n�o configurado"
        if not self.app_token:
            return False, "GLPI_APP_TOKEN n�o configurado"
        if not self.user_token:
            return False, "GLPI_USER_TOKEN n�o configurado"

        return True, None

    def __repr__(self):
        """String representation hiding sensitive tokens."""
        return (
            f"Config(url={self.url}, "
            f"app_token={'***' if self.app_token else None}, "
            f"user_token={'***' if self.user_token else None})"
        )
