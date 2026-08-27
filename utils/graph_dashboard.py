# ============================================================
# GRAPH DASHBOARD
# ============================================================

import streamlit as st
import plotly.express as px
import pandas as pd

from utils.graph_intelligence import (
    get_complete_graph_intelligence
)

# ============================================================
# HELPER FUNCTIONS
# ============================================================

# ADD CSS
st.markdown(
"""
<style>

.metric-card{
    background:#111827;
    border:1px solid #243044;
    border-radius:14px;
    padding:20px;
    height:120px;
}

.metric-title{
    color:#94A3B8;
    font-size:13px;
}

.metric-value{
    margin-top:18px;
    font-size:30px;
    font-weight:700;
    color:#F8FAFC;
}

.summary-card{
    background:#162A45;
    border:1px solid #2563EB;
    border-radius:12px;
    padding:18px;
}

.summary-title{
    font-size:18px;
    font-weight:700;
    margin-bottom:10px;
}

.summary-text{
    color:#93C5FD;
    font-size:15px;
}

</style>
""",
unsafe_allow_html=True
)

def create_line_chart(
    data,
    x_column,
    y_column,
    x_title,
    y_title,
    color= "#60A5FA",
    key=None,
    markers = True
):
    """
    Creates a consistent dark-theme line chart.
    """

    if data is None or data.empty:
        return None

    fig = px.line(
        data,
        x=x_column,
        y=y_column,
        markers=True,
    )

    fig.update_traces(
        line=dict(
            width=3,
            color=color
        ),
        marker=dict(size=6)
    )

    fig.update_layout(
        height=280,
        autosize=True,
        template="plotly_dark",
        paper_bgcolor="#0F172A",
        plot_bgcolor="#0F172A",
        font=dict(size=13),
        margin=dict(
            l=40,
            r=20,
            t=10,
            b=30
        ),
        xaxis_title=None,
        yaxis_title=None,
        xaxis=dict(
            tickangle=0,
            showgrid=True
        ),
        yaxis=dict(
            showgrid=True
        )
    )

    fig.update_xaxes(
        showgrid=True,
        gridcolor="#2A2F3A"
    )

    fig.update_yaxes(
        showgrid=True,
        gridcolor="#2A2F3A",
        rangemode="tozero"
    )

    return fig

def create_metric_card(
    title,
    value,
    color="#38BDF8",
    icon="●"
):

    st.markdown(
        f"""
        <div style="
            background:#111827;
            border:1px solid #243244;
            border-radius:16px;
            padding:16px;
            height:145px;
            box-shadow:0 0 15px rgba(0,0,0,0.25);
        ">

        <div style="
            display:flex;
            align-items:center;
            gap:8px;
            color:#94A3B8;
            font-size:13px;
        ">

        <span style="
            color:{color};
            font-size:18px;
        ">
        {icon}
        </span>

        {title}

        </div>


        <div style="
            margin-top:15px;
            color:{color};
            font-size:36px;
            text-shadow: 0 0 12px {color};
            font-weight:700;
        ">
        {value}
        </div>


        <div style="
            margin-top:12px;
            height:4px;
            background:#1E293B;
            box-shadow:0 0 12px #1E293B
            border-radius:10px;
        ">

        <div style="
            width:65%;
            height:4px;
            background:{color};
            border-radius:10px;
        ">
        </div>
        </div>
        </div>
        """,
        unsafe_allow_html=True
    )

def graph_container(title, fig, color):

    st.markdown(
        f"""
        <div style="
            background:#111827;
            border:1px solid #1E293B;
            border-radius:12px;
            padding:8px 12px;
            margin-bottom:20px;
            border-radius:14px;
            overflow:hidden;
        ">

        <div style="
            color:{color};
            font-size:16px;
            font-weight:600;
            margin-bottom:5px;
        ">
        📈 {title}
        </div>
        """,
        unsafe_allow_html=True
    )

    st.plotly_chart(
        fig,
        width="stretch",
        config={
            "displayModeBar": False
        }
    )

    st.markdown(
        """
        </div>
        """,
        unsafe_allow_html=True
    )
