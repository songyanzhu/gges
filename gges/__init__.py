import importlib
from pathlib import Path
import subprocess
import sys

__all__ = ["data_path", "np", "pd", "plt", "rio", "gpd", "xr", "rxr", "sns", "functions"]

data_path = Path(__file__).parent.joinpath('data')


def _install(package: str) -> None:
    """Install a PyPI package into the current Python environment."""
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])


def _try_import(
    import_name: str,
    pip_name: str,
    extra_pip: list[str] | None = None,
):
    """
    Attempt to import a module; install via pip if missing.
    """
    try:
        return importlib.import_module(import_name)
    except ModuleNotFoundError:
        print(f"Module '{import_name}' not found — geoxai is installing '{pip_name}'...")
        try:
            _install(pip_name)
            if extra_pip:
                for pkg in extra_pip:
                    _install(pkg)
            # Invalidate import caches to discover newly installed packages in site-packages
            importlib.invalidate_caches()
            return importlib.import_module(import_name)
        except Exception as e:
            raise RuntimeError(
                f"Failed to auto-install or import '{import_name}' (pip package: '{pip_name}'). "
                f"Please install it manually."
            ) from e


# Auto-load common data science and geospatial libraries
np = _try_import("numpy", "numpy")
pd = _try_import("pandas", "pandas")
plt = _try_import("matplotlib.pyplot", "matplotlib")
rio = _try_import("rasterio", "rasterio")
gpd = _try_import("geopandas", "geopandas")
xr = _try_import("xarray", "xarray", extra_pip=["netCDF4"])  # xarray reading/writing NetCDF typically requires netCDF4
rxr = _try_import("rioxarray", "rioxarray")
sns = _try_import("seaborn", "seaborn")

from . import functions