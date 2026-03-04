import logging
from pathlib import Path
from app.core.config import settings

LOG_LEVEL_NUM = getattr(logging, settings.LOG_LEVEL, logging.INFO)

LOG_DIR = Path("logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)

RESET = "\033[0m"
COLOR_TIME = "\033[90m"     # серый
COLOR_NAME = "\033[36m"     # циан
COLOR_FUNC = "\x1b[38;5;208m"  # оранжевый
LEVEL_COLORS = {
    "DEBUG":    "\033[37m",
    "INFO":     "\033[32m",
    "WARNING":  "\033[33m",
    "ERROR":    "\033[31m",
    "CRITICAL": "\033[41m",
}

class ColorFormatter(logging.Formatter):
    def format(self, record):
        asctime = f"{COLOR_TIME}{self.formatTime(record, self.datefmt)}{RESET}"
        level = f"{LEVEL_COLORS.get(record.levelname, '')}{record.levelname}{RESET}"
        name = f"{COLOR_NAME}[{record.name}]{RESET}"

        # добавляем место вызова
        where = f"{COLOR_FUNC}[{record.funcName}]{RESET}"

        msg = record.getMessage()
        return f"{asctime} {level}: {name} {where}: {msg}"

def get_logger(name: str, filename: str = "logs.log") -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(LOG_LEVEL_NUM)

    if not logger.handlers:
        # файл без цветов
        file_formatter = logging.Formatter(
            "%(asctime)s %(levelname)s: [%(name)s] %(funcName)s: %(message)s",
            "%d/%m/%Y %H:%M:%S"
        )
        file_handler = logging.FileHandler(LOG_DIR / filename, encoding="utf-8")
        file_handler.setFormatter(file_formatter)
        file_handler.setLevel(LOG_LEVEL_NUM)
        logger.addHandler(file_handler)

        # консоль с цветами
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(ColorFormatter(datefmt="%d/%m/%Y %H:%M:%S"))
        stream_handler.setLevel(logging.DEBUG if name == "aiogram" else LOG_LEVEL_NUM)
        logger.addHandler(stream_handler)

        logger.propagate = False

    return logger