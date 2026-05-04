import logging


def configure_logging(level: str = "INFO") -> None:
    """Configure a consistent logging format across modules."""
    logging.basicConfig(
        level=level,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )

