from contextlib import contextmanager
import time
import logging
from typing import Iterator

@contextmanager
def timer(label: str) -> Iterator[None]:
    """
    Context manager that logs how long the block took (in ms).
    TODO:
      - Record start time
      - Yield control
      - On exit, compute elapsed ms and log with INFO level using logging.info
    """
    #TODO: implement
    start_time = time.perf_counter()
    try:
      yield
    finally:
      end_time = time.perf_counter()
      elapsed_ms = (end_time - start_time) * 1000
      logging.info(f"{label} took {elapsed_ms:.2f} ms")

@contextmanager
def suppress_and_log(*exc_types: type[BaseException]) -> Iterator[None]:
    """
    Context manager that suppresses given exception types and logs the exception.
    Example:
        with suppress_and_log(ValueError):
            int("not int")  # won't crash; logs the error
    TODO:
      - Wrap the body in try/except for the given exc_types
      - On exception, log with logging.exception and do NOT re-raise
    """
    # TODO: implement
    try:
       yield
    except exc_types as e:
       logging.exception(f"Suppressed exception: {e.__class__.__name__}")
