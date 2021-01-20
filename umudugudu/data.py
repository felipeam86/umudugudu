from pathlib import Path

import geopandas as gpd

PARQUETFILES_PATH = Path(__file__).parent / "data"


def get_villages():
    parquet_file = PARQUETFILES_PATH / "Village.parquet"

    if not parquet_file.exists():
        raise ValueError("Parquet file does not exist")

    return gpd.read_parquet(parquet_file).set_index("Village_ID")


def get_districts():
    parquet_file = PARQUETFILES_PATH / "District.parquet"

    if not parquet_file.exists():
        raise ValueError("Parquet file does not exist")

    return gpd.read_parquet(parquet_file).set_index("Dist_ID")
