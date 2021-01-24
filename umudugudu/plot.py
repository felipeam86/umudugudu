import geopandas as gpd
import numpy as np
import plotly.express as px


def get_zoom_center(
    df: gpd.GeoDataFrame, margin: float = 1.2, width_to_height: float = 2
):
    """
    The code to compute the zoom was borrowed from:
    https://github.com/richieVil/rv_packages/blob/master/rv_geojson.py
    """

    lon_min, lat_min, lon_max, lat_max = df.total_bounds

    center = {
        "lon": round((lon_max + lon_min) / 2, 6),
        "lat": round((lat_max + lat_min) / 2, 6),
    }

    lon_zoom_range = np.array(
        [
            0.0007,
            0.0014,
            0.003,
            0.006,
            0.012,
            0.024,
            0.048,
            0.096,
            0.192,
            0.3712,
            0.768,
            1.536,
            3.072,
            6.144,
            11.8784,
            23.7568,
            47.5136,
            98.304,
            190.0544,
            360.0,
        ]
    )

    height = (lat_max - lat_min) * margin * width_to_height
    width = (lon_max - lon_min) * margin
    lon_zoom = np.interp(width, lon_zoom_range, range(20, 0, -1))
    lat_zoom = np.interp(height, lon_zoom_range, range(20, 0, -1))
    zoom = round(min(lon_zoom, lat_zoom), 2)

    return zoom, center


def hex_to_rgba(cmap, opacity=1.0):
    return [
        f"rgba({red}, {green}, {blue}, {opacity})"
        for red, green, blue in map(px.colors.hex_to_rgb, cmap)
    ]


def administrative_divisions(
    df: gpd.GeoDataFrame,
    opacity=0.25,
    line_width=1.5,
    transparent: bool = False,
    color="District",
    legend: bool = True,
):
    if transparent:
        colors = ["rgba(255,255,255,0)"]
    else:
        colors = hex_to_rgba(px.colors.qualitative.D3, opacity=opacity)
    hover_cols = [
        col
        for col in ["Village", "Cell", "Sector", "District", "Province"]
        if col in df.columns
    ]
    hovertemplate = (
        "<br>".join(
            [f"<b>{col}</b>=%{{customdata[{i}]}}" for i, col in enumerate(hover_cols)]
        )
        + "<extra></extra>"
    )
    zoom, center = get_zoom_center(df)
    fig = px.choropleth_mapbox(
        df,
        geojson=df.geometry,
        locations=df.index,
        color=color,
        mapbox_style="open-street-map",
        zoom=zoom,
        center=center,
        opacity=1,
        hover_data=hover_cols,
        color_discrete_sequence=colors,
    )
    fig.update_layout(
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        showlegend=legend and (not transparent),
    )
    fig.update_traces(
        marker_line_width=line_width,
        hovertemplate=hovertemplate,
    )
    return fig
