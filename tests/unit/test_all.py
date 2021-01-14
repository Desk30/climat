import shutil
from pathlib import Path
from climat import retrieve_data, Settings

Settings.pdata = Path("tests/data")


def test_request():
    jsonfile = Settings.pdata / "default_test.json"
    zfile = jsonfile.with_suffix(".zip")
    outdir = jsonfile.with_suffix("")

    if zfile.is_file():
        zfile.unlink()
    if outdir.is_dir():
        shutil.rmtree(outdir)

    retrieve_data(jsonfile)
    assert not zfile.is_file()
    assert outdir.is_dir()
    assert len(list(outdir.glob("*"))) > 0
    shutil.rmtree(outdir)
