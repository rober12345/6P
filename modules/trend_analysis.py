import streamlit as st
import plotly.express as px

def render_trends(df):

    st.subheader("Trend Analysis")

    if df.empty:
        st.warning("No data available.")
        return

    trend_data = (
        df.groupby(
            ["Date", "6 - Pain Point"]
        )
        .size()
        .reset_index(name="Count")
    )

    fig = px.line(
        trend_data,
        x="Date",
        y="Count",
        color="6 - Pain Point",
        markers=True,
        title="Pain Point Trends"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )