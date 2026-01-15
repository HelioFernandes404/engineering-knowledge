from abc import ABC, abstractmethod
from typing import Dict, Any

class OTLPExporterPort(ABC):
    @abstractmethod
    def export_metrics(self, metrics: Dict[str, Any]) -> bool:
        """Export metrics to OTLP collector"""
        pass

    @abstractmethod
    def is_enabled(self) -> bool:
        """Check if OTLP export is enabled"""
        pass
