import logging
import os
from typing import Dict, Any
from opentelemetry import metrics
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.resources import Resource
from src.ports.otlp_exporter_port import OTLPExporterPort

logger = logging.getLogger(__name__)

class OTLPExporterAdapter(OTLPExporterPort):
    def __init__(self, endpoint: str = None, enabled: bool = True):
        self._enabled = enabled
        self._endpoint = endpoint or os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "http://otel-collector:4317")

        if self._enabled:
            self._initialize_meter()
        else:
            logger.info("OTLP exporter is disabled")

    def _initialize_meter(self):
        """Initialize OpenTelemetry meter and metrics"""
        try:
            # Configure resource
            resource = Resource.create({
                "service.name": os.getenv("APP_NAME", "infragen"),
                "service.version": os.getenv("APP_VERSION", "1.0.0"),
                "deployment.environment": os.getenv("ENVIRONMENT", "production")
            })

            # Configure OTLP exporter
            otlp_exporter = OTLPMetricExporter(
                endpoint=self._endpoint,
                insecure=True  # Use insecure for local development
            )

            # Configure metric reader with export interval
            reader = PeriodicExportingMetricReader(
                otlp_exporter,
                export_interval_millis=30000  # Export every 30 seconds
            )

            # Set up meter provider
            provider = MeterProvider(resource=resource, metric_readers=[reader])
            metrics.set_meter_provider(provider)

            # Create meter
            self._meter = metrics.get_meter(__name__)

            # Create instruments
            self._cpu_gauge = self._meter.create_gauge(
                name="system.cpu.percent",
                description="CPU usage percentage",
                unit="%"
            )

            self._memory_gauge = self._meter.create_gauge(
                name="system.memory.percent",
                description="Memory usage percentage",
                unit="%"
            )

            self._disk_gauge = self._meter.create_gauge(
                name="system.disk.percent",
                description="Disk usage percentage",
                unit="%"
            )

            logger.info(f"OTLP exporter initialized with endpoint: {self._endpoint}")
        except Exception as e:
            logger.error(f"Failed to initialize OTLP exporter: {e}")
            self._enabled = False

    def export_metrics(self, metrics_data: Dict[str, Any]) -> bool:
        """Export metrics to OTLP collector"""
        if not self._enabled:
            return False

        try:
            system_metrics = metrics_data.get("system_metrics", {})

            # Export CPU metrics
            if "cpu" in system_metrics:
                cpu_percent = system_metrics["cpu"].get("percent", 0)
                self._cpu_gauge.set(cpu_percent)
                logger.debug(f"Exported CPU metric: {cpu_percent}%")

            # Export Memory metrics
            if "memory" in system_metrics:
                memory_percent = system_metrics["memory"].get("percent", 0)
                self._memory_gauge.set(memory_percent)
                logger.debug(f"Exported Memory metric: {memory_percent}%")

            # Export Disk metrics
            if "disk" in system_metrics:
                disk_percent = system_metrics["disk"].get("percent", 0)
                self._disk_gauge.set(disk_percent)
                logger.debug(f"Exported Disk metric: {disk_percent}%")

            return True
        except Exception as e:
            logger.error(f"Failed to export metrics to OTLP: {e}")
            return False

    def is_enabled(self) -> bool:
        """Check if OTLP export is enabled"""
        return self._enabled
