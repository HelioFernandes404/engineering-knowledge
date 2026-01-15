"""Centralized logging configuration using loguru"""
import sys
from loguru import logger

# Remove default handler
logger.remove()

# Add custom handler with formatting
logger.add(
    sys.stderr,
    format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <level>{message}</level>",
    level="INFO",
    colorize=True,
)

# Add file handler for errors
logger.add(
    "logs/speech2text_{time:YYYY-MM-DD}.log",
    rotation="1 day",
    retention="7 days",
    level="WARNING",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
)

__all__ = ["logger"]
