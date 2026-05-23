from app.utils.path import ROOT
import logging as log
from pathlib import Path

log_dir = ROOT / "app" / "log"
log_dir.mkdir(parents=True, exist_ok=True)

logger = log.getLogger()
logger.setLevel(log.DEBUG)

formatter = log.Formatter(
    "%(asctime)s [%(levelname)s] %(message)s"
)

if logger.hasHandlers():
    logger.handlers.clear()

file_handler = log.FileHandler(log_dir / "app.log", mode="w", encoding="utf-8")
file_handler.setFormatter(formatter)

console_handler = log.StreamHandler()
console_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)