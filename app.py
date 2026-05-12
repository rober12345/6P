import streamlit as st
import pandas as pd
import plotly.express as px
import os
from datetime import datetime

# =========================================================
# CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="6P",
    layout="wide"
)

DATA_FILE = "data/observations.csv"

PAIN_POINTS = [
    "a_scrap",
    "b_rwk",
    "c_fpy",
    "d_ppm",
    "e_8D",
    "f_safety",
    "g_other"
]

COLUMNS = [
    "Date",
    "1 - Place",
    "2 - Process",
    "3 - Players",
    "4 - Principle : W.I., Visual Aid, Measure Tech.",
    "5 - Procedure Used",
    "6 - Pain Point",
    "7 - Comment"
]

# =========================================================
# CREATE DATA DIRECTORY
# =========================================================

os.makedirs("data", exist_ok=True)

# =========================================================
# LOAD MASTER DATA
# =========================================================

if os.path.exists(DATA_FILE):

    try:
        master_df = pd.read_csv(DATA_FILE)

    except pd.errors.EmptyDataError:
        master_df = pd.DataFrame(columns=COLUMNS)

else:
    master_df = pd.DataFrame(columns=COLUMNS)

# =========================================================
# FIX DATE COLUMN TYPE
# =========================================================

if "Date" in master_df.columns:

    master_df["Date"] = pd.to_datetime(
        master_df["Date"],
        errors="coerce"
    )

# =========================================================
# TITLE
# =========================================================

st.title("6P")
st.subheader("Process Pain Point Platform")

st.markdown("""
Capture operational pain points, process variation,
waste, and execution gaps across manufacturing operations.
""")

# =========================================================
# INITIALIZE SESSION DATA
# =========================================================

if "session_df" not in st.session_state:

    empty_rows = pd.DataFrame(
        [
            {
                "Date": datetime.today(),
                "1 - Place": "",
                "2 - Process": "",
                "3 - Players": "",
                "4 - Principle : W.I., Visual Aid, Measure Tech.": "",
                "5 - Procedure Used": "",
                "6 - Pain Point": "a_scrap",
                "7 - Comment": ""
            }
            for _ in range(100)
        ]
    )

    st.session_state.session_df = empty_rows

# =========================================================
# DATA EDITOR TABLE
# =========================================================

edited_df = st.data_editor(
    st.session_state.session_df,
    num_rows="dynamic",
    use_container_width=True,
    height=700,

    column_config={

        "Date": st.column_config.DateColumn(
            "Date"
        ),

        "1 - Place": st.column_config.TextColumn(
            "1 - Place",
            width="medium"
        ),

        "2 - Process": st.column_config.TextColumn(
            "2 - Process",
            width="large"
        ),

        "3 - Players": st.column_config.TextColumn(
            "3 - Players",
            width="large"
        ),

        "4 - Principle : W.I., Visual Aid, Measure Tech.": st.column_config.TextColumn(
            "4 - Principle : W.I., Visual Aid, Measure Tech.",
            width="large"
        ),

        "5 - Procedure Used": st.column_config.TextColumn(
            "5 - Procedure Used",
            width="large"
        ),

        "6 - Pain Point": st.column_config.SelectboxColumn(
            "6 - Pain Point",
            options=PAIN_POINTS
        ),

        "7 - Comment": st.column_config.TextColumn(
            "7 - Comment",
            width="large"
        )
    }
)

# SAVE SESSION
st.session_state.session_df = edited_df

# =========================================================
# BUTTONS
# =========================================================

col1, col2, col3, col4 = st.columns(4)

# =========================================================
# SAVE BUTTON
# =========================================================

with col1:

    if st.button("💾 SAVE"):

        combined_df = pd.concat(
            [master_df, edited_df],
            ignore_index=True
        )

        combined_df = combined_df.drop_duplicates()

        combined_df.to_csv(DATA_FILE, index=False)

        st.success("Data saved successfully.")

# =========================================================
# CHARTS BUTTON
# =========================================================

with col2:

    generate_charts = st.button("📊 CHARTS")

# =========================================================
# CLEAN BUTTON
# =========================================================

