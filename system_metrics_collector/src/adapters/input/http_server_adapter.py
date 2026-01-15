import logging
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
from typing import Optional
from src.adapters.out.prometheus_metrics_adapter import PrometheusMetricsAdapter

logger = logging.getLogger(__name__)

class MetricsHandler(BaseHTTPRequestHandler):
    prometheus_adapter: Optional[PrometheusMetricsAdapter] = None

    def do_GET(self):
        if self.path == '/metrics':
            if self.prometheus_adapter:
                try:
                    content = self.prometheus_adapter.get_metrics_content()
                    self.send_response(200)
                    self.send_header('Content-Type', self.prometheus_adapter.get_content_type())
                    self.end_headers()
                    self.wfile.write(content)
                    logger.debug("Served metrics at /metrics endpoint")
                except Exception as e:
                    logger.error(f"Error serving metrics: {e}")
                    self.send_response(500)
                    self.end_headers()
                    self.wfile.write(b"Internal Server Error")
            else:
                self.send_response(503)
                self.end_headers()
                self.wfile.write(b"Metrics adapter not available")
        elif self.path == '/health':
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            self.wfile.write(b"OK")
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Not Found")

    def log_message(self, format, *args):
        logger.debug(f"HTTP: {format % args}")

class HTTPServerAdapter:
    def __init__(self, prometheus_adapter: PrometheusMetricsAdapter, port: int = 8000) -> None:
        self.prometheus_adapter = prometheus_adapter
        self.port = port
        self.server: Optional[HTTPServer] = None
        self.server_thread: Optional[threading.Thread] = None

        MetricsHandler.prometheus_adapter = prometheus_adapter

    def start(self) -> None:
        try:
            self.server = HTTPServer(('0.0.0.0', self.port), MetricsHandler)
            self.server_thread = threading.Thread(target=self.server.serve_forever)
            self.server_thread.daemon = True
            self.server_thread.start()
            logger.info(f"HTTP server started on port {self.port}")
            logger.info(f"Metrics endpoint: http://0.0.0.0:{self.port}/metrics")
            logger.info(f"Health endpoint: http://0.0.0.0:{self.port}/health")
        except Exception as e:
            logger.error(f"Error starting HTTP server: {e}")
            raise

    def stop(self) -> None:
        if self.server:
            self.server.shutdown()
            self.server.server_close()
            logger.info("HTTP server stopped")
        if self.server_thread:
            self.server_thread.join(timeout=5)