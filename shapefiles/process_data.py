from pathlib import Path
from zipfile import ZipFile

import geopandas as gpd

SHAPEFILES_PATH = Path(__file__).parent


def unzip_worldbank_files(worldbank_shapefiles: Path = SHAPEFILES_PATH):
    worldbank_shapefiles = Path(worldbank_shapefiles)
    for zipfile in worldbank_shapefiles.glob("*.zip"):
        with ZipFile(zipfile, "r") as zipfh:
            zipfh.extractall(worldbank_shapefiles / zipfile.stem)


def process_worldbank_shapefile(worldbank_shapefiles: Path = SHAPEFILES_PATH):
    worldbank_shapefiles = Path(worldbank_shapefiles)
    for shapefile in worldbank_shapefiles.glob("**/*.shp"):
        df = gpd.read_file(shapefile).to_crs("EPSG:4326")
        df.to_parquet(worldbank_shapefiles / shapefile.with_suffix(".parquet").name)


def main():
    unzip_worldbank_files()
    process_worldbank_shapefile()


if __name__ == "__main__":
    main()
