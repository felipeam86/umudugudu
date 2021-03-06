from pathlib import Path
from zipfile import ZipFile

import geopandas as gpd

SHAPEFILES_PATH = Path(__file__).parent
PARQUETFILES_PATH = Path(__file__).parent.parent / "umudugudu" / "data"


def simplify_provinces(df):
    return df.Province.map(
        {
            "Kigali Town/Umujyi wa Kigali": "Kigali",
            "South/Amajyepfo": "South",
            "West/Iburengerazuba": "West",
            "North/Amajyaruguru": "North",
            "East/Iburasirazuba": "East",
        }
    )


def unzip_worldbank_files(worldbank_shapefiles: Path = SHAPEFILES_PATH):
    worldbank_shapefiles = Path(worldbank_shapefiles)
    for zipfile in worldbank_shapefiles.glob("*.zip"):
        with ZipFile(zipfile, "r") as zipfh:
            zipfh.extractall(worldbank_shapefiles / zipfile.stem)


def process_villages(df):
    provinces_ids = (
        df.groupby("Province")
        .province_id.value_counts()
        .rename("count")
        .sort_values(ascending=False)[:5]
        .reset_index(-1)
        .drop(columns=["count"])
        .province_id.to_dict()
    )
    df.loc[:, "province_id"] = df.Province.map(provinces_ids)
    df = (
        df.set_index("village_id")
        .rename(columns={"Name": "Village"})
        .assign(Province=simplify_provinces)
        .assign(Sector=lambda df: df.Sector.replace("Mageregere", "Mageragere"))
        .assign(
            Cell=lambda df: df.Cell.replace(
                [
                    "Munanira Ii",
                    "Nyakabanda Ii",
                    "Kabuguru Ii",
                    "Rwezamenyo Ii",
                    "Rukiri Ii",
                    "Kabuga Ii",
                    "Rugarama Ii",
                    "Rukomo Ii",
                    "Rukomo Ii",
                ],
                [
                    "Munanira II",
                    "Nyakabanda II",
                    "Kabuguru II",
                    "Rwezamenyo II",
                    "Rukiri II",
                    "Kabuga II",
                    "Rugarama II",
                    "Rukomo II",
                    "Rukomo II",
                ],
            )
        )
    )

    df.loc["11050304", "Cell"] = "Mataba"  # Wrongly assigned to 'Mwendo'
    df.to_parquet(PARQUETFILES_PATH / "Village.parquet")
    return df


def process_cells(df, provinces):
    df = (
        df.set_index("cell_id")
        .rename(columns={"Name": "Cell"})
        .assign(Province=lambda df: df.province_id.map(provinces))
        .assign(Sector=lambda df: df.Sector.replace("Mageregere", "Mageragere"))
        .assign(
            Cell=lambda df: df.Cell.replace(
                [
                    "Munanira i",
                    "Nyakabanda i",
                    "Kabuguru i",
                    "Rwezamenyo i",
                    "Rukiri i",
                    "Kabuga i",
                    "Rugarama i",
                    "Rukomo i",
                    "Rukomo i",
                ],
                [
                    "Munanira I",
                    "Nyakabanda I",
                    "Kabuguru I",
                    "Rwezamenyo I",
                    "Rukiri I",
                    "Kabuga I",
                    "Rugarama I",
                    "Rukomo I",
                    "Rukomo I",
                ],
            )
        )
        .assign(
            Cell=lambda df: df.Cell.replace(
                [
                    "Munanira ii",
                    "Nyakabanda ii",
                    "Kabuguru ii",
                    "Rwezamenyo ii",
                    "Rukiri ii",
                    "Kabuga ii",
                    "Rugarama ii",
                    "Rukomo ii",
                    "Rukomo ii",
                ],
                [
                    "Munanira II",
                    "Nyakabanda II",
                    "Kabuguru II",
                    "Rwezamenyo II",
                    "Rukiri II",
                    "Kabuga II",
                    "Rugarama II",
                    "Rukomo II",
                    "Rukomo II",
                ],
            )
        )
    )
    df.to_parquet(PARQUETFILES_PATH / "Cell.parquet")
    return df


def process_sectors(df, provinces):
    df = (
        df.set_index("sector_id")
        .rename(columns={"Name": "Sector"})
        .assign(Province=lambda df: df.province_id.map(provinces))
        .assign(Sector=lambda df: df.Sector.replace("Mageregere", "Mageragere"))
    )
    df.loc["4116", "Sector"] = "Shyorongi"  # It is misspelled as Shyrongi
    df.to_parquet(PARQUETFILES_PATH / "Sector.parquet")

    return df


def process_districts(df_districts, df_villages):
    df_districts = df_districts.set_index("district_id").join(
        df_villages[["district_id", "province_id", "Province"]]
        .drop_duplicates()
        .set_index("district_id")
    )[["province_id", "Province", "District", "geometry"]]
    df_districts.to_parquet(PARQUETFILES_PATH / "District.parquet")

    return df_districts


def make_province_geometries(df_districts):
    df = (
        df_districts.groupby(["province_id", "Province"])
        .geometry.apply(lambda df: df.unary_union)
        .to_frame()
        .reset_index()
        .set_index("province_id")
        .set_crs("EPSG:4326")
    )

    df.to_parquet(PARQUETFILES_PATH / "Province.parquet")
    return df


def process_worldbank_shapefile(worldbank_shapefiles: Path = SHAPEFILES_PATH):
    PARQUETFILES_PATH.mkdir(exist_ok=True)
    worldbank_shapefiles = Path(worldbank_shapefiles)

    def read(shapefile: Path):
        df = gpd.read_file(shapefile).to_crs("EPSG:4326")
        for col in df.columns:
            if "_ID" in col:
                df.loc[:, col] = df.loc[:, col].map(int).map(str)
        return df.rename(
            columns={
                "Prov_ID": "province_id",
                "Dist_ID": "district_id",
                "Distr_ID": "district_id",
                "Sect_ID": "sector_id",
                "Village_ID": "village_id",
                "Cell_ID": "cell_id",
            }
        )

    df_villages = read(worldbank_shapefiles / "rwa_villages" / "Village.shp")
    df_cells = read(worldbank_shapefiles / "rwa_cell" / "Cell.shp")
    df_sectors = read(worldbank_shapefiles / "rwa_sector" / "Sector.shp")
    df_districts = read(worldbank_shapefiles / "rwa_district" / "District.shp")

    df_villages = process_villages(df_villages)
    provinces = (
        df_villages[["province_id", "Province"]]
        .drop_duplicates()
        .set_index("province_id")
        .Province.to_dict()
    )
    df_cells = process_cells(df_cells, provinces)
    df_sectors = process_sectors(df_sectors, provinces)
    df_districts = process_districts(df_districts, df_villages)
    df_provinces = make_province_geometries(df_districts)


def main():
    unzip_worldbank_files()
    process_worldbank_shapefile()


if __name__ == "__main__":
    main()
