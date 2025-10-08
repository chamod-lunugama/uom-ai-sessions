from dataclasses import dataclass

@dataclass(frozen=True)
class LabConfig:
    """
    Configuration for the lab.
    TODO:
    """
    #Add type-hinted fields with sensible defaults:
    #sample_rate: int (e.g., 1000)
    sample_rate: int = 1000
    #duration_s: float (e.g., 2.0)
    duration_s: float = 2.0
    #noise_std: float (e.g., 0.15)
    noise_std: float = 0.15
    #median_window: int (e.g., 11)
    median_window: int = 11
    #cache_size: int (e.g., 256)  # for lru_cache in stretch
    cache_size: int = 256
    
    #TODO: implement the fields above
    pass
