import logging
import time
import signal
import sys
from typing import Optional, List, Any
from src.domain.services import MetricsService
from src.domain.models import MetricsSnapshot
from src.ports.config_port import ConfigPort
from src.adapters.input.http_server_adapter import HTTPServerAdapter
from src.adapters.out.prometheus_metrics_adapter import PrometheusMetricsAdapter
from src.adapters.out.victorialogs_adapter import VictoriaLogsAdapter

logger = logging.getLogger(__name__)

class CLIAdapter:
    def __init__(self, metrics_service: MetricsService, config: ConfigPort, prometheus_adapter: Optional[PrometheusMetricsAdapter] = None) -> None:
        self.metrics_service = metrics_service
        self.config = config
        self.prometheus_adapter = prometheus_adapter
        self.running = True
        self.http_server: Optional[HTTPServerAdapter] = None
        self._setup_logging()

    def _setup_logging(self) -> None:
        log_level = self.config.get_log_level().upper()

        # If VictoriaLogs is enabled, use the VictoriaLogs adapter
        if self.config.is_victorialogs_enabled():
            vlogs_adapter = VictoriaLogsAdapter(
                victorialogs_url=self.config.get_victorialogs_url(),
                app_name=self.config.get_app_name(),
                environment=self.config.get_environment(),
                log_level=log_level,
                enable_console=True
            )
            vlogs_adapter.configure_logging()
        else:
            # Fallback to basic logging configuration
            log_level_int = getattr(logging, log_level)
            if self.config.get_log_format() == "json":
                logging.basicConfig(
                    level=log_level_int,
                    format='{"timestamp": "%(asctime)s", "level": "%(levelname)s", "message": "%(message)s"}'
                )
            else:
                logging.basicConfig(
                    level=log_level_int,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
                )

    def _signal_handler(self, signum: int, frame: Any) -> None:
        logger.info("Received signal to stop. Shutting down gracefully...")
        self.running = False
        if self.http_server:
            self.http_server.stop()

    def run_once(self) -> Optional[MetricsSnapshot]:
        try:
            snapshot = self.metrics_service.collect_metrics()
            self.metrics_service.display_metrics(snapshot)
            result = self.metrics_service.update_metrics(snapshot)
            return snapshot
        except Exception as e:
            logger.error(f"Error during metrics collection: {e}")
            return None

    def run_continuous(self) -> None:
        logger.info(f"Starting {self.config.get_app_name()} in continuous mode")
        logger.info(f"Metrics will be collected every {self.config.get_metrics_interval()} seconds")

        if not self.prometheus_adapter:
            raise ValueError("PrometheusMetricsAdapter is required for continuous mode")

        self.http_server = HTTPServerAdapter(self.prometheus_adapter, self.config.get_metrics_server_port())

        try:
            self.http_server.start()
        except Exception as e:
            logger.error(f"Failed to start HTTP server: {e}")
            return

        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)

        while self.running:
            self.run_once()
            if self.running:
                time.sleep(self.config.get_metrics_interval())

        logger.info("Application stopped")

    def start(self, args: List[str]) -> None:
        if len(args) > 1 and args[1] == "--once":
            self.run_once()
        else:
            self.run_continuous()