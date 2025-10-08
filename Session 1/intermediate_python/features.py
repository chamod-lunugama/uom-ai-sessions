import numpy as np
from typing import Sequence

def feature_vector(x: np.ndarray) -> list[float]:
    """
    Compute basic features for 1D signal x:
      - RMS
      - zero-crossings (count)
      - peak-to-peak (max - min)
      - mean absolute diff (MAD)
    Use NumPy vectorized ops only.
    Return as [rms, zc, p2p, mad].
    TODO: implement.
    """
    # TODO: implement
    if x.size == 0:
      return [0.0, 0.0, 0.0, 0.0]
    rms = np.sqrt(np.mean(x ** 2))
    zero_crossings = np.count_nonzero(np.diff(np.sign(x)))
    peak_to_peak = np.max(x) - np.min(x)
    mad = np.mean(np.abs(np.diff(x)))
    return [rms.item(), float(zero_crossings), peak_to_peak.item(), mad.item()]
