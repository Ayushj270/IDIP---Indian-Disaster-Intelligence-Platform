# ============================================================
# DISASTER SPATIAL MAP ENGINE
# ============================================================

import math
import pandas as pd
import plotly.graph_objects as go

# ============================================================
# CALCULATE MAP VIEW FROM SELECTED STATE BOUNDARY
# ============================================================

def calculate_map_view(
    india_geo,
    selected_state
):
    # --------------------------------------------------------
    # FIND SELECTED STATE
    # --------------------------------------------------------

    selected_feature = None
    for feature in india_geo.get(
        "features",
        []
    ):
        state_name = feature.get(
            "properties",
            {}
        ).get(
            "ST_NM"
        )
        if state_name == selected_state:
            selected_feature = feature
            break

    # --------------------------------------------------------
    # FALLBACK
    # --------------------------------------------------------

    if selected_feature is None:
        return {
            "center": {
                "lat": 22.0,
                "lon": 79.0
            },
            "zoom": 5
        }

    # --------------------------------------------------------
    # EXTRACT ALL STATE COORDINATES
    # --------------------------------------------------------

    geometry = selected_feature.get(
        "geometry",
        {}
    )
    coordinates = []
    def extract_coordinates(
        coords
    ):

        for item in coords:
            if (
                isinstance(
                    item,
                    (list, tuple)
                )
                and len(item) >= 2
                and isinstance(
                    item[0],
                    (int, float)
                )
            ):
                coordinates.append(
                    item
                )
            else:
                extract_coordinates(
                    item
                )

    extract_coordinates(
        geometry.get(
            "coordinates",
            []
        )
    )

    # --------------------------------------------------------
    # SAFETY CHECK
    # --------------------------------------------------------

    if not coordinates:

        return {
            "center": {
                "lat": 22.0,
                "lon": 79.0
            },
            "zoom": 5
        }

    # --------------------------------------------------------
    # GET STATE BOUNDING BOX
    # --------------------------------------------------------

    lons = [
        point[0]
        for point in coordinates
    ]
    lats = [
        point[1]
        for point in coordinates
    ]
    min_lon = min(lons)
    max_lon = max(lons)
    min_lat = min(lats)
    max_lat = max(lats)

    # --------------------------------------------------------
    # CALCULATE CENTER
    # --------------------------------------------------------

    center_lon = (
        min_lon + max_lon
    ) / 2

    center_lat = (
        min_lat + max_lat
    ) / 2

    # --------------------------------------------------------
    # CALCULATE STATE SIZE
    # --------------------------------------------------------

    lon_range = (
        max_lon - min_lon
    )

    lat_range = (
        max_lat - min_lat
    )

    # --------------------------------------------------------
    # ADD SMALL SAFE PADDING
    # --------------------------------------------------------

    effective_range = max(
        lon_range * 0.75,
        lat_range * 1.10
    )

    # --------------------------------------------------------
    # CALCULATE DYNAMIC ZOOM
    # --------------------------------------------------------

    zoom = math.log2(
        360 / effective_range
    )
    # --------------------------------------------------------
    # LIMIT ZOOM
    # --------------------------------------------------------

    zoom = max(
        5.0,
        min(
            zoom,
            8.2
        )
    )
    return {
        "center": {
            "lat": center_lat,
            "lon": center_lon
        },
        "zoom": zoom
    }

# ============================================================
# GET SPATIAL DISASTER DATA
# ============================================================

