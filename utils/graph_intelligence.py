# ============================================================
# GRAPH INTELLIGENCE ENGINE
# ============================================================

import pandas as pd

# ============================================================
# EARTHQUAKE GRAPH INTELLIGENCE
# ============================================================

def get_earthquake_graph_intelligence(
    data,
    selected_state
):

    earthquake_df = data["earthquake"]
    state_eq = earthquake_df[
        earthquake_df["state_name"]
        ==
        selected_state
    ].copy()

    if state_eq.empty:

        return {
            "events":0,
            "yearly_trend":pd.DataFrame(),
            "yearly_magnitude_trend":pd.DataFrame(),
            "average_magnitude":0,
            "maximum_magnitude":0,
            "most_active_year":None
        }
    
    # --------------------------------------------------------
    # YEARLY EVENT TREND
    # --------------------------------------------------------

    yearly_trend = (
        state_eq
        .groupby("year")
        .size()
        .reset_index(
            name="events"
        )
        .sort_values("year")
    )

    # --------------------------------------------------------
    # YEARLY MAGNITUDE TREND
    # --------------------------------------------------------

    yearly_magnitude_trend = (
        state_eq
        .groupby("year")["magnitude"]
        .mean()
        .reset_index(
            name="average_magnitude"
        )
        .sort_values("year")
    )

    yearly_magnitude_trend["average_magnitude"] = (
        yearly_magnitude_trend["average_magnitude"]
        .round(2)
    )

    # --------------------------------------------------------
    # MAGNITUDE METRICS
    # --------------------------------------------------------

    magnitude = pd.to_numeric(
        state_eq["magnitude"],
        errors="coerce"
    )

    average_magnitude = round(
        magnitude.mean(),
        2
    )

    maximum_magnitude = round(
        magnitude.max(),
        2
    )

    # --------------------------------------------------------
    # MOST ACTIVE YEAR
    # --------------------------------------------------------

    most_active_year = int(
        yearly_trend.loc[
            yearly_trend["events"].idxmax(),
            "year"
        ]
    )

    return {

        "events":
        len(state_eq),

        "yearly_trend":
        yearly_trend,

        "yearly_magnitude_trend":
        yearly_magnitude_trend,

        "average_magnitude":
        average_magnitude,

        "maximum_magnitude":
        maximum_magnitude,

        "most_active_year":
        most_active_year
    }

# ============================================================
# FLOOD GRAPH INTELLIGENCE
# ============================================================

def get_flood_graph_intelligence(
    data,
    selected_state
):

    flood_df = data["flood"]

    state_flood = flood_df[
        flood_df["state_name"]
        ==
        selected_state
    ].copy()

    if state_flood.empty:

        return {
            "events": 0,
            "yearly_trend": pd.DataFrame(),
            "yearly_duration_trend": pd.DataFrame(),
            "average_duration": 0,
            "maximum_duration": 0,
            "fatalities": 0,
            "most_active_year": None
        }

    # --------------------------------------------------------
    # YEARLY EVENT TREND
    # --------------------------------------------------------

    yearly_trend = (
        state_flood
        .groupby("year")
        .size()
        .reset_index(
            name="events"
        )
        .sort_values("year")
    )

    # --------------------------------------------------------
    # YEARLY DURATION TREND
    # --------------------------------------------------------

    yearly_duration_trend = (
        state_flood
        .groupby("year")["duration_days"]
        .mean()
        .reset_index(
            name="average_duration"
        )
    )

    yearly_duration_trend["average_duration"] = (
        yearly_duration_trend["average_duration"]
        .round(2)
    )

    # --------------------------------------------------------
    # DURATION METRICS
    # --------------------------------------------------------

    duration = pd.to_numeric(
        state_flood["duration_days"],
        errors="coerce"
    )

    average_duration = round(
        duration.mean(),
        2
    )

    maximum_duration = round(
        duration.max(),
        2
    )

    # --------------------------------------------------------
    # FATALITIES
    # --------------------------------------------------------

    fatalities = int(
        pd.to_numeric(
            state_flood["fatalities"],
            errors="coerce"
        )
        .fillna(0)
        .sum()
    )

    # --------------------------------------------------------
    # MOST ACTIVE YEAR
    # --------------------------------------------------------

    most_active_year = int(
        yearly_trend.loc[
            yearly_trend["events"].idxmax(),
            "year"
        ]
    )

    return {

        "events":
        len(state_flood),

        "yearly_trend":
        yearly_trend,

        "yearly_duration_trend":
        yearly_duration_trend,

        "average_duration":
        average_duration,

        "maximum_duration":
        maximum_duration,

        "fatalities":
        fatalities,

        "most_active_year":
        most_active_year
    }

# ============================================================
# CYCLONE GRAPH INTELLIGENCE
# ============================================================

def get_cyclone_graph_intelligence(
    data,
    selected_state
):

    cyclone_df = data["cyclone"]
    state_cyclone = cyclone_df[
        cyclone_df["state_name"]
        ==
        selected_state
    ].copy()

    if state_cyclone.empty:

        return {
            "events": 0,
            "yearly_trend": pd.DataFrame(),
            "yearly_wind_speed_trend": pd.DataFrame(),
            "average_wind_speed": 0,
            "maximum_wind_speed": 0,
            "minimum_pressure": 0,
            "most_active_year": None
        }

    # --------------------------------------------------------
    # YEARLY EVENT TREND
    # --------------------------------------------------------

    yearly_trend = (
        state_cyclone
        .groupby("year")
        .size()
        .reset_index(
            name="events"
        )
        .sort_values("year")
    )

    # --------------------------------------------------------
    # YEARLY WIND SPEED TREND
    # --------------------------------------------------------

    yearly_wind_speed_trend = (
        state_cyclone
        .groupby("year")["wind_speed_knots"]
        .mean()
        .reset_index(
            name="average_wind_speed"
        )
    )

    yearly_wind_speed_trend["average_wind_speed"] = (
        yearly_wind_speed_trend["average_wind_speed"]
        .round(2)
    )

    # --------------------------------------------------------
    # WIND SPEED METRICS
    # --------------------------------------------------------

    wind_speed = pd.to_numeric(
        state_cyclone["wind_speed_knots"],
        errors="coerce"
    )

    average_wind_speed = round(
        wind_speed.mean(),
        2
    )

    maximum_wind_speed = round(
        wind_speed.max(),
        2
    )

    # --------------------------------------------------------
    # PRESSURE METRIC
    # --------------------------------------------------------

    pressure = pd.to_numeric(
        state_cyclone["pressure_mb"],
        errors="coerce"
    )

    minimum_pressure = round(
        pressure.min(),
        2
    )

    # --------------------------------------------------------
    # MOST ACTIVE YEAR
    # --------------------------------------------------------

    most_active_year = int(
        yearly_trend.loc[
            yearly_trend["events"].idxmax(),
            "year"
        ]
    )

    return {

        "events":
        len(state_cyclone),

        "yearly_trend":
        yearly_trend,

        "yearly_wind_speed_trend":
        yearly_wind_speed_trend,

        "average_wind_speed":
        average_wind_speed,

        "maximum_wind_speed":
        maximum_wind_speed,

        "minimum_pressure":
        minimum_pressure,

        "most_active_year":
        most_active_year
    }

# ============================================================
# STATE DISASTER INTELLIGENCE
# ============================================================

def get_state_disaster_intelligence(

    earthquake,
    flood,
    cyclone,
    selected_state

):

    disaster_events = {

        "Earthquake":
        earthquake["events"],

        "Flood":
        flood["events"],

        "Cyclone":
        cyclone["events"]
    }

    total_events = sum(
        disaster_events.values()
    )

    if total_events == 0:
        return {

            "total_events": 0,

            "most_active_disaster":
            "N/A",

            "most_active_events":
            0,

            "no_record_disasters":
            list(disaster_events.keys())
        }

    most_active_disaster = max(
        disaster_events,
        key=disaster_events.get
    )

    most_active_events = (
        disaster_events[
            most_active_disaster
        ]
    )

    no_record_disasters = [

        disaster
        for disaster, events
        in disaster_events.items()
        if events == 0
    ]

    return {

        "total_events":
        total_events,

        "most_active_disaster":
        most_active_disaster,

        "most_active_events":
        most_active_events,

        "no_record_disasters":
        no_record_disasters
    }

# ============================================================
# COMPLETE GRAPH INTELLIGENCE
# ============================================================

def get_complete_graph_intelligence(
    data,
    selected_state
):

    earthquake = (
        get_earthquake_graph_intelligence(
            data=data,
            selected_state=selected_state
        )
    )

    flood = (
        get_flood_graph_intelligence(
            data=data,
            selected_state=selected_state
        )
    )

    cyclone = (
        get_cyclone_graph_intelligence(
            data=data,
            selected_state=selected_state
        )
    )

    state_intelligence = (
        get_state_disaster_intelligence(
            earthquake=earthquake,
            flood=flood,
            cyclone=cyclone,
            selected_state=selected_state
        )
    )

    return {

        "earthquake":
        earthquake,

        "flood":
        flood,

        "cyclone":
        cyclone,

        "state_intelligence":
        state_intelligence
    }