"""CLI entry‑point: schedule the daily job and start the scheduler."""
import signal
from apscheduler.schedulers.blocking import BlockingScheduler

from jobs import daily_fact_job
from config import settings
from logger import logger


def _graceful_shutdown(signum, frame):  # noqa: D401, D403 (simple handler)
    """Stop the scheduler without waiting for running jobs when a signal is received."""
    logger.info("Signal %s received — shutting down scheduler …", signum)
    scheduler.shutdown(wait=False)


scheduler = BlockingScheduler()

scheduler.add_job(
    daily_fact_job,
    "cron",
    hour=settings.SEND_TIME_HOUR,
    minute=settings.SEND_TIME_MINUTE,
    id="daily_fact",
    misfire_grace_time=60 * 5,
)

signal.signal(signal.SIGINT, _graceful_shutdown)
signal.signal(signal.SIGTERM, _graceful_shutdown)

logger.info(
    "Bot started. Facts will be sent daily at %02d:%02d.",
    settings.SEND_TIME_HOUR,
    settings.SEND_TIME_MINUTE,
)

if __name__ == "__main__":
    scheduler.start()
