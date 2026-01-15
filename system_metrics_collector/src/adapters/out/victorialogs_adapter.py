import logging
import json
import requests
from typing import Dict, Any, Optional
from datetime import datetime


class VictoriaLogsHandler(logging.Handler):
    """Custom logging handler to send logs to VictoriaLogs"""

    def __init__(self, victorialogs_url: str, app_name: str, environment: str):
        super().__init__()
        self.victorialogs_url = victorialogs_url.rstrip('/')
        self.app_name = app_name
        self.environment = environment
        self.session = requests.Session()

    def emit(self, record: logging.LogRecord) -> None:
        """Send log record to VictoriaLogs"""
        try:
            log_entry = self._format_log_entry(record)
            self._send_to_victorialogs(log_entry)
        except Exception as e:
            # Print to stderr to avoid recursion
            import sys
            print(f"VictoriaLogs error: {e}", file=sys.stderr)
            self.handleError(record)

    def _format_log_entry(self, record: logging.LogRecord) -> Dict[str, Any]:
        """Format log record as JSON for VictoriaLogs"""
        log_data = {
            "_msg": record.getMessage(),
            "_time": datetime.fromtimestamp(record.created).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "app": self.app_name,
            "environment": self.environment,
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }

        # Add exception info if present
        if record.exc_info:
            log_data["exception"] = self.format(record.exc_info)

        # Add extra fields if present
        if hasattr(record, 'extra_fields'):
            log_data.update(record.extra_fields)

        return log_data

    def _send_to_victorialogs(self, log_entry: Dict[str, Any]) -> None:
        """Send log entry to VictoriaLogs via HTTP API"""
        try:
            # VictoriaLogs expects JSON Lines format
            url = f"{self.victorialogs_url}/insert/jsonline"

            # Convert to JSON string and send
            response = self.session.post(
                url,
                data=json.dumps(log_entry) + '\n',
                headers={'Content-Type': 'application/x-ndjson'},
                timeout=5
            )
            response.raise_for_status()
        except requests.RequestException as e:
            # Print to stderr to debug
            import sys
            print(f"VictoriaLogs send error: {e}", file=sys.stderr)
            raise

    def close(self) -> None:
        """Close the session"""
        self.session.close()
        super().close()


class VictoriaLogsAdapter:
    """Adapter to configure VictoriaLogs logging for the application"""

    def __init__(
        self,
        victorialogs_url: str,
        app_name: str,
        environment: str,
        log_level: str = "INFO",
        enable_console: bool = True
    ):
        self.victorialogs_url = victorialogs_url
        self.app_name = app_name
        self.environment = environment
        self.log_level = log_level
        self.enable_console = enable_console

    def configure_logging(self) -> None:
        """Configure logging to send to both console and VictoriaLogs"""
        root_logger = logging.getLogger()
        root_logger.setLevel(getattr(logging, self.log_level.upper()))

        # Clear existing handlers
        root_logger.handlers.clear()

        # Add VictoriaLogs handler
        vlogs_handler = VictoriaLogsHandler(
            self.victorialogs_url,
            self.app_name,
            self.environment
        )
        vlogs_handler.setLevel(getattr(logging, self.log_level.upper()))
        root_logger.addHandler(vlogs_handler)

        # Add console handler if enabled
        if self.enable_console:
            console_handler = logging.StreamHandler()
            console_handler.setLevel(getattr(logging, self.log_level.upper()))

            # JSON format for console
            formatter = logging.Formatter(
                '{"timestamp": "%(asctime)s", "level": "%(levelname)s", "logger": "%(name)s", "message": "%(message)s"}'
            )
            console_handler.setFormatter(formatter)
            root_logger.addHandler(console_handler)

        logging.info(f"VictoriaLogs logging configured: {self.victorialogs_url}")