def get_spatial_disaster_data(
    data,
    selected_state
):
    # --------------------------------------------------------
    # COPY DATA
    # --------------------------------------------------------
    earthquake = data[
        "earthquake"
    ].copy()

    flood = data[
        "flood"
    ].copy()
    cyclone = data[
        "cyclone"
    ].copy()

    # --------------------------------------------------------
    # FILTER SELECTED STATE
    # --------------------------------------------------------

    earthquake = earthquake[
        earthquake[
            "state_name"
        ] == selected_state
    ]
    flood = flood[
        flood[
            "state_name"
        ] == selected_state
    ]
    cyclone = cyclone[
        cyclone[
            "state_name"
        ] == selected_state
    ]
    # --------------------------------------------------------
    # KEEP ONLY EVENTS WITH VALID COORDINATES
    # --------------------------------------------------------

    earthquake_map = earthquake[
        earthquake[
            "latitude"
        ].notna()
        &
        earthquake[
            "longitude"
        ].notna()
    ]
    flood_map = flood[
        flood[
            "latitude"
        ].notna()
        &
        flood[
            "longitude"
        ].notna()
    ]
    cyclone_map = cyclone[
        cyclone[
            "latitude"
        ].notna()
        &
        cyclone[
            "longitude"
        ].notna()
    ]
    # --------------------------------------------------------
    # RETURN MAP DATA + COVERAGE INFORMATION
    # --------------------------------------------------------

    return {

        "earthquake": earthquake_map,
        "flood": flood_map,
        "cyclone": cyclone_map,
        "coverage": {
            "earthquake": {
                "total": len(
                    earthquake
                ),
                "mapped": len(
                    earthquake_map
                )
            },
            "flood": {
                "total": len(
                    flood
                ),
                "mapped": len(
                    flood_map
                )
            },
            "cyclone": {
                "total": len(
                    cyclone
                ),
                "mapped": len(
                    cyclone_map
                )
            }
        }
    }
# ============================================================
# CREATE OUTSIDE STATE MASK
# ============================================================

def create_state_focus_mask(selected_feature):

    world = [
        [-180, -90],
        [180, -90],
        [180, 90],
        [-180, 90],
        [-180, -90]
    ]
    state_geometry = selected_feature["geometry"]
    if state_geometry["type"] == "Polygon":
        hole = state_geometry["coordinates"]
    elif state_geometry["type"] == "MultiPolygon":
        hole = []
        for polygon in state_geometry["coordinates"]:
            hole.extend(polygon)

    mask_geometry = {
        "type": "Polygon",
        "coordinates": [
            world
        ] + hole
    }
    return {
        "type": "Feature",
        "geometry": mask_geometry
    }

# ============================================================
# CREATE DISASTER SPATIAL MAP
# ============================================================

