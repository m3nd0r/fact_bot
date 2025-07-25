"""Simple logging wrapper so every module imports the same logger."""
import logging

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s: %(message)s",
)
logger = logging.getLogger("fact_bot")
