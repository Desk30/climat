import xarray as xr
import dask.array as da
from dask.distributed import Client
from pathlib import Path

if __name__ == '__main__':
    cli = Client()

    chunk_space = 1114111
    chunk_time = 50

    main_folder = "/work/bm0834/k203095/ICON_LEM_DE/"
    file_prefix = "2d_cloud_day"
    domain = "DOM01"
    folders = ["20130620-default-ifs"]
    variable = "swvl1"

    filenames = list(Path("data/default").glob("*"))
    temps = [xr.open_dataset(fn, chunks={"number": 1}, engine='cfgrib').variables[variable] for fn in filenames]

    arrays = [da.from_array(t) for t in temps]
    var_normal = da.concatenate(arrays, axis=0)
    mean = var_normal.mean(axis=1)
    mean = mean.persist()
    print(mean)
