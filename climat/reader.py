from pathlib import Path
from netCDF4 import Dataset
from typing import Dict


def get_all_data(dirpath: Path) -> Dict[str, Dataset]:
    dfs = {}
    for afile in dirpath.glob("*.nc"):
        print(f"Reading file {afile}...")
        dfs[afile.stem] = Dataset(afile)
    return dfs
