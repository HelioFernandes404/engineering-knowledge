from abc import ABC, abstractmethod
from src.domain.types import LogLevel, LogFormat, OutputFormat

class ConfigPort(ABC):
    @abstractmethod
    def get_app_name(self) -> str:
        pass

    @abstractmethod
    def get_app_version(self) -> str:
        pass

    @abstractmethod
    def get_environment(self) -> str:
        pass

    @abstractmethod
    def get_metrics_interval(self) -> int:
        pass

    @abstractmethod
    def get_output_format(self) -> OutputFormat:
        pass

    @abstractmethod
    def get_output_file(self) -> str:
        pass

    @abstractmethod
    def should_collect_cpu_metrics(self) -> bool:
        pass

    @abstractmethod
    def should_collect_memory_metrics(self) -> bool:
        pass

    @abstractmethod
    def should_collect_disk_metrics(self) -> bool:
        pass

    @abstractmethod
    def should_collect_network_metrics(self) -> bool:
        pass

    @abstractmethod
    def should_collect_system_metrics(self) -> bool:
        pass

    @abstractmethod
    def get_custom_metric_prefix(self) -> str:
        pass

    @abstractmethod
    def get_log_level(self) -> LogLevel:
        pass

    @abstractmethod
    def get_log_format(self) -> LogFormat:
        pass

    @abstractmethod
    def get_metrics_server_port(self) -> int:
        pass