import psutil
import time
import logging
from datetime import datetime
from typing import Dict, Any
import pytz
from src.ports.metrics_collector_port import MetricsCollectorPort
from src.ports.config_port import ConfigPort
from src.domain.models import SystemMetrics, ApplicationMetrics

logger = logging.getLogger(__name__)

class SystemMetricsAdapter(MetricsCollectorPort):
    def __init__(self, config: ConfigPort) -> None:
        self.config = config

    def collect_system_metrics(self) -> SystemMetrics:
        try:
            cpu_percent = 0.0
            cpu_count = 0
            if self.config.should_collect_cpu_metrics():
                cpu_percent = psutil.cpu_percent(interval=1)
                cpu_count = psutil.cpu_count()

            memory_total = 0
            memory_available = 0
            memory_percent = 0.0
            if self.config.should_collect_memory_metrics():
                memory = psutil.virtual_memory()
                memory_total = memory.total
                memory_available = memory.available
                memory_percent = memory.percent

            disk_total = 0
            disk_used = 0
            disk_free = 0
            disk_percent = 0.0
            if self.config.should_collect_disk_metrics():
                disk = psutil.disk_usage('/')
                disk_total = disk.total
                disk_used = disk.used
                disk_free = disk.free
                disk_percent = (disk.used / disk.total) * 100

            sao_paulo_tz = pytz.timezone('America/Sao_Paulo')
            return SystemMetrics(
                timestamp=datetime.now(sao_paulo_tz),
                cpu_percent=cpu_percent,
                cpu_count=cpu_count,
                memory_total=memory_total,
                memory_available=memory_available,
                memory_percent=memory_percent,
                disk_total=disk_total,
                disk_used=disk_used,
                disk_free=disk_free,
                disk_percent=disk_percent
            )

        except Exception as e:
            logger.error(f"Error collecting system metrics: {e}")
            raise

    def collect_application_metrics(self) -> ApplicationMetrics:
        custom_metrics = {
            f"{self.config.get_custom_metric_prefix()}uptime": time.time(),
        }

        return ApplicationMetrics(
            app_name=self.config.get_app_name(),
            app_version=self.config.get_app_version(),
            environment=self.config.get_environment(),
            uptime=time.time(),
            custom_metrics=custom_metrics
        )