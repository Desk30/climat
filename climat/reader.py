from pathlib import Path
import xarray as xr
from typing import Dict


def read_data(dirpath: Path, pattern: str) -> Dict[str, xr.Dataset]:
    ds_dict = {}
    for data_file in dirpath.glob(pattern):
        print(f"Reading file {data_file}...")
        ds_dict[data_file.stem] = xr.open_dataset(data_file, engine="cfgrib")
    return ds_dict
