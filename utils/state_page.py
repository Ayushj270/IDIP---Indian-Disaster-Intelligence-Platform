# ============================================================
# 1. IMPORT LIBRARIES
# ============================================================

import streamlit as st
from utils.india_map import (
    create_state_uplift_map
)

from utils.state_intelligence import (
    get_complete_state_intelligence
)

from utils.graph_dashboard import (
        show_graph_dashboard
    )

from utils.disaster_map import (
    get_spatial_disaster_data,
    create_disaster_spatial_map
)

# ============================================================
# UI COMPONENTS
# ============================================================

def create_overview_card(
    title,
    value,
    subtitle,
    icon,
    accent_color
):

    st.markdown(
        f"""
        <div style="
            background:#111827;
            padding:14px;
            border-radius:12px;
            border:1px solid {accent_color};
            min-height:120px;
        ">
        <div style="
            color:{accent_color};
            font-size:14px;
            font-weight:700;
            margin-bottom:12px;
        ">
        {icon} {title}
        </div>
        <div style="
            color:white;
            font-size:26px;
            font-weight:800;
            margin-bottom:10px;
        ">
        {value}
        </div>
        <div style="
            color:#94A3B8;
            font-size:14px;
        ">
        {subtitle}
        </div>
        </div>
        """,
        unsafe_allow_html=True
    )

