import logging
import os
import sys
from argparse import ArgumentParser
from logging.handlers import TimedRotatingFileHandler

from dns_health_exporter import exporter

parser = ArgumentParser(
    description=(
        "DNS health monitor, exporting metrics to prometheus.\n"
        "Checks DNS for specified hosts every minute, and logs the health"
    )
)
parser.add_argument(
    "hosts", metavar="N", type=str, nargs="*", help=f"List of hosts to check. Defaults: {exporter.DEFAULT_HOSTS}"
)
parser.add_argument(
    "--port", dest="port", type=int, help=f"Prometheus metrics endpoint port. Default: {exporter.DEFAULT_PORT}"
)
parser.add_argument(
    "--sleep", dest="sleep", type=int,
    help=f"Number of seconds to sleep between checks. Default: {exporter.DEFAULT_SLEEP}"
)


def setup_logging() -> None:
    os.makedirs("logs", exist_ok=True)
    formatter = logging.Formatter("{asctime}:{levelname}:{name}:{message}", style="{")

    base_logger = logging.getLogger()
    base_logger.setLevel(logging.INFO)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    base_logger.addHandler(console_handler)

    # debug log, for diagnosing any DNS issues.
    debug_logger = logging.getLogger("dns_health_exporter")
    debug_logger.setLevel(logging.DEBUG)
    file_handler = TimedRotatingFileHandler("logs/dns_health.log", when="midnight")
    file_handler.setFormatter(formatter)
    debug_logger.addHandler(file_handler)


if __name__ == "__main__":
    setup_logging()
    args = parser.parse_args()
    exporter.monitor_hosts(args.hosts, port=args.port, sleep=args.sleep)