# ============================================================
# YEAR FILTER
# ============================================================

def filter_data_by_year(
    data,
    start_year,
    end_year
):

    filtered_data = {}
    for disaster_type, disaster_df in data.items():

        if (
            disaster_df is None
            or disaster_df.empty
            or "year" not in disaster_df.columns
        ):

            filtered_data[disaster_type] = disaster_df

        else:

            disaster_df = disaster_df.copy()
            disaster_df["year"] = pd.to_numeric(
                disaster_df["year"],
                errors="coerce"
            )

            filtered_data[disaster_type] = disaster_df[
                (
                    disaster_df["year"] >= start_year
                )
                &
                (
                    disaster_df["year"] <= end_year
                )
            ]

    return filtered_data

# ============================================================
# DISASTER GRAPH DASHBOARD
# ============================================================

def show_graph_dashboard(
    data,
    selected_state
):

    # ========================================================
    # FIND AVAILABLE YEARS
    # ========================================================

    available_years = set()
    for disaster_type, disaster_df in data.items():

        if (
            disaster_df is not None
            and not disaster_df.empty
            and "year" in disaster_df.columns
        ):

            years = pd.to_numeric(
                disaster_df["year"],
                errors="coerce"
            ).dropna()

            available_years.update(
                years.astype(int).tolist()
            )

    # ========================================================
    # PAGE HEADER
    # ========================================================

    st.markdown(
        "# 📈 Disaster Graph Dashboard"
    )

    st.markdown(
        f"### 🌍 Disaster Intelligence — {selected_state}"
    )

    # ========================================================
    # YEAR FILTER
    # ========================================================

    if available_years:

        min_year = min(available_years)
        max_year = max(available_years)
        st.markdown(
            "### 📅 Select Analysis Period"
        )

        st.markdown(
            """
            <div style="
                background:#111827;
                border:1px solid #1E293B;
                border-radius:12px;
                padding:15px 20px;
                margin-bottom:15px;
            ">
            <div style="
                color:#94A3B8;
                font-size:20px;
                margin-bottom:8px;
            ">
            Historical Analysis Range
            </div>
            """,
            unsafe_allow_html=True
        )

        selected_year_range = st.slider(
            "",
            key="graph_year_filter",
            min_value=min_year,
            max_value=max_year,
            value=(
                min_year,
                max_year
            )
        )

        st.markdown(
            "</div>",
            unsafe_allow_html=True
        )
        start_year = selected_year_range[0]
        end_year = selected_year_range[1]
        filtered_data = filter_data_by_year(
            data,
            start_year,
            end_year
        )

    else:

        filtered_data = data
        start_year = None
        end_year = None

    # ========================================================
    # LOAD GRAPH INTELLIGENCE
    # ========================================================

    graph_intelligence = (
        get_complete_graph_intelligence(
            data=filtered_data,
            selected_state=selected_state,
        )
    )

    earthquake = graph_intelligence.get(
        "earthquake",
        {}
    )

    flood = graph_intelligence.get(
        "flood",
        {}
    )

    cyclone = graph_intelligence.get(
        "cyclone",
        {}
    )

    state_intelligence = graph_intelligence.get(
        "state_intelligence",
        {}
    )

    # ========================================================
    # EARTHQUAKE INTELLIGENCE
    # ========================================================

    st.markdown(
        f"## 🌍 Earthquake Intelligence — {selected_state}"
    )

    earthquake_events = earthquake.get(
        "events",
        0
    )

    if earthquake_events > 0:

        col1,col2,col3,col4 = st.columns(4)

        with col1:
            create_metric_card(
                "Total Events",
                earthquake_events,
                "#EF4444",
                "📊"
            )

        with col2:
            create_metric_card(
                "Average Magnitude",
                earthquake.get(
                    "average_magnitude",
                    0
                ),
                "#EF4444",
                "🎯"
            )

        with col3:
            create_metric_card(
                "Maximum Magnitude",
                earthquake.get(
                    "maximum_magnitude",
                    0
                ),
                "#EF4444",
                "⛰️"
            )

        with col4:
            create_metric_card(
                "Most Active Year",
                earthquake.get(
                    "most_active_year",
                    "N/A"
                ),
                "#EF4444",
                "📅"
            )

        st.divider()

        # ====================================================
        # EARTHQUAKE GRAPHS
        # ====================================================

        yearly_data = earthquake.get(
            "yearly_trend",
            pd.DataFrame()
        )


        fig = create_line_chart(
            data=yearly_data,
            x_column="year",
            y_column="events",
            x_title="Year",
            y_title="Number of Events",
            color="#EF4444"
        )

        magnitude_data = earthquake.get(
            "yearly_magnitude_trend",
            pd.DataFrame()
        )

        fig_magnitude = create_line_chart(
            data=magnitude_data,
            x_column="year",
            y_column="average_magnitude",
            x_title="Year",
            y_title="Average Magnitude",
            color="#EF4444"
        )

        # ====================================================
        # SIDE BY SIDE GRAPH LAYOUT
        # ====================================================

        graph_col1, graph_col2 = st.columns(2)

        with graph_col1:

            if fig:

                graph_container(
                    "Earthquake Frequency Trend",
                    fig,
                    "#EF4444"
                )

            else:

                st.info(
                    "No earthquake trend data available."
                )

        with graph_col2:

            if fig_magnitude:

                graph_container(
                    "Earthquake Magnitude Trend",
                    fig_magnitude,
                    "#EF4444"
                )

            else:

                st.info(
                    "No earthquake magnitude data available."
                )

    # ========================================================
    # FLOOD INTELLIGENCE
    # ========================================================

    st.markdown(
        f"## 🌊 Flood Intelligence — {selected_state}"
    )

    flood_events = flood.get(
        "events",
        0
    )

    if flood_events > 0:

        f1, f2, f3, f4 = st.columns(4)

        with f1:

            create_metric_card(
                "Total Events",
                flood_events,
                "#3B82F6"
            )

        with f2:

            create_metric_card(
                "Average Duration",
                f"{flood.get('average_duration', 0)} days",
                "#3B82F6"
            )

        with f3:

            create_metric_card(
                "Maximum Duration",
                f"{flood.get('maximum_duration', 0)} days",
                "#3B82F6"
            )

        with f4:

            create_metric_card(
                "Fatalities",
                flood.get(
                    "fatalities",
                    0
                ),
                "#3B82F6"
            )

        st.divider()

        # ====================================================
        # FLOOD FREQUENCY TREND + DURATION TREND
        # ====================================================

        flood_col1, flood_col2 = st.columns(2)

        with flood_col1:

            flood_yearly_data = flood.get(
                "yearly_trend",
                pd.DataFrame()
            )

            fig_flood_frequency = create_line_chart(
                data=flood_yearly_data,
                x_column="year",
                y_column="events",
                x_title="Year",
                y_title="Number of Events",
                color="#2563EB"
            )

            if fig_flood_frequency:

                graph_container(
                    "Flood Frequency Trend",
                    fig_flood_frequency,
                    "#2563EB"
                )

        with flood_col2:

            duration_data = flood.get(
                "yearly_duration_trend",
                pd.DataFrame()
            )

            fig_flood_duration = create_line_chart(
                data=duration_data,
                x_column="year",
                y_column="average_duration",
                x_title="Year",
                y_title="Average Duration",
                color="#2563EB"
            )

            if fig_flood_duration:

                graph_container(
                    "Flood Duration Trend",
                    fig_flood_duration,
                    "#2563EB"
                )

    # ========================================================
    # CYCLONE INTELLIGENCE
    # ========================================================

    st.markdown(
        f"## 🌀 Cyclone Intelligence — {selected_state}"
    )

    cyclone_events = cyclone.get(
        "events",
        0
    )

    if cyclone_events > 0:

        c1, c2, c3, c4 = st.columns(4)

        with c1:

            create_metric_card(
                "Total Events",
                cyclone_events,
                "#F97316"
            )

        with c2:

            create_metric_card(
                "Average Wind Speed",
                f"{cyclone.get('average_wind_speed', 0)} knots",
                "#F97316"
            )

        with c3:

            create_metric_card(
                "Maximum Wind Speed",
                f"{cyclone.get('maximum_wind_speed', 0)} knots",
                "#F97316"
            )

        with c4:

            create_metric_card(
                "Minimum Pressure",
                f"{cyclone.get('minimum_pressure', 0)} mb",
                "#F97316"
            )

        st.divider()

        # ====================================================
        # CYCLONE FREQUENCY + WIND SPEED TREND
        # ====================================================

        cyclone_col1, cyclone_col2 = st.columns(2)

        with cyclone_col1:

            cyclone_yearly_data = cyclone.get(
                "yearly_trend",
                pd.DataFrame()
            )

            fig_cyclone_frequency = create_line_chart(
                data=cyclone_yearly_data,
                x_column="year",
                y_column="events",
                x_title="Year",
                y_title="Number of Events",
                color="#F97316"
            )


            if fig_cyclone_frequency:

                graph_container(
                    "Cyclone Frequency Trend",
                    fig_cyclone_frequency,
                    "#F97316"
                )

        with cyclone_col2:

            wind_speed_data = cyclone.get(
                "yearly_wind_speed_trend",
                pd.DataFrame()
            )

            fig_wind_speed = create_line_chart(
                data=wind_speed_data,
                x_column="year",
                y_column="average_wind_speed",
                x_title="Year",
                y_title="Wind Speed",
                color="#F97316"
            )

            if fig_wind_speed:

                graph_container(
                    "Cyclone Wind Speed Trend",
                    fig_wind_speed,
                    "#F97316"
                )
    # ========================================================
    # OVERALL STATE DISASTER INTELLIGENCE
    # ========================================================

    st.markdown(
        f"## 🧠 Overall Disaster Intelligence — {selected_state}"
    )

    i1, i2, i3 = st.columns(3)

    with i1:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">
                    Total Recorded Events
                </div>
                <div class="metric-value">
                    {state_intelligence.get("total_events",0)}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with i2:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">
                    Most Frequent Disaster
                </div>
                <div class="metric-value">
                    {state_intelligence.get("most_active_disaster","N/A")}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with i3:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">
                    Events in Most Frequent Disaster
                </div>
                <div class="metric-value">
                    {state_intelligence.get("most_active_events",0)}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


    # ========================================================
    # DISASTERS WITH NO RECORDS
    # ========================================================

    no_record_disasters = state_intelligence.get(
        "no_record_disasters",
        []
    )

    st.caption(
        "No available historical records found for: "
        +
        ", ".join(
            no_record_disasters
        )
    )

# ========================================================
# STATE SUMMARY
# ========================================================

    st.markdown(
        "### 📋 State Disaster Summary"
    )

    st.markdown(
        f"""
        <div class="summary-card">

        <div class="summary-title">
        📋 State Disaster Summary
        </div>

        <div class="summary-text">
        {state_intelligence.get("summary","No summary available")}
        </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    # ========================================================
    # METHODOLOGY NOTE
    # ========================================================

    st.caption(

        "All visualizations are based on the available historical "
        "records for the selected state and selected year range. "
        "Event frequency indicates recorded occurrence patterns, while "
        "magnitude, duration, and wind speed describe different "
        "characteristics of each disaster type. These measures should "
        "not be interpreted as a direct comparison of overall disaster risk."

    )