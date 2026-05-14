from app.core.path import ROOT
import logging as log
log.basicConfig(level=log.DEBUG)

import logging as log

logger = log.getLogger()
logger.setLevel(log.DEBUG)

formatter = log.Formatter(
    "%(asctime)s [%(levelname)s] %(message)s"
)

# FILE
file_handler = log.FileHandler(ROOT / "app" / "log" / "app.log")
file_handler.setFormatter(formatter)

# CONSOLE
console_handler = log.StreamHandler()
console_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)