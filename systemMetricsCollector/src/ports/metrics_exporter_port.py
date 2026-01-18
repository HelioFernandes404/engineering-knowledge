from abc import ABC, abstractmethod
from typing import Dict, Any

class MetricsExporterPort(ABC):
    @abstractmethod
    def export(self, metrics: Dict[str, Any]) -> str:
        pass

    @abstractmethod
    def display(self, metrics: Dict[str, Any]) -> None:
        pass