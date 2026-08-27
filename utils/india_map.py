# ============================================================
# 1. IMPORTS
# ============================================================

import json
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go


# ============================================================
# 2. PROJECT PATHS
# ============================================================

PROJECT_DIR = Path(__file__).resolve().parent.parent

GEOJSON_FILE = (
    PROJECT_DIR
    / "shapfiles"
    / "india_states_new.geojson"
)


# ============================================================
# 3. STATE NAME NORMALIZATION
# ============================================================

STATE_NAME_MAPPING = {

    "Andaman and Nicobar":
        "Andaman and Nicobar Islands",

    "Jammu and Kashmir":
        "Jammu & Kashmir",

    "NCT of Delhi":
        "Delhi",

    "Dadra and Nagar Haveli":
        "Dadra and Nagar Haveli and Daman and Diu",

    "Daman and Diu":
        "Dadra and Nagar Haveli and Daman and Diu"
}


# ============================================================
# 4. LOAD AND NORMALIZE INDIA GEOJSON
# ============================================================

def load_india_geojson():

    with open(
        GEOJSON_FILE,
        encoding="utf-8"
    ) as file:

        india_geo = json.load(file)

    for feature in india_geo.get(
        "features",
        []
    ):

        properties = feature.setdefault(
            "properties",
            {}
        )

        original_state_name = properties.get(
            "NAME_1"
        )

        if original_state_name:

            normalized_state_name = (
                STATE_NAME_MAPPING.get(
                    original_state_name,
                    original_state_name
                )
            )

            properties["ST_NM"] = (
                normalized_state_name
            )

    return india_geo


# ============================================================
# 5. EXTRACT STATES AND UNION TERRITORIES
# ============================================================

def get_india_states(india_geo):

    states = sorted(

        {
            feature
            .get(
                "properties",
                {}
            )
            .get(
                "ST_NM"
            )

            for feature in india_geo.get(
                "features",
                []
            )

            if feature
            .get(
                "properties",
                {}
            )
            .get(
                "ST_NM"
            )
        }

    )

    return states


# ============================================================
# 7. STATE COLORS
# ============================================================

STATE_COLORS = {

    "Andhra Pradesh": "#00BFFF",

    "Arunachal Pradesh": "#FFB347",

    "Assam": "#8A2BE2",

    "Bihar": "#FF6347",

    "Chhattisgarh": "#32CD32",

    "Goa": "#00CED1",

    "Gujarat": "#FF8C00",

    "Haryana": "#FFD700",

    "Himachal Pradesh": "#87CEEB",

    "Jharkhand": "#7FFF00",

    "Karnataka": "#FF4500",

    "Kerala": "#00FA9A",

    "Madhya Pradesh": "#9ACD32",

    "Maharashtra": "#FF1493",

    "Manipur": "#9370DB",

    "Meghalaya": "#00FFFF",

    "Mizoram": "#FF69B4",

    "Nagaland": "#BA55D3",

    "Odisha": "#FFA500",

    "Punjab": "#FFD700",

    "Rajasthan": "#FF4FA3",

    "Sikkim": "#40E0D0",

    "Tamil Nadu": "#FF6347",

    "Telangana": "#DA70D6",

    "Tripura": "#7CFC00",

    "Uttar Pradesh": "#00BFFF",

    "Uttarakhand": "#87CEFA",

    "West Bengal": "#FF1493",

    "Andaman and Nicobar Islands": "#00CED1",

    "Chandigarh": "#FFD700",

    "Dadra and Nagar Haveli and Daman and Diu":
        "#ADFF2F",

    "Delhi": "#FF4500",

    "Jammu & Kashmir": "#00BFFF",

    "Ladakh": "#DDA0DD",

    "Lakshadweep": "#00FA9A",

    "Puducherry": "#FFA07A"
}


# ============================================================
# 8. CREATE INDIA MAP
# ============================================================

def create_india_map(
    india_geo,
    states,
    selected_state=None
):

    # --------------------------------------------------------
    # 8.01 PREPARE MAP DATA
    # --------------------------------------------------------

    # If a state is selected, remove it from the lower map.
    # That state will be displayed separately as the uplifted map.
    if selected_state:

        remaining_states = [

            state

            for state in states

            if state != selected_state

        ]

    else:

        remaining_states = states


    map_df = pd.DataFrame(
        {
            "state": remaining_states
        }
    )


    # --------------------------------------------------------
    # 8.02 CREATE FIGURE
    # --------------------------------------------------------

    fig = go.Figure()


    # --------------------------------------------------------
    # 8.03 BASE INDIA MAP
    # --------------------------------------------------------

    fig.add_trace(

        go.Choropleth(

            geojson=india_geo,

            locations=map_df["state"],

            featureidkey="properties.ST_NM",

            z=[1] * len(map_df),

            zmin=0,

            zmax=1,

            colorscale=[

                [
                    0,
                    "rgba(0,0,0,0)"
                ],

                [
                    1,
                    "rgba(0,0,0,0)"
                ]

            ],

            showscale=False,

            marker=dict(

                line=dict(

                    color="#6EAED4",

                    width=1.2

                )

            ),

            hovertemplate=(

                "<b>%{location}</b>"

                "<extra></extra>"

            )

        )

    )


    # --------------------------------------------------------
    # 8.04 MAP SETTINGS
    # --------------------------------------------------------

    fig.update_geos(

        visible=False,

        showcoastlines=False,

        showcountries=False,

        showland=False,

        showocean=False,

        showlakes=False,

        showframe=False,

        bgcolor="#0E1117",

        projection_type="mercator",

        fitbounds="locations"

    )


    # --------------------------------------------------------
    # 8.05 MAP LAYOUT
    # --------------------------------------------------------

    fig.update_layout(

        height=600,

        margin=dict(

            l=0,

            r=0,

            t=0,

            b=0

        ),

        paper_bgcolor="#0E1117",

        plot_bgcolor="#0E1117",

        dragmode=False,

        showlegend=False

    )


    # --------------------------------------------------------
    # 8.06 RETURN FIGURE
    # --------------------------------------------------------

    return fig

# ============================================================
# 9. CREATE SELECTED STATE UPLIFT MAP
# ============================================================

def create_state_uplift_map(
    india_geo,
    selected_state
):

    # --------------------------------------------------------
    # 9.01 FIND SELECTED STATE FEATURE
    # --------------------------------------------------------

    selected_features = []


    for feature in india_geo.get(
        "features",
        []
    ):

        properties = feature.get(
            "properties",
            {}
        )


        state_name = properties.get(
            "ST_NM"
        )


        if state_name == selected_state:

            selected_features.append(
                feature
            )


    # --------------------------------------------------------
    # 9.02 SAFETY CHECK
    # --------------------------------------------------------

    if not selected_features:

        return None


    # --------------------------------------------------------
    # 9.03 CREATE STATE GEOJSON
    # --------------------------------------------------------

    selected_geojson = {

        "type": "FeatureCollection",

        "features": selected_features

    }


    # --------------------------------------------------------
    # 9.04 GET STATE COLOR
    # --------------------------------------------------------

    selected_color = STATE_COLORS.get(

        selected_state,

        "#00E5FF"

    )


    # --------------------------------------------------------
    # 9.05 CREATE FIGURE
    # --------------------------------------------------------

    fig = go.Figure()


    # --------------------------------------------------------
    # 9.06 OUTER GLOW
    # --------------------------------------------------------

    fig.add_trace(

        go.Choropleth(

            geojson=selected_geojson,

            locations=[selected_state],

            featureidkey="properties.ST_NM",

            z=[1],

            zmin=0,

            zmax=1,

            colorscale=[

                [0, selected_color],

                [1, selected_color]

            ],

            showscale=False,

            marker=dict(

                line=dict(

                    color=selected_color,

                    width=10

                )

            ),

            hoverinfo="skip"

        )

    )


    # --------------------------------------------------------
    # 9.07 MAIN STATE
    # --------------------------------------------------------

    fig.add_trace(

        go.Choropleth(

            geojson=selected_geojson,

            locations=[selected_state],

            featureidkey="properties.ST_NM",

            z=[1],

            zmin=0,

            zmax=1,

            colorscale=[

                [0, selected_color],

                [1, selected_color]

            ],

            showscale=False,

            marker=dict(

                line=dict(

                    color="#FFFFFF",

                    width=2.5

                )

            ),

            hovertemplate=(

                f"<b>{selected_state}</b>"

                "<extra></extra>"

            )

        )

    )


    # --------------------------------------------------------
    # 9.08 MAP SETTINGS
    # --------------------------------------------------------

    fig.update_geos(

        visible=False,

        showcoastlines=False,

        showcountries=False,

        showland=False,

        showocean=False,

        showlakes=False,

        showframe=False,

        bgcolor="#0E1117",

        projection_type="mercator",

        fitbounds="locations"

    )


    # --------------------------------------------------------
    # 9.09 MAP LAYOUT
    # --------------------------------------------------------

    fig.update_layout(

        height=420,

        margin=dict(

            l=0,

            r=0,

            t=0,

            b=0

        ),

        paper_bgcolor="#0E1117",

        plot_bgcolor="#0E1117",

        dragmode=False,

        showlegend=False

    )


    # --------------------------------------------------------
    # 9.10 RETURN FIGURE
    # --------------------------------------------------------

    return fig