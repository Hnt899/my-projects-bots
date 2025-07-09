from sys import stdout

from loguru import logger

from app.config.settings import settings
from app.utils.utils import get_project_root

logger.remove()

def setup_logger():
    log_directory = get_project_root() / "log"
    log_directory.mkdir(exist_ok=True)

    if settings.LOG_FILE:
        logger.add(
            sink=log_directory / "p2p_bot.log",
            level="DEBUG",
            rotation="20 MB",
            compression="zip",
            backtrace=True,
            diagnose=True,
            enqueue=True,
        )

    if settings.LOG_STREAM:
        logger.add(
            sink=stdout,
            level="DEBUG",
            backtrace=True,
            diagnose=True,
            enqueue=True,
        )
