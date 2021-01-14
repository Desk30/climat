from pathlib import Path


class Settings:
    pdata = Path("data")


def get_data_dir(json_file: str):
    return Settings.pdata / json_file.stem
