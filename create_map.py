import json
from pathlib import Path

import geopandas as gpd
import plotly.express as px

SHAPEFILES_PATH = Path("rwa_villages")


def process_worldbank_shapefile():
    df = gpd.read_file(SHAPEFILES_PATH / "Village.shp").to_crs("EPSG:4326")
    df.to_parquet(SHAPEFILES_PATH / "Village.parquet")


def get_villages():
    parquet_file = SHAPEFILES_PATH / "Village.parquet"

    if not parquet_file.exists():
        process_worldbank_shapefile()

    return gpd.read_parquet(parquet_file)


def read_geojson(geojson_file):

    with open(geojson_file) as geofile:
        geojson = json.load(geofile)

    for feature in geojson["features"]:
        feature["id"] = feature["properties"]["Village_ID"]

    return geojson


def get_data():
    df = get_villages()
    df_kigali = df.query("Province == 'Kigali Town/Umujyi wa Kigali'")
    df_kigali.to_file("rwa_villages/Village_Kigali.geojson", driver="GeoJSON")
    geo_kigali = read_geojson("rwa_villages/Village_Kigali.geojson")

    return df_kigali, geo_kigali


if __name__ == "__main__":

    df_kigali, geo_kigali = get_data()
    fig = px.choropleth_mapbox(
        df_kigali,
        geojson=geo_kigali,
        locations="Village_ID",
        color="District",
        color_continuous_scale="Viridis",
        mapbox_style="open-street-map",
        featureidkey="properties.Village_ID",
        zoom=11,
        center={"lat": -1.953402, "lon": 30.090357},
        opacity=0.2,
        labels={"Name": "Village/Umudugudu"},
        hover_name="Name",
        hover_data=["District", "Sector", "Cell"],
    )
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    export_folder = Path("Kigali_villages")
    export_folder.mkdir(exist_ok=True)
    (export_folder / "index.html").write_text(fig.to_html())
