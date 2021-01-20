from pathlib import Path
from zipfile import ZipFile

import geopandas as gpd

SHAPEFILES_PATH = Path(__file__).parent


def unzip_worldbank_files(worldbank_shapefiles: Path = SHAPEFILES_PATH):
    worldbank_shapefiles = Path(worldbank_shapefiles)
    for zipfile in worldbank_shapefiles.glob("*.zip"):
        with ZipFile(zipfile, "r") as zipfh:
            zipfh.extractall(worldbank_shapefiles / zipfile.stem)


def clean_province_ids(df):
    provinces_ids = (
        df.groupby("Province")
            .Prov_ID.value_counts()
            .rename("count")
            .sort_values(ascending=False)[:5]
            .reset_index(-1)
            .drop(columns=["count"])
            .Prov_ID.to_dict()
    )
    df.loc[:, "Prov_ID"] = df.Province.map(provinces_ids)

    return df


def process_worldbank_shapefile(worldbank_shapefiles: Path = SHAPEFILES_PATH):
    worldbank_shapefiles = Path(worldbank_shapefiles)
    for shapefile in worldbank_shapefiles.glob("**/*.shp"):
        df = gpd.read_file(shapefile).to_crs("EPSG:4326")
        df.to_parquet(worldbank_shapefiles / shapefile.with_suffix(".parquet").name)
        if shapefile.name == "Village.shp":
            print("cleaning")
            df = clean_province_ids(df)


def main():
    unzip_worldbank_files()
    process_worldbank_shapefile()


if __name__ == "__main__":
    main()
