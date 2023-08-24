import logging
import sentry_sdk
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration
from sentry_sdk.integrations.logging import LoggingIntegration
from sentry_sdk import capture_message

# sentry_logging = LoggingIntegration(
#     level=logging.DEBUG,
#     event_level=logging.ERROR,
# )

sentry_sdk.init(
    dsn="https://1a9822b93f9d3590febc7538c806553c@o4505753981026304.ingest.sentry.io/4505754045120512",
    integrations=[
        SqlalchemyIntegration(),
        # sentry_logging,
    ],
    debug=True,
    traces_sample_rate=1.0,
)
division_by_zero = 1 / 0

logging.debug("i am debug")
logging.info("i am info")
logging.error("i am error")
logging.exception("i am exception")


def pouet():
    print("poeut")
    logging.debug("i am debug")
    logging.info("i am info")
    logging.error("i am error")
    logging.exception("i am exception")
