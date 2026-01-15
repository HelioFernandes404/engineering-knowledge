from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Any, Optional, Union

@dataclass
class SystemMetrics:
    timestamp: datetime
    cpu_percent: float
    cpu_count: int
    memory_total: int
    memory_available: int
    memory_percent: float
    disk_total: int
    disk_used: int
    disk_free: int
    disk_percent: float

@dataclass
class ApplicationMetrics:
    app_name: str
    app_version: str
    environment: str
    uptime: float
    custom_metrics: Dict[str, Any]

@dataclass
class MetricsSnapshot:
    system_metrics: Optional[SystemMetrics]
    application_metrics: ApplicationMetrics
    timestamp: datetime

    def to_dict(self) -> Dict[str, Any]:
        result = {
            "timestamp": self.timestamp.isoformat(),
            "app_name": self.application_metrics.app_name,
            "app_version": self.application_metrics.app_version,
            "app_environment": self.application_metrics.environment,
            "app_uptime": self.application_metrics.uptime,
        }

        if self.system_metrics:
            result.update({
                "cpu_percent": self.system_metrics.cpu_percent,
                "cpu_count": self.system_metrics.cpu_count,
                "memory_total": self.system_metrics.memory_total,
                "memory_available": self.system_metrics.memory_available,
                "memory_percent": self.system_metrics.memory_percent,
                "disk_total": self.system_metrics.disk_total,
                "disk_used": self.system_metrics.disk_used,
                "disk_free": self.system_metrics.disk_free,
                "disk_percent": self.system_metrics.disk_percent,
            })

        result.update(self.application_metrics.custom_metrics)
        return result