with col3:

    if st.button("🧹 CLEAN / NEW FILE"):

        clean_df = pd.DataFrame(columns=COLUMNS)

        clean_df.to_csv(DATA_FILE, index=False)

        st.session_state.session_df = pd.DataFrame(
            [
                {
                    "Date": datetime.today(),
                    "1 - Place": "",
                    "2 - Process": "",
                    "3 - Players": "",
                    "4 - Principle : W.I., Visual Aid, Measure Tech.": "",
                    "5 - Procedure Used": "",
                    "6 - Pain Point": "a_scrap",
                    "7 - Comment": ""
                }
                for _ in range(100)
            ]
        )

        st.success("New file created.")

# =========================================================
# DOWNLOAD REPORT BUTTON
# =========================================================

with col4:

    if os.path.exists(DATA_FILE):

        with open(DATA_FILE, "rb") as file:

            st.download_button(
                label="📄 PRINT REPORT / DOWNLOAD CSV",
                data=file,
                file_name="6P_Report.csv",
                mime="text/csv"
            )

# =========================================================
# CHARTS SECTION
# =========================================================

if generate_charts:

    st.divider()

    st.header("Operational Analysis Dashboard")

    if os.path.exists(DATA_FILE):

        analysis_df = pd.read_csv(DATA_FILE)

        # Convert dates safely
        analysis_df["Date"] = pd.to_datetime(
            analysis_df["Date"],
            errors="coerce"
        )

        # =================================================
        # PARETO ANALYSIS
        # =================================================

        st.subheader("Pareto Analysis")

        pareto = (
            analysis_df["6 - Pain Point"]
            .value_counts()
            .reset_index()
        )

        pareto.columns = ["Pain Point", "Count"]

        fig_pareto = px.bar(
            pareto,
            x="Pain Point",
            y="Count",
            title="Pain Point Distribution"
        )

        st.plotly_chart(
            fig_pareto,
            use_container_width=True
        )

        # =================================================
        # STACK BAR CHART
        # =================================================

        st.subheader("Stack Bar Chart")

        stack_data = (
            analysis_df.groupby(
                ["1 - Place", "6 - Pain Point"]
            )
            .size()
            .reset_index(name="Count")
        )

        fig_stack = px.bar(
            stack_data,
            x="1 - Place",
            y="Count",
            color="6 - Pain Point",
            title="Pain Points by Place",
            barmode="stack"
        )

        st.plotly_chart(
            fig_stack,
            use_container_width=True
        )

        # =================================================
        # TREND ANALYSIS
        # =================================================

        st.subheader("Trend Analysis")

        trend_data = (
            analysis_df.groupby(
                ["Date", "6 - Pain Point"]
            )
            .size()
            .reset_index(name="Count")
        )

        fig_trend = px.line(
            trend_data,
            x="Date",
            y="Count",
            color="6 - Pain Point",
            markers=True,
            title="Pain Point Trends"
        )

        st.plotly_chart(
            fig_trend,
            use_container_width=True
        )

        # =================================================
        # WORST LINE
        # =================================================

        st.subheader("Worst Line / Area")

        worst_line = (
            analysis_df["1 - Place"]
            .value_counts()
            .reset_index()
        )

        worst_line.columns = ["Place", "Count"]

        st.dataframe(worst_line.head(10))

        # =================================================
        # TOP OFFENDERS
        # =================================================

        st.subheader("Top Offenders")

        offenders = (
            analysis_df["2 - Process"]
            .value_counts()
            .reset_index()
        )

        offenders.columns = ["Process", "Count"]

        st.dataframe(offenders.head(10))

        # =================================================
        # AI ANALYSIS
        # =================================================

        st.subheader("A.I. Operational Insight")

        if not pareto.empty:

            top_pain = pareto.iloc[0]["Pain Point"]

            st.info(f"""
            Most dominant operational pain point detected:
            {top_pain}

            Recommended focus areas:
            - Verify process execution consistency
            - Review operator alignment
            - Validate work instruction clarity
            - Investigate recurring operational losses
            - Prioritize high-frequency pain points
            """)

    else:

        st.warning("No operational data available.")