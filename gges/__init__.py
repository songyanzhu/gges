import os
import sys
import subprocess
import importlib
from pathlib import Path

__all__ = ["data_path"]

data_path = Path(__file__).parent.joinpath('data')


def _install(package: str) -> None:
    """Install a PyPI package into the current Python environment."""
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def _try_import(
    import_name: str,
    pip_name: str,
    alias: str | None = None,
    extra_pip: list[str] | None = None,
):
    """
    Attempt to import a module by name; install it via pip if missing,
    and optionally assign it to an alias in the global namespace.

    Args:
        import_name (str)       : The module name used in `import <name>`.
                                  Example: 'xarray'.
        pip_name    (str)       : The PyPI package name used for pip install.
                                  Usually the same as import_name.
                                  Example: 'xarray'.
        alias       (str, optional) : Optional name to assign the module to in
                                  globals(), simulating `import module as alias`.
                                  Example: alias='xr' for xarray.
        extra_pip   (list[str], optional) : Additional PyPI packages to install
                                  alongside the main one (e.g., ['netCDF4']).

    Returns:
        module : The imported module object. Can be used directly if no alias
                 is provided.
    """
    try:
        module = importlib.import_module(import_name)
    except ModuleNotFoundError:
        print(f"Module '{import_name}' not found — geoxai is installing '{pip_name}' for you...")
        _install(pip_name)
        if extra_pip:
            for pkg in extra_pip:
                _install(pkg)
        module = importlib.import_module(import_name)

    if alias:
        globals()[alias] = module

    return module

np = _try_import("numpy",     "numpy")
pd = _try_import("pandas",    "pandas")
matplotlib = _try_import("matplotlib", "matplotlib")
rio = _try_import("rasterio",  "rasterio")
gpd = _try_import("geopandas", "geopandas")
xr = _try_import("xarray",    "xarray")
rxr = _try_import("rioxarray", "rioxarray")
sns = _try_import("seaborn", "seaborn")