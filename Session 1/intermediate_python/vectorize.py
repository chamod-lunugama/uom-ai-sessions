from typing import Sequence
import numpy as np
import math

def python_rms(seq: Sequence[float]) -> float:
    """
    Pure-Python RMS implementation.
    TODO:
      - sum of squares / len, then sqrt (use math.sqrt)
    """
    # TODO: implement
    if not seq:
       return 0.0
    sum_of_squares = sum(x * x for x in seq)
    mean_of_squares = sum_of_squares / len(seq)
    return math.sqrt(mean_of_squares)

def numpy_rms(arr: np.ndarray) -> float:
    """
    NumPy-vectorized RMS implementation.
    TODO:
      - Use np.mean and vectorized operations; return float
    """
    # TODO: implement
    if arr.size == 0:
       return 0.0
    mean_of_squares = np.mean(arr ** 2)
    return np.sqrt(mean_of_squares).item()
