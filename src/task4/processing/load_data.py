import tomllib
from pathlib import Path

import pandas as pd
import yaml

with Path("src/task4/config/config.toml").open("rb") as file:
    cfg = tomllib.load(file)
    yaml_file_path = cfg["input_data"]["yaml"]["path"]
    parquet_file_path = cfg["input_data"]["parquet"]["path"]
    csv_file_path = cfg["input_data"]["csv"]["path"]


def read_yaml(iteration: int):
    file_path = yaml_file_path.replace("$", str(iteration))
    with Path(file_path).open("r") as file:
        data = yaml.load(file, Loader=yaml.FullLoader)
        df = pd.DataFrame(data)
    return df


def read_parquet(iteration: int):
    file_path = parquet_file_path.replace("$", str(iteration))
    data = pd.read_parquet(file_path)
    return data


def read_csv(iteration: int):
    file_path = csv_file_path.replace("$", str(iteration))
    data = pd.read_csv(file_path)
    return data
