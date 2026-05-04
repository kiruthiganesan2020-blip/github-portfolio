from __future__ import annotations

import logging
from pathlib import Path

from .config import AppConfig, load_config
from .logging_utils import configure_logging

logger = logging.getLogger(__name__)


def bootstrap() -> AppConfig:
    """
    Phase 0 bootstrap:
    - Load environment config
    - Create required folders
    - Configure logging
    """
    config = load_config()
    configure_logging(config.log_level)
    ensure_project_directories(config)
    logger.info("Phase 0 bootstrap completed successfully.")
    return config


def ensure_project_directories(config: AppConfig) -> None:
    required_dirs = [
        config.data_dir,
        Path("logs").resolve(),
        Path("artifacts").resolve(),
    ]
    for directory in required_dirs:
        directory.mkdir(parents=True, exist_ok=True)
        logger.debug("Ensured directory exists: %s", directory)