def create_disaster_spatial_map(
    spatial_data,
    selected_state,
    india_geo
):
    # --------------------------------------------------------
    # CREATE FIGURE
    # --------------------------------------------------------

    fig = go.Figure()

    # ========================================================
    # FIND SELECTED STATE
    # ========================================================

    selected_feature = None
    for feature in india_geo.get("features", []):
        state_name = feature.get(
            "properties",
            {}
        ).get(
            "ST_NM"
        )

        if state_name == selected_state:
            selected_feature = feature
            break

    # ========================================================
    # FIND SELECTED STATE FEATURE
    # ========================================================

    selected_feature = None
    for feature in india_geo.get(
        "features",
        []
    ):
        state_name = feature.get(
            "properties",
            {}
        ).get(
            "ST_NM"
        )
        if state_name == selected_state:
            selected_feature = feature
            break

    # ========================================================
    # DRAW SELECTED STATE BOUNDARY
    # ========================================================

    if selected_feature is not None:
        geometry = selected_feature.get(
            "geometry",
            {}
        )
        fig.add_trace(
            go.Choroplethmapbox(
                geojson={
                    "type":"Feature",
                    "geometry":geometry
                },
                locations=[0],
                z=[1],
                colorscale=[
                    [
                        0,
                        "rgba(56,189,248,0.20)"
                    ],
                    [
                        1,
                        "rgba(56,189,248,0.20)"
                    ]
                ],
                showscale=False,
                hoverinfo="skip"
            )
        )
        geometry_type = geometry.get(
            "type"
        )
        if geometry_type == "Polygon":
            polygons = [
                geometry[
                    "coordinates"
                ]
            ]
        elif geometry_type == "MultiPolygon":
            polygons = geometry[
                "coordinates"
            ]
        else:
            polygons = []
        for polygon in polygons:
            for ring in polygon:
                lons = [
                    point[0]
                    for point in ring
                ]
                lats = [
                    point[1]
                    for point in ring
                ]
                # Outer glow line
                fig.add_trace(
                    go.Scattermapbox(
                        lat=lats,
                        lon=lons,
                        mode="lines",
                        line=dict(
                            width=8,
                            color="rgba(0,191,255,0.25)"
                        ),
                        hoverinfo="skip",
                        showlegend=False
                    )
                )
                # Main boundary line
                fig.add_trace(
                    go.Scattermapbox(
                        lat=lats,
                        lon=lons,
                        mode="lines",
                        line=dict(
                            width=1,
                            color="#00BFFF"
                        ),
                        hoverinfo="skip",
                        showlegend=False
                    )
                )
    # ========================================================
    # ADD OUTSIDE STATE DARK MASK
    # ========================================================

    if selected_feature is not None:
        mask_geojson = create_state_focus_mask(
            selected_feature
        )
        fig.add_trace(
            go.Choroplethmapbox(
                geojson=mask_geojson,
                locations=[0],
                z=[1],
                colorscale=[
                    [
                        0,
                        "rgba(0,0,0,0.45)"
                    ],
                    [
                        1,
                        "rgba(0,0,0,0.45)"
                    ]
                ],
                showscale=False,
                hoverinfo="skip"
            )
        )
    # ========================================================
    # EARTHQUAKE EVENTS
    # ========================================================

    eq = spatial_data[
        "earthquake"
    ]
    if not eq.empty:
        fig.add_trace(
            go.Scattermapbox(
                lat=eq[
                    "latitude"
                ],
                lon=eq[
                    "longitude"
                ],
                mode="markers",
                name="Earthquake",
                marker=dict(
                    size=8,
                    color="#F59E0B"
                ),
                customdata=eq[
                    "magnitude"
                ],
                hovertemplate=(
                    "<b>Earthquake</b><br>"
                    "Magnitude: %{customdata}"
                    "<extra></extra>"
                )
            )
        )
    # ========================================================
    # FLOOD EVENTS
    # ========================================================

    flood = spatial_data[
        "flood"
    ]
    if not flood.empty:
        fig.add_trace(
            go.Scattermapbox(
                lat=flood[
                    "latitude"
                ],
                lon=flood[
                    "longitude"
                ],
                mode="markers",
                name="Flood",
                marker=dict(
                    size=9,
                    color="#38BDF8"
                ),
                hovertemplate=(
                    "<b>Flood Event</b>"
                    "<extra></extra>"
                )
            )
        )
    # ========================================================
    # CYCLONE EVENTS
    # ========================================================

    cyclone = spatial_data[
        "cyclone"
    ]
    if not cyclone.empty:
        fig.add_trace(
            go.Scattermapbox(
                lat=cyclone[
                    "latitude"
                ],
                lon=cyclone[
                    "longitude"
                ],
                mode="markers",
                name="Cyclone",
                marker=dict(
                    size=12,
                    color="#22C55E"
                ),
                hovertemplate=(
                    "<b>Cyclone Event</b>"
                    "<extra></extra>"
                )
            )
        )

    # ========================================================
    # CALCULATE SELECTED STATE VIEW
    # ========================================================

    map_view = calculate_map_view(

        india_geo,
        selected_state
    )

    # ========================================================
    # DARK BASEMAP
    # ========================================================

    dark_base = (
        "https://server.arcgisonline.com/"
        "ArcGIS/rest/services/"
        "Canvas/World_Dark_Gray_Base/"
        "MapServer/tile/{z}/{y}/{x}"
    )

    dark_reference = (
        "https://server.arcgisonline.com/"
        "ArcGIS/rest/services/"
        "Canvas/World_Dark_Gray_Reference/"
        "MapServer/tile/{z}/{y}/{x}"
    )

    # ========================================================
    # MAP SETTINGS
    # ========================================================

    fig.update_layout(
        autosize=False,
        height=720,
        width=700,
        showlegend=False,
        dragmode=False,
        mapbox=dict(
            style="white-bg",
            layers=[
                dict(
                    sourcetype="raster",
                    source=[
                        "https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Dark_Gray_Base/MapServer/tile/{z}/{y}/{x}"
                    ],
                    below="traces",
                    opacity=1
                ),
                dict(
                    sourcetype="raster",
                    source=[
                        "https://tile.openstreetmap.org/{z}/{x}/{y}.png"
                    ],
                    below="traces",
                    opacity=0.05
                )
            ],
            zoom=map_view["zoom"],
            center=dict(
                lat=map_view["center"]["lat"],
                lon=map_view["center"]["lon"]
            ),
            pitch=0,
            bearing=0
        ),
        paper_bgcolor="#0B1120",
        plot_bgcolor="#0B1120",
        margin=dict(
            l=0,
            r=0,
            t=0,
            b=0
        )
    )

    for trace in fig.data:
        trace.showlegend = False

    return fig