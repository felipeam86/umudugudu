from pathlib import Path

import geopandas as gpd

PARQUETFILES_PATH = Path(__file__).parent / "data"


def get_villages():
    parquet_file = PARQUETFILES_PATH / "Village.parquet"

    if not parquet_file.exists():
        raise ValueError("Parquet file does not exist")

    return gpd.read_parquet(parquet_file)


def get_cells():
    parquet_file = PARQUETFILES_PATH / "Cell.parquet"

    if not parquet_file.exists():
        raise ValueError("Parquet file does not exist")

    return gpd.read_parquet(parquet_file)


def get_sectors():
    parquet_file = PARQUETFILES_PATH / "Sector.parquet"

    if not parquet_file.exists():
        raise ValueError("Parquet file does not exist")

    return gpd.read_parquet(parquet_file)


def get_districts():
    parquet_file = PARQUETFILES_PATH / "District.parquet"

    if not parquet_file.exists():
        raise ValueError("Parquet file does not exist")

    return gpd.read_parquet(parquet_file)


def get_provinces():
    parquet_file = PARQUETFILES_PATH / "Province.parquet"

    if not parquet_file.exists():
        raise ValueError("Parquet file does not exist")

    return gpd.read_parquet(parquet_file)
