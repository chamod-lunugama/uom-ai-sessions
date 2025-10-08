# Optional CLI using typer
import typer, logging, time, math, csv
from typing import Callable, TypeVar, Any, List, Sequence, Iterable, Iterator, Optional
from pathlib import Path
import numpy as np
from .io import load_signal_csv, save_features_csv
from .features import feature_vector

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

# --- Utility Functions (for chunks) ---
T = TypeVar("T", int, float)

def chunks(iterable: Iterable[T], size: int) -> Iterator[List[T]]:
    """Yield lists of length `size` from `iterable`. Last chunk may be shorter."""
    if size <= 0:
        raise ValueError("Chunk size must be positive")
        
    buffer: List[T] = []
    for item in iterable:
        buffer.append(item)
        if len(buffer) == size:
            yield buffer
            buffer = []
    
    if buffer:
        yield buffer

# --- RMS Implementations and Timing (for profile command) ---

def python_rms(seq: Sequence[float]) -> float:
    """Pure-Python RMS implementation."""
    if not seq:
        return 0.0
    sum_of_squares = sum(x * x for x in seq)
    return math.sqrt(sum_of_squares / len(seq))

def numpy_rms(arr: np.ndarray) -> float:
    """NumPy-vectorized RMS implementation."""
    if arr.size == 0:
        return 0.0
    return np.sqrt(np.mean(arr**2)).item()

def timed(fn: Callable, *args: Any, **kwargs: Any) -> float:
    """Simple helper to time a function execution and return time in ms."""
    start = time.perf_counter()
    fn(*args, **kwargs)
    end = time.perf_counter()
    return (end - start) * 1000 # returns ms

# --- Feature Extraction (for run_pipeline command) ---

def feature_vector(x: np.ndarray) -> List[float]:
    """
    Compute basic features for 1D signal x: RMS, zero-crossings, peak-to-peak, MAD.
    Return as [rms, zc, p2p, mad].
    """
    if x.size == 0:
        return [0.0, 0.0, 0.0, 0.0]

    rms = np.sqrt(np.mean(x**2))
    zero_crossings = np.count_nonzero(np.diff(np.sign(x)))
    p2p = np.max(x) - np.min(x)
    mad = np.mean(np.abs(np.diff(x)))

    return [rms.item(), float(zero_crossings), p2p.item(), mad.item()]

# --- CSV I/O (for generate_data and run_pipeline commands) ---

def load_signal_csv(path: Path) -> List[float]:
    """Load a single-column CSV of floats into a list."""
    if not path.is_file():
        raise FileNotFoundError(f"Signal file not found at: {path}")

    signal: List[float] = []
    with open(path, 'r', newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        for i, row in enumerate(reader):
            if not row: continue
            try:
                signal.append(float(row[0]))
            except ValueError as e:
                logging.error(f"Data type error in {path.name} at row {i+1}: Could not convert '{row[0]}' to float.")
                raise e
    return signal

def save_features_csv(path: Path, rows: Iterable[Sequence[float]]) -> None:
    """Save a CSV with header: rms,zero_crossings,peak_to_peak,mad"""
    path.parent.mkdir(parents=True, exist_ok=True)
    
    header = ["rms", "zero_crossings", "peak_to_peak", "mad"]
    
    with open(path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)

app = typer.Typer(help="Intermediate Python Lab CLI")

@app.command()
def generate_data(
    out: Path = typer.Option(Path("data/signal.csv"), help="Output CSV path"),
    n: int = 4000,
    noise: float = 0.15
):
    """
    Generate synthetic signal data (sine + square mixture) and save to CSV.
    TODO:
      - Implement signal synthesis similar to dataset seeded in data/signal.csv
    """
    logging.info(f"Generating {n} samples with noise {noise} to {out}")
    t = np.linspace(0, 4*np.pi, n, endpoint=False)
    sine_wave = np.sin(t*1.5)
    square_wave = np.sign(np.sin(t*0.5))*0.5
    signal = sine_wave + square_wave
    signal += np.random.randn(n) * noise
    out.parent.mkdir(parents=True, exist_ok=True)

    with open(out, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows([[x] for x in signal])
    logging.info(f"Data saved to {out.resolve()}")

@app.command()
def run_pipeline(
    inp: Path = typer.Argument(Path("data/signal.csv"), help="Input CSV path"),
    out: Path = typer.Option(Path("data/features.csv"), help="Output CSV path"),
    chunk: int = 256
):
    """
    Stream the input CSV in chunks, compute features per chunk, and save to CSV.
    TODO:
      - Use load_signal_csv, slice into chunks, compute feature_vector on each chunk (np.array)
      - Save with save_features_csv
    """
    logging.info(f"Running feature extraction pipeline ...")
    try:
        signal_list = load_signal_csv(inp)
    except FileNotFoundError as e:
        typer.echo(f"Error: {e}")
        raise typer.Exit(code=1)
    
    features_rows: List[Sequence[float]] = []
    typer.echo(f"Processing {len(signal_list)} samples in chunks of {chunk}")

    for i, chunk_list in enumerate(chunks(signal_list, chunk)):
        chunk_arr = np.array(chunk_list, dtype=np.float64)
        features = feature_vector(chunk_arr)
        features_rows.append(features)

        if (i+1)%10 == 0:
            typer.echo(f"Processed {i+1} chunks...")
            save_features_csv(out, features_rows)
            logging.info(f"Feature extraction complete. Saved {len(features_rows)} feature vectors to {out.resolve()}")

@app.command()
def profile(
    size: int = typer.Option(int(1e6), help="Number of random floats to generate")
):
    """
    Profile Python vs NumPy RMS on a large array and print timings.
    TODO:
      - Create 1e6 random floats (np.random.randn)
      - Time pure-python and numpy versions; print ms
    """
    typer.echo("TODO: implement profile")

    test_array = np.random.randn(size)
    test_list = test_array.tolist()

    typer.echo(f"Test Array Size: {size:,}")
    time_py = timed(python_rms, test_list)
    typer.echo(f"Pure Python RMS: {time_py:.2f} ms")
    time_np = timed(numpy_rms, test_array)
    typer.echo(f"NumPy RMS: {time_np:.2f} ms")

    if time_np > 0:
        speedup = time_py / time_np
        typer.echo(f"NumPy is {speedup:.1f}x faster than pure Python")

if __name__ == "__main__":
    app()
