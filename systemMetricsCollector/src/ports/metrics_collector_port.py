from abc import ABC, abstractmethod
from src.domain.models import SystemMetrics, ApplicationMetrics

class MetricsCollectorPort(ABC):
    @abstractmethod
    def collect_system_metrics(self) -> SystemMetrics:
        pass

    @abstractmethod
    def collect_application_metrics(self) -> ApplicationMetrics:
        pass