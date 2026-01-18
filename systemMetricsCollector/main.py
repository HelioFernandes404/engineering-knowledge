import sys
import os
from typing import NoReturn, Optional

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.adapters.out.config_adapter import ConfigAdapter
from src.adapters.out.system_metrics_adapter import SystemMetricsAdapter
from src.adapters.out.prometheus_metrics_adapter import PrometheusMetricsAdapter
from src.adapters.out.otlp_exporter_adapter import OTLPExporterAdapter
from src.adapters.input.cli_adapter import CLIAdapter
from src.domain.services import MetricsService

def main() -> None:
    config = ConfigAdapter()
    metrics_collector = SystemMetricsAdapter(config)
    prometheus_adapter = PrometheusMetricsAdapter(config)

    # Initialize OTLP exporter if enabled
    otlp_exporter: Optional[OTLPExporterAdapter] = None
    if config.is_otlp_enabled():
        otlp_exporter = OTLPExporterAdapter(
            endpoint=config.get_otlp_endpoint(),
            enabled=True
        )

    metrics_service = MetricsService(
        config,
        metrics_collector,
        prometheus_adapter,
        otlp_exporter
    )
    cli_adapter = CLIAdapter(metrics_service, config, prometheus_adapter)

    cli_adapter.start(sys.argv)

if __name__ == "__main__":
    main()