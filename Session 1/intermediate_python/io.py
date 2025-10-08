from pathlib import Path
import csv
import logging
from typing import Iterable, Sequence, List

def load_signal_csv(path: Path) -> list[float]:
    """
    Load a single-column CSV of floats into a list.
    TODO:
      - Validate that path exists and is a file; else raise FileNotFoundError
      - Read rows; parse as float; collect into list
      - Use try/except to catch ValueError and log it (then re-raise)
    """
    # TODO: implement
    if not path.is_file():
        raise FileNotFoundError(f"{path} does not exist or is not a file")
    signal: List[float] = []

    with open(path, 'r', newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        for i, row in enumerate(reader):
            if not row:
                continue
            if len(row) > 1:
                logging.warning(f"Row {i+1} has more than one column; using first column")
            try:
                value = float(row[0])
                signal.append(value)
            except ValueError as e:
                logging.error(f"Data type error in {path.name} at row {i+1}: Could not convert '{row[0]}' to float.")
                raise e
    return signal

def save_features_csv(path: Path, rows: Iterable[Sequence[float]]) -> None:
    """
    Save a CSV with header: rms,zero_crossings,peak_to_peak,mad
    TODO:
      - Ensure parent dir exists (mkdir parents=True, exist_ok=True)
      - Write header and rows via csv.writer
    """
    # TODO: implement
    path.parent.mkdir(parents=True, exist_ok=True)
    header = ["rms", "zero_crossings", "peak_to_peak", "mad"]
    with open(path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)
