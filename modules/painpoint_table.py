import streamlit as st
from datetime import datetime

PAIN_POINTS = [
    "a_scrap",
    "b_rwk",
    "c_fpy",
    "d_ppm",
    "e_8D",
    "f_safety",
    "g_other"
]

def create_empty_rows():

    return [
        {
            "Date": datetime.today().strftime("%Y-%m-%d"),
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

def render_table(df):

    edited_df = st.data_editor(
        df,
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

    return edited_df