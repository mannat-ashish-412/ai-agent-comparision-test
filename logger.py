"""
Logging configuration for the agent system.
"""

import logging
import sys
from pathlib import Path
from typing import Optional


class AgentLogger:
    """Centralized logger for the agent system."""

    _instance: Optional[logging.Logger] = None

    @classmethod
    def get_logger(
        cls,
        name: str = "agent_system",
        level: str = "INFO",
        log_file: Optional[str] = None,
    ) -> logging.Logger:
        """Get or create the logger instance."""

        if cls._instance is not None:
            return cls._instance

        # Create logger
        logger = logging.getLogger(name)
        logger.setLevel(getattr(logging, level.upper()))

        # Avoid duplicate handlers
        if logger.handlers:
            return logger

        # Create formatters
        detailed_formatter = logging.Formatter(
            fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(funcName)s:%(lineno)d | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        simple_formatter = logging.Formatter(
            fmt="%(asctime)s | %(levelname)-8s | %(message)s", datefmt="%H:%M:%S"
        )

        # Console handler (simple format)
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(simple_formatter)
        logger.addHandler(console_handler)

        # File handler (detailed format)
        if log_file:
            log_path = Path(log_file)
            log_path.parent.mkdir(parents=True, exist_ok=True)

            file_handler = logging.FileHandler(log_file, encoding="utf-8")
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(detailed_formatter)
            logger.addHandler(file_handler)

        cls._instance = logger
        return logger

    @classmethod
    def reset(cls):
        """Reset the logger instance."""
        if cls._instance:
            for handler in cls._instance.handlers[:]:
                handler.close()
                cls._instance.removeHandler(handler)
            cls._instance = None


def get_logger(name: str = "agent_system") -> logging.Logger:
    """Convenience function to get the logger."""
    from config import get_settings

    settings = get_settings()
    return AgentLogger.get_logger(
        name=name, level=settings.log_level, log_file=settings.log_file
    )