def create_intelligence_card(
    title,
    icon,
    metrics,
    accent_color,
    footer_text=""
):
    with st.container(border=True):

        # Header
        st.markdown(
            f"""
            <div style="
                display:flex;
                align-items:center;
                gap:8px;
                color:{accent_color};
                font-size:17px;
                font-weight:700;
                margin-bottom:14px;
            ">
                <span>{icon}</span>
                <span>{title}</span>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Metrics
        metric_cols = st.columns(3)
        for col, item in zip(metric_cols, metrics):
            label, value = item
            with col:
                st.markdown(
                    f"""
                    <div style="
                        background:#172033;
                        border-radius:10px;
                        padding:22px;
                        border:1px solid #233047;
                        min-height:85px;
                    ">
                    <div style="
                        color:#94A3B8;
                        font-size:12px;
                        line-height:14px;
                    ">
                    {label}
                    </div>
                    <div style="
                        color:white;
                        font-size:22px;
                        font-weight:800;
                        margin-top:8px;
                    ">
                    {value}
                    </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        # Insight footer
        st.markdown(
            f"""
            <div style="
                color:#94A3B8;
                font-size:14px;
                margin-top:15px;
                padding-top:10px;
                border-top:1px solid #1F2937;
            ">
            {footer_text}
            </div>
            """,
            unsafe_allow_html=True
        )

def create_spatial_coverage_card(
    title,
    icon,
    total,
    mapped,
    accent_color
):
    coverage = 0
    if total > 0:
        coverage = int((mapped / total) * 100)

    st.html(
    f"""
    <div style="
        background:#111827;
        border:1px solid {accent_color};
        border-radius:12px;
        padding:10px;
        margin-bottom:8px;
    ">
        <div style="
            color:{accent_color};
            font-size:16px;
            font-weight:700;
            margin-bottom:8px;
        ">
            {icon} {title}
        </div>
        <div style="
            display:flex;
            justify-content:space-between;
            align-items:flex-start;
        ">
            <div>
                <div style="
                    color:#94A3B8;
                    font-size:11px;
                    margin-bottom:5px;
                ">
                    Total Records
                </div>
                <div style="
                    color:white;
                    font-size:24px;
                    font-weight:700;
                ">
                    {total}
                </div>
            </div>
            <div style="
                text-align:right;
            ">
                <div style="
                    color:#94A3B8;
                    font-size:11px;
                    margin-bottom:5px;
                ">
                    Mapped Locations
                </div>
                <div style="
                    color:{accent_color};
                    font-size:24px;
                    font-weight:700;
                ">
                    {mapped}
                </div>
            </div>
        </div>
        <div style="
            margin-top:15px;
        ">
            <div style="
                height:6px;
                background:#1E293B;
                border-radius:10px;
                overflow:hidden;
            ">
                <div style="
                    width:{coverage}%;
                    height:100%;
                    background:{accent_color};
                    border-radius:10px;
                "></div>
            </div>
            <div style="
                color:{accent_color};
                font-size:12px;
                margin-top:8px;
                font-weight:600;
            ">
                Coverage {coverage}%
            </div>
        </div>
    </div>
    """
    )

# ============================================================
# 2. STATE INTELLIGENCE PAGE
# ============================================================

def show_state_intelligence_page(
    data,
    selected_state,
    india_geo
):

    # ========================================================
    # 5. INITIALIZE VIEW
    # ========================================================

    if (
        "previous_state" not in st.session_state
        or st.session_state["previous_state"] != selected_state
    ):
        st.session_state["state_view"] = "analysis"
        st.session_state["previous_state"] = selected_state

    # ========================================================
    # 3. LOAD STATE INTELLIGENCE
    # ========================================================

    intelligence = get_complete_state_intelligence(
        data=data,
        selected_state=selected_state
    )

    # ========================================================
    # 4. EXTRACT DATA
    # ========================================================

    summary = intelligence["summary"]
    earthquake = intelligence["earthquake"]
    flood = intelligence["flood"]
    cyclone = intelligence["cyclone"]
    ml = intelligence["ml"]

    # ============================================================
    # SPATIAL DATA
    # ============================================================

    spatial_data = get_spatial_disaster_data(
        data=data,
        selected_state=selected_state
    )
    coverage = spatial_data["coverage"]

    # ============================================================
    # CREATE SPATIAL MAP
    # ============================================================

    spatial_fig = create_disaster_spatial_map(
        spatial_data,
        selected_state,
        india_geo
    )

    # ============================================================
    # BOUND SPATIAL COVERAGE + MAP
    # ============================================================

    with st.container(border=True):
        coverage_col, map_col = st.columns(
            [1, 2.8],
            gap="small"
        )

        # ============================================================
        # LEFT — SPATIAL DATA COVERAGE
        # ============================================================

        with coverage_col:
            st.markdown(
                """
                <div style="
                    color:#38BDF8;
                    font-size:15px;
                    font-weight:700;
                    margin-bottom:12px;
                ">
                    📊 Spatial Data Coverage
                </div>
                """,
                unsafe_allow_html=True
            )
            create_spatial_coverage_card(
                title="Earthquake",
                icon="🟠",
                total=coverage["earthquake"]["total"],
                mapped=coverage["earthquake"]["mapped"],
                accent_color="#F59E0B"
            )
            create_spatial_coverage_card(
                title="Flood",
                icon="🔵",
                total=coverage["flood"]["total"],
                mapped=coverage["flood"]["mapped"],
                accent_color="#38BDF8"
            )
            create_spatial_coverage_card(
                title="Cyclone",
                icon="🟢",
                total=coverage["cyclone"]["total"],
                mapped=coverage["cyclone"]["mapped"],
                accent_color="#22C55E"
            )
            st.markdown(
                """
                <div style="
                    background:#111827;
                    border:1px solid #1E40AF;
                    border-radius:12px;
                    padding:15px;
                    margin-top:15px;
                    color:#CBD5E1;
                    font-size:14px;
                ">
                <div style="
                    color:#38BDF8;
                    font-size:16px;
                    font-weight:700;
                    margin-bottom:8px;
                ">
                ⓘ Map Interpretation
                </div>
                <div>
                The map displays only disaster records
                with available geographic coordinates.
                </div>
                </div>
                """,
                unsafe_allow_html=True
            )
        # ============================================================
        # RIGHT — SPATIAL MAP
        # ============================================================

        with map_col:
            st.plotly_chart(
                spatial_fig,
                use_container_width=True,
                width=700,
                config={
                    "displayModeBar": False,
                    "scrollZoom": False,
                    "doubleClick": False,
                    "staticPlot": False
                }
            )
    # ========================================================
    # 8. INTRODUCTION
    # ========================================================

    st.markdown(

        f"""
        <h4 style="
        text-align:center;
        color:#CBD5E1;
        ">
        Here's the complete disaster analysis
        for {selected_state}
        </h4>
        """,
        unsafe_allow_html=True
    )

# ========================================================
# 11. PAGE SWITCH BUTTONS
# ========================================================

    left, btn1, btn2, right = st.columns(
        [3,1,1,3]
    )
    with btn1:
        if st.button(
            "← Analysis",
            width="stretch",
            key="analysis_button"
        ):
            st.session_state["state_view"] = "analysis"
            st.rerun()
    with btn2:
        if st.button(
            "Graphs →",
            width="stretch",
            key="graph_button"
        ):
            st.session_state["state_view"] = "graphs"
            st.rerun()

    # separation line after navigation
    st.divider()

    # ========================================================
    # 12. ANALYTICAL VIEW
    # ========================================================

    if st.session_state["state_view"] == "analysis":

        # ====================================================
        # ML INTELLIGENCE
        # ====================================================

        st.markdown("### 🤖 ML Intelligence")
        if ml["available"]:
            ml1, ml2, ml3, ml4 = st.columns(4)
            with ml1:
                create_overview_card(
                    title="Anomaly Candidates",
                    value=f"{ml.get('closest_event_km', 0)} km",
                    subtitle="Detected by ML model",
                    icon="🤖",
                    accent_color="#8B5CF6"
                )
            with ml2:
                create_overview_card(
                    title="Closest Event",
                    value=f"{ml['closest_event_km']} km",
                    subtitle="Nearest recorded event",
                    icon="📍",
                    accent_color="#38BDF8"
                )
            with ml3:
                create_overview_card(
                    title="Strongest Anomaly",
                    value=ml.get("strongest_anomaly", 0),
                    subtitle="Highest anomaly score",
                    icon="⚡",
                    accent_color="#F59E0B"
                )
            with ml4:
                create_overview_card(
                    title="Highest Magnitude",
                    value=ml.get("highest_magnitude", 0),
                    subtitle="Detected earthquake magnitude",
                    icon="📈",
                    accent_color="#EF4444"
                )
        else:
            st.info(
                "No ML prediction available for this state."
            )

        st.divider()

        # ====================================================
        # DISASTER OVERVIEW
        # ====================================================

        st.markdown("### 📊 Disaster Overview")
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            create_overview_card(
                title="Total Events",
                value=summary["total_events"],
                subtitle="All recorded disasters",
                icon="🛡️",
                accent_color="#8B5CF6"
            )
        with c2:
            create_overview_card(
                title="Earthquakes",
                value=summary["earthquake_events"],
                subtitle="Most frequent",
                icon="🌍",
                accent_color="#F59E0B"
            )
        with c3:
            create_overview_card(
                title="Floods",
                value=summary["flood_events"],
                subtitle="Recorded flood events",
                icon="🌊",
                accent_color="#38BDF8"
            )
        with c4:
            create_overview_card(
                title="Cyclones",
                value=summary["cyclone_events"],
                subtitle="Recorded cyclone events",
                icon="🌀",
                accent_color="#22C55E"
            )

        st.markdown(
            f"""
            <div style="
                color: #94A3B8;
                font-size: 13px;
                margin-top: 15px;
                margin-bottom: 10px;
            ">
                {intelligence["analysis_text"]}
            </div>
            """,
            unsafe_allow_html=True
        )

        st.divider()

        # ====================================================
        # ANALYTICAL INTELLIGENCE
        # ====================================================

        st.markdown("### 📄 Analytical Intelligence")

        # ====================================================
        # THREE DISASTER CARDS
        # ====================================================

        eq_col, flood_col, cyclone_col = st.columns(3)

        # -------------------------------
        # EARTHQUAKE
        # -------------------------------

        with eq_col:
            if earthquake["events"] > 0:
                create_intelligence_card(
                    title="Earthquake Intelligence",
                    icon="🌍",
                    accent_color="#F59E0B",
                    metrics=[
                        (
                            "Average Magnitude",
                            earthquake["average_magnitude"]
                        ),
                        (
                            "Maximum Magnitude",
                            earthquake["maximum_magnitude"]
                        ),
                        (
                            "Total Events",
                            earthquake.get("events", 0)
                        )
                    ],
                    footer_text=(
                        f"Maximum magnitude: {earthquake['maximum_magnitude']} "
                        f"| Total recorded events: {earthquake['events']}"
                    )
                )
            else:
                st.info(
                    "No earthquake records available."
                )

        # -------------------------------
        # FLOOD
        # -------------------------------

        with flood_col:
            if flood["events"] > 0:
                create_intelligence_card(
                    title="Flood Intelligence",
                    icon="🌊",
                    accent_color="#38BDF8",
                    metrics=[
                        (
                            "Average Duration",
                            f"{flood['average_duration']} days"
                        ),
                        (
                            "Fatalities",
                            flood.get("total_fatalities", flood.get("fatalities", 0))
                        ),
                        (
                            "Total Events",
                            flood.get("events", 0)
                        )
                    ],
                    footer_text=(
                        f"Total impact: {flood['total_fatalities']} fatalities "
                        f"| Average duration: {flood['average_duration']} days"
                    )
                )
            else:
                st.info(
                    "No flood records available."
                )

        # -------------------------------
        # CYCLONE
        # -------------------------------

        with cyclone_col:
            if cyclone["events"] > 0:
                create_intelligence_card(
                    title="Cyclone Intelligence",
                    icon="🌀",
                    accent_color="#22C55E",
                    metrics=[
                        (
                            "Maximum Wind Speed",
                            f"{cyclone.get('maximum_wind_speed', 0)} knots"
                        ),
                        (
                            "Minimum Pressure",
                            f"{cyclone.get('minimum_pressure', 0)} mb"
                        ),
                        (
                            "Total Events",
                            cyclone.get("events", 0)
                        )
                    ],
                    footer_text=(
                        f"Peak wind speed: {cyclone['maximum_wind_speed']} knots "
                        f"| Minimum pressure: {cyclone['minimum_pressure']} mb"
                    )
                )
            else:
                st.info(
                    "No cyclone records available."
                )

    # ========================================================
    # 13. GRAPH VIEW
    # ========================================================

    elif st.session_state["state_view"]=="graphs":
        show_graph_dashboard(
            data=data,
            selected_state=selected_state
        )

    # ========================================================
    # 14. BACK HOME
    # ========================================================

    st.markdown(
        "<br><br>",
        unsafe_allow_html=True
    )

    _,center,_ = st.columns(
        [2,1.5,2]
    )

    with center:
        if st.button(
            "← Back to India Map",
            width="stretch",
            key="back_home"
        ):
            st.session_state["page"] = "home"
            st.session_state["state_view"] = "analysis"
            st.rerun()