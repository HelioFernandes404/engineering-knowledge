import logging
from datetime import datetime
from typing import Dict, Any, Optional
import pytz
from src.domain.models import MetricsSnapshot, SystemMetrics, ApplicationMetrics
from src.ports.metrics_collector_port import MetricsCollectorPort
from src.ports.metrics_exporter_port import MetricsExporterPort
from src.ports.config_port import ConfigPort
from src.ports.otlp_exporter_port import OTLPExporterPort

logger = logging.getLogger(__name__)

class MetricsService:
    def __init__(
        self,
        config: ConfigPort,
        collector: MetricsCollectorPort,
        exporter: MetricsExporterPort,
        otlp_exporter: Optional[OTLPExporterPort] = None
    ) -> None:
        self.config = config
        self.collector = collector
        self.exporter = exporter
        self.otlp_exporter = otlp_exporter

    def collect_metrics(self) -> MetricsSnapshot:
        sao_paulo_tz = pytz.timezone('America/Sao_Paulo')
        timestamp = datetime.now(sao_paulo_tz)

        system_metrics: Optional[SystemMetrics] = None
        if self.config.should_collect_system_metrics():
            system_metrics = self.collector.collect_system_metrics()

        application_metrics = self.collector.collect_application_metrics()

        snapshot = MetricsSnapshot(
            system_metrics=system_metrics,
            application_metrics=application_metrics,
            timestamp=timestamp
        )

        logger.info(f"Metrics collected at {timestamp}")
        return snapshot

    def update_metrics(self, snapshot: MetricsSnapshot) -> str:
        metrics_dict = snapshot.to_dict()
        result = self.exporter.export(metrics_dict)
        logger.info(f"Metrics updated: {result}")

        # Export to OTLP if enabled
        if self.otlp_exporter and self.otlp_exporter.is_enabled():
            self.otlp_exporter.export_metrics(metrics_dict)
            logger.debug("Metrics exported to OTLP collector")

        return result

    def display_metrics(self, snapshot: MetricsSnapshot) -> None:
        metrics_dict = snapshot.to_dict()
        self.exporter.display(metrics_dict)