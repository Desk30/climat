import cdsapi
import zipfile
import json
from .settings import Settings, get_data_dir
from pathlib import Path


def retrieve_data(json_file: Path, force: bool = False):
    outdir = get_data_dir(json_file)
    zfile = Settings.pdata / f"{json_file.stem}.zip"
    if not force:
        if outdir.is_dir():
            print(f"Data found at {outdir}. Skipping download.")
            return
        elif zfile.is_file():
            extract(zfile)
            return

    download(json_file, zfile)
    extract(zfile)


def download(json_file: Path, zfile: Path):
    """Downloads the data specified by 'default.json' in data/download.zip

    Requires a valid cds account. Go to https://cds.climate.copernicus.eu/api-how-to#install-the-cds-api-key
    for more information."""

    try:
        c = cdsapi.Client()
    except Exception as e:
        if "Missing/incomplete configuration file" in str(e):
            raise ConnectionError(
                f"{str(e)}\nPlease go to"
                " https://cds.climate.copernicus.eu/api-how-to#install-the-cds-api-key and follow the instructions"
            )
        raise e

    with open(json_file, "r") as ifile:
        to_get = json.load(ifile)

    c.retrieve("ecv-for-climate-change", to_get, str(zfile))


def extract(zfile_path: Path):
    zfile = zipfile.ZipFile(zfile_path)
    outdir = zfile_path.with_suffix("")
    if not outdir.is_dir():
        if outdir.exists():
            raise FileExistsError("Output directory exists and is not a directory : {outdir}")
        outdir.mkdir()
    zfile.extractall(outdir)
    zfile_path.unlink()
