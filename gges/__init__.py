import os
from pathlib import Path

__all__ = ["data_path"]

data_path = Path(__file__).parent.joinpath('data')