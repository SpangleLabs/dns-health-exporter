#!/usr/bin/python
import socket
import time
import logging
from contextlib import contextmanager
from typing import List, Optional, ContextManager

from prometheus_client import start_http_server, Counter, Histogram

DEFAULT_HOSTS = ["google.com"]
DEFAULT_PORT = 8080
DEFAULT_SLEEP = 60

DNS_QUERY_TIME = Histogram(
    "dns_health_latency_seconds",
    "Time taken to lookup hostname",
    labelnames=["host"],
    buckets=[
        1 / 10 ** 6, 10 / 10 ** 6, 100 / 10 ** 6,
        1 / 10 ** 3, 10 / 10 ** 3, 100 / 10 ** 3,
        1, 10, 100
    ]
)
DNS_REQUESTS = Counter("dns_health_request_count", "Total count of DNS requests", labelnames=["host"])
DNS_FAILURES = Counter("dns_health_failure_count", "Total count of DNS lookup failures", labelnames=["host"])

logger = logging.getLogger(__name__)


@contextmanager
def time_query(hostname: str) -> ContextManager:
    start = time.perf_counter()
    yield
    end = time.perf_counter()
    logger.warning("Time taken: %s", end - start)
    DNS_QUERY_TIME.labels(host=hostname).observe(end - start)


def run_test(hostname: str):
    logger.info("Looking up %s", hostname)
    DNS_REQUESTS.labels(host=hostname).inc()
    try:
        with time_query(hostname):
            socket.gethostbyname(hostname)
    except Exception as e:
        logger.warning("Failed to lookup host: %s", hostname)
        logger.debug(e, exc_info=True)
        DNS_FAILURES.labels(host=hostname).inc()


def monitor_hosts(hosts: Optional[List[str]], port: int = DEFAULT_PORT, sleep: int = DEFAULT_SLEEP) -> None:
    # Set up arguments
    if not hosts:
        hosts = DEFAULT_HOSTS
    port = port or DEFAULT_PORT
    sleep = sleep or DEFAULT_SLEEP
    # Set up labels
    for host in hosts:
        DNS_QUERY_TIME.labels(host=host)
        DNS_REQUESTS.labels(host=host)
        DNS_FAILURES.labels(host=host)
    start_http_server(port)
    # Start monitor
    while True:
        logger.info("Running DNS test")
        for hostname in hosts:
            run_test(hostname)
        logger.info("Waiting %s seconds before the next test", sleep)
        time.sleep(sleep)
