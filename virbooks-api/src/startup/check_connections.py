from collections.abc import Callable
from time import sleep

from flask import Flask
from pymongo import MongoClient
from pymongo.errors import PyMongoError

from src.configs.logger_config import setup_logger

logger = setup_logger(__name__)

MAX_ATTEMPTS = 5
RETRY_DELAY_SECONDS = 2
CONNECT_TIMEOUT_MS = 3000

MONGO_SERVICE_NAME = "MongoDB"


def check_mongo_connection(app: Flask) -> bool:
    mongo_uri: str | None = app.config.get("MONGO_URI")
    if not mongo_uri:
        logger.info("%s is not configured (no MONGO_URI). Skipping connection check.", MONGO_SERVICE_NAME)
        return False

    for attempt in range(1, MAX_ATTEMPTS + 1):
        client: MongoClient = MongoClient(mongo_uri, serverSelectionTimeoutMS=CONNECT_TIMEOUT_MS)
        try:
            client.admin.command("ping")
            logger.info("Connected to %s on attempt %d/%d.", MONGO_SERVICE_NAME, attempt, MAX_ATTEMPTS)
            return True
        except PyMongoError:
            logger.warning("Could not connect to %s (attempt %d/%d).", MONGO_SERVICE_NAME, attempt, MAX_ATTEMPTS)
            if attempt < MAX_ATTEMPTS:
                sleep(RETRY_DELAY_SECONDS)
        finally:
            client.close()

    logger.warning(
        "Could not connect to %s after %d attempts. The app will continue running, "
        "but %s-dependent features will fail until the connection is available.",
        MONGO_SERVICE_NAME,
        MAX_ATTEMPTS,
        MONGO_SERVICE_NAME,
    )
    return False


CONNECTION_CHECKS: list[tuple[str, Callable[[Flask], bool]]] = [
    (MONGO_SERVICE_NAME, check_mongo_connection),
]


def check_connections(app: Flask) -> None:
    for service_name, check_connection in CONNECTION_CHECKS:
        try:
            check_connection(app)
        except Exception:
            logger.exception("Unexpected error while checking the %s connection.", service_name)
