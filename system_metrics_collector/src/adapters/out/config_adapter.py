import os
import logging
from dotenv import load_dotenv
from src.ports.config_port import ConfigPort
from src.domain.types import LogLevel, LogFormat, OutputFormat

logger = logging.getLogger(__name__)

class ConfigAdapter(ConfigPort):
    def __init__(self, env_file: str = ".env") -> None:
        load_dotenv(env_file)
        logger.info(f"Configuration loaded from {env_file}")

    def get_app_name(self) -> str:
        return os.getenv("APP_NAME", "MetricsApp")

    def get_app_version(self) -> str:
        return os.getenv("APP_VERSION", "1.0.0")

    def get_environment(self) -> str:
        return os.getenv("ENVIRONMENT", "development")

    def get_metrics_interval(self) -> int:
        return int(os.getenv("METRICS_INTERVAL_SECONDS", "60"))

    def get_output_format(self) -> OutputFormat:
        format_value = os.getenv("METRICS_OUTPUT_FORMAT", "json")
        return format_value if format_value in ["json", "yaml"] else "json"

    def get_output_file(self) -> str:
        return os.getenv("METRICS_OUTPUT_FILE", "metrics.json")

    def should_collect_cpu_metrics(self) -> bool:
        return os.getenv("COLLECT_CPU_METRICS", "true").lower() == "true"

    def should_collect_memory_metrics(self) -> bool:
        return os.getenv("COLLECT_MEMORY_METRICS", "true").lower() == "true"

    def should_collect_disk_metrics(self) -> bool:
        return os.getenv("COLLECT_DISK_METRICS", "true").lower() == "true"

    def should_collect_network_metrics(self) -> bool:
        return os.getenv("COLLECT_NETWORK_METRICS", "false").lower() == "true"

    def should_collect_system_metrics(self) -> bool:
        return (self.should_collect_cpu_metrics() or
                self.should_collect_memory_metrics() or
                self.should_collect_disk_metrics() or
                self.should_collect_network_metrics())

    def get_custom_metric_prefix(self) -> str:
        return os.getenv("CUSTOM_METRIC_PREFIX", "app_")

    def get_log_level(self) -> LogLevel:
        level = os.getenv("LOG_LEVEL", "INFO")
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        return level if level in valid_levels else "INFO"

    def get_log_format(self) -> LogFormat:
        log_format = os.getenv("LOG_FORMAT", "json")
        return log_format if log_format in ["json", "text"] else "json"

    def get_metrics_server_port(self) -> int:
        return int(os.getenv("METRICS_SERVER_PORT", "8000"))

    def get_victorialogs_url(self) -> str:
        return os.getenv("VICTORIALOGS_URL", "http://localhost:9428")

    def is_victorialogs_enabled(self) -> bool:
        return os.getenv("ENABLE_VICTORIALOGS", "false").lower() == "true"

    def is_otlp_enabled(self) -> bool:
        return os.getenv("ENABLE_OTLP", "false").lower() == "true"

    def get_otlp_endpoint(self) -> str:
        return os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "http://otel-collector:4317")