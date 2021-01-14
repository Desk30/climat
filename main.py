import sys

from climat import retrieve_data, read_data, Settings, get_data_dir
from pathlib import Path
import argparse
import os
import shutil
from dotenv import load_dotenv

load_dotenv()

# noinspection PyTypeChecker
parser = argparse.ArgumentParser(description="climat", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument(
    "-f", action="store_true", help="Force redownload of specified data.", default=os.environ.get("force", False),
)
parser.add_argument(
    "-i",
    type=str,
    help="Input json file containing the instructions to download the data",
    default=os.environ.get("data_json", "default.json"),
)
parser.add_argument(
    "--clean",
    action="store_true",
    help="Deletes data corresponding to specified json",
)
parser.add_argument(
    "--cleanall",
    action="store_true",
    help="Deletes data corresponding to specified json",
)
args = parser.parse_args()

json_file = Path(args.i)

if not Settings.pdata.is_dir():
    Settings.pdata.mkdir()

if args.clean:
    zfile = Settings.pdata / json_file.with_suffix(".zip")
    if zfile.is_file():
        zfile.unlink()
    if (Settings.pdata / json_file.with_suffix("")).is_dir:
        shutil.rmtree(Settings.pdata / json_file.with_suffix(""))
    sys.exit()
if args.cleanall:
    if Settings.pdata.is_dir:
        shutil.rmtree(Settings.pdata)
    Settings.pdata.mkdir()
    sys.exit()

if not json_file.is_file():
    raise FileNotFoundError(f"No such file: {json_file}")
if json_file.is_dir():
    raise IsADirectoryError(str(json_file))

force = args.f
data_path = json_file.with_suffix(".zip")
retrieve_data(json_file, force)

# Test on example files (plotting should be moved to a dedicated function)
import matplotlib.pyplot as plt
fig, ax = plt.subplots()
ds_dict = read_data(get_data_dir(json_file), "12month*v03.grib")
for (key, ds) in ds_dict.items():
    print(key)
    print(ds.swvl1)
    ds.swvl1.plot()
    plt.show()
    break # Just test on 1 entry
