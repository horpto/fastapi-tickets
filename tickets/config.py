import logging
import logging.config
import multiprocessing
from functools import cache

from pydantic import BaseSettings, RedisDsn


class Settings(BaseSettings):
    workers: int = multiprocessing.cpu_count() - 1
    listen_addr: str = "0.0.0.0"
    listen_port: int = 8080
    debug: bool = True
    sentry_dsn: str = ""

    redis_dsn: RedisDsn = ""


@cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()


def set_logging_config():
    log_level = logging.INFO

    if settings.debug:
        log_level = logging.DEBUG

    log_config = {
        "version": 1,
        "formatters": {
            "def": {
                "format": "[%(asctime)s] [%(levelname)s] %(name)s: %(message)s",
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "def",
                "stream": "ext://sys.stdout",
            },
        },
        "loggers": {
            "root": {"level": log_level, "handlers": ["console"]},
        },
        "disable_existing_loggers": False,
    }

    logging.config.dictConfig(log_config)
