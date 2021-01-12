import shutil
from pathlib import Path
from climat import get, Settings

Settings.pdata = Path("tests/data")


def test_request():
    jsonfile = Path("tests/data/default_test.json")
    zfile = Settings.pdata / jsonfile.with_suffix(".zip")
    outdir = Settings.pdata / jsonfile.with_suffix("")

    if zfile.is_file():
        zfile.unlink()
    if outdir.is_dir():
        shutil.rmtree(outdir)

    get(jsonfile)
    assert not zfile.is_file()
    assert outdir.is_dir()
    assert len(list(outdir.glob("*"))) > 0
    zfile.unlink()
    shutil.rmtree(outdir)
