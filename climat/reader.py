from pathlib import Path
import xarray as xr
from typing import Dict, Union


expected_variables = [
    "1month_anomaly_Global_ea_swvl1",
    "1month_anomaly_Global_ei_swvl1",
    "1month_mean_Global_ea_swvl1",
    "1month_mean_Global_ei_swvl1",
    "12month_anomaly_Global_ea_swvl1",
    "12month_anomaly_Global_ei_swvl1",
    "climatology_0.25g_ea_swvl1",
    "climatology_0.25g_ei_swvl1"
]


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

    grouped_files = group_files_by_variable(list(dirpath.glob(pattern)))

    for var in grouped_files:
        if len(grouped_files[var]) > 0:
            print(f"Loading files for variable {var}...")
            ds_dict[var] = read_crib(grouped_files[var])
    return ds_dict


def read_crib(data_file, chunks: Union[dict, None] = None):
    if isinstance(data_file, (list, tuple)):
        return xr.open_mfdataset(data_file, engine="cfgrib", parallel=True, chunks=chunks)
    else:
        return xr.open_dataset(data_file, engine="cfgrib", chunks=chunks)


def group_files_by_variable(files):
    grouped_files = {var: [] for var in expected_variables}
    for var in expected_variables:
        print(var)
        for f_ in files:
            if f_.suffix != ",grib" or f_.suffix != ".grb":
                if var in f_.stem:
                    grouped_files[var].append(f_)
            else:
                raise ValueError(f"Unexpected file type : {f_.suffix}")
    return grouped_files
