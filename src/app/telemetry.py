import time
from contextlib import contextmanager
from typing import Dict

metrics: Dict[str, float] = {}


def record_metric(name: str, value):
    metrics[name] = metrics.get(name, 0) + value


@contextmanager
def record_latency(name: str):
    start = time.time()
    try:
        yield
    finally:
        elapsed = time.time() - start
        record_metric(f"latency.{name}", elapsed)
