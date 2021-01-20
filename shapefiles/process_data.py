from pathlib import Path
from zipfile import ZipFile

import geopandas as gpd

SHAPEFILES_PATH = Path(__file__).parent
PARQUETFILES_PATH = Path(__file__).parent.parent / "umudugudu" / "data"


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


def clean_district_ids(df):
    df.loc[:, "Dist_ID"] = df.loc[:, "Dist_ID"].map(int).map(str)
    return df


def process_worldbank_shapefile(worldbank_shapefiles: Path = SHAPEFILES_PATH):
    PARQUETFILES_PATH.mkdir(exist_ok=True)
    worldbank_shapefiles = Path(worldbank_shapefiles)
    for shapefile in worldbank_shapefiles.glob("**/*.shp"):
        df = gpd.read_file(shapefile).to_crs("EPSG:4326")
        if shapefile.name == "Village.shp":
            df = clean_province_ids(df)
        if shapefile.name == "District.shp":
            df = clean_district_ids(df)
        df.to_parquet(PARQUETFILES_PATH / shapefile.with_suffix(".parquet").name)


def make_province_geometries():
    df_districts = data.get_districts()
    df_d = (
        df[["Province", "Prov_ID", "Distr_ID"]].drop_duplicates().set_index("Distr_ID")
    )
    df_districts = df_districts.join(df_d)


def main():
    unzip_worldbank_files()
    process_worldbank_shapefile()


if __name__ == "__main__":
    main()
