import logging
from typing import Dict, Any
from prometheus_client import Gauge, Info, CollectorRegistry, generate_latest, CONTENT_TYPE_LATEST
from src.ports.metrics_exporter_port import MetricsExporterPort
from src.ports.config_port import ConfigPort

logger = logging.getLogger(__name__)

class PrometheusMetricsAdapter(MetricsExporterPort):
    def __init__(self, config: ConfigPort) -> None:
        self.config = config
        self.registry = CollectorRegistry()
        self._setup_metrics()

    def _setup_metrics(self) -> None:
        self.cpu_percent = Gauge(
            'system_cpu_percent',
            'CPU usage percentage',
            registry=self.registry
        )
        self.cpu_count = Gauge(
            'system_cpu_count',
            'Number of CPU cores',
            registry=self.registry
        )
        self.memory_total = Gauge(
            'system_memory_total_bytes',
            'Total memory in bytes',
            registry=self.registry
        )
        self.memory_available = Gauge(
            'system_memory_available_bytes',
            'Available memory in bytes',
            registry=self.registry
        )
        self.memory_percent = Gauge(
            'system_memory_percent',
            'Memory usage percentage',
            registry=self.registry
        )
        self.disk_total = Gauge(
            'system_disk_total_bytes',
            'Total disk space in bytes',
            registry=self.registry
        )
        self.disk_used = Gauge(
            'system_disk_used_bytes',
            'Used disk space in bytes',
            registry=self.registry
        )
        self.disk_free = Gauge(
            'system_disk_free_bytes',
            'Free disk space in bytes',
            registry=self.registry
        )
        self.disk_percent = Gauge(
            'system_disk_percent',
            'Disk usage percentage',
            registry=self.registry
        )
        self.app_uptime = Gauge(
            'app_uptime_seconds',
            'Application uptime in seconds',
            registry=self.registry
        )
        self.app_info = Info(
            'app_info',
            'Application information',
            registry=self.registry
        )

    def export(self, metrics: Dict[str, Any]) -> str:
        try:
            if 'cpu_percent' in metrics:
                self.cpu_percent.set(metrics['cpu_percent'])
            if 'cpu_count' in metrics:
                self.cpu_count.set(metrics['cpu_count'])
            if 'memory_total' in metrics:
                self.memory_total.set(metrics['memory_total'])
            if 'memory_available' in metrics:
                self.memory_available.set(metrics['memory_available'])
            if 'memory_percent' in metrics:
                self.memory_percent.set(metrics['memory_percent'])
            if 'disk_total' in metrics:
                self.disk_total.set(metrics['disk_total'])
            if 'disk_used' in metrics:
                self.disk_used.set(metrics['disk_used'])
            if 'disk_free' in metrics:
                self.disk_free.set(metrics['disk_free'])
            if 'disk_percent' in metrics:
                self.disk_percent.set(metrics['disk_percent'])
            if 'app_uptime' in metrics:
                self.app_uptime.set(metrics['app_uptime'])

            self.app_info.info({
                'name': metrics.get('app_name', ''),
                'version': metrics.get('app_version', ''),
                'environment': metrics.get('app_environment', '')
            })

            return "/metrics endpoint ready"
        except Exception as e:
            logger.error(f"Error updating Prometheus metrics: {e}")
            raise

    def display(self, metrics: Dict[str, Any]) -> None:
        print("Metrics available at /metrics endpoint")
        for key, value in metrics.items():
            if key not in ['timestamp']:
                print(f"{key}: {value}")

    def get_metrics_content(self) -> bytes:
        return generate_latest(self.registry)

    def get_content_type(self) -> str:
        return CONTENT_TYPE_LATEST