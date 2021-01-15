from pathlib import Path
import xarray as xr
from typing import Dict


def read_data(dirpath: Path, pattern: str) -> Dict[str, xr.Dataset]:
    """
    Read all files matching a pattern and return the data as a dictionary.

    Supported types:
    - grib

    Parameters
    ----------
    dirpath: Path
        The data directory.
    pattern: str
        A pattern for filtering the files.

    Returns
    -------
        Dict[str, netCDF4._netCDF4.Dataset]: The data indexed by data file stem.
    """
    ds_dict = {}
    for data_file in dirpath.glob(pattern):
        print(f"Reading file {data_file}...")
        file_extension = data_file.suffix
        if file_extension == ".grib":
            ds_dict[data_file.stem] = xr.open_dataset(data_file, engine="cfgrib")
        else:
            raise TypeError(f"unsupported data type {file_extension}")
    return ds_dict
