from collections import deque
from statistics import median
from typing import Iterable, Iterator, TypeVar, Deque, Optional

T = TypeVar("T", int, float)

def chunks(iterable: Iterable[T], size: int) -> Iterator[list[T]]:
    """
    Yield lists of length `size` from `iterable`. Last chunk may be shorter.
    TODO:
      - Accumulate items into a buffer
      - Yield buffer when size reached; clear and continue
    """
    # TODO: implement
    if size <= 0:
        raise ValueError("Chunk size must be positive")
    buffer: list[T] = []
    for item in iterable:
        buffer.append(item)
        if len(buffer) == size:
            yield buffer
            buffer = []
    if buffer:
        yield buffer

def moving_average(window: int):
    """
    Stateful GENERATOR that yields the moving average each time a new value is sent.
    Usage:
        gen = moving_average(5); next(gen)
        out = gen.send(3.0)  # returns current average
    TODO:
      - Keep a deque(maxlen=window)
      - On each .send(x): append x and yield average (sum/len)
    """
    # TODO: implement
    if window <= 0:
        raise ValueError("Window size must be positive")
    window_data: Deque[float] = deque(maxlen=window)
    value: Optional[float] = None

    while True:
        value = yield None if not window_data else sum(window_data) / len(window_data)
        if value is not None:
            window_data.append(float(value))

def moving_median(window: int):
    """
    Stateful GENERATOR that yields the moving median each time a new value is sent.
    TODO: mirror moving_average but compute statistics.median over the deque.
    """
    # TODO: implement
    if window <= 0:
        raise ValueError("Window size must be positive")
    window_data: Deque[float] = deque(maxlen=window)
    value: Optional[float] = None

    while True:
        result = None 
        if window_data:
            result = median(list(window_data))
        value = yield result
        if value is not None:
            window_data.append(float(value))
