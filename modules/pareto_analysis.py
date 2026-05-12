import streamlit as st
import plotly.express as px

def render_pareto(df):

    st.subheader("Pareto Analysis")

    if df.empty:
        st.warning("No data available.")
        return

    pareto = (
        df["6 - Pain Point"]
        .value_counts()
        .reset_index()
    )

    pareto.columns = ["Pain Point", "Count"]

    fig = px.bar(
        pareto,
        x="Pain Point",
        y="Count",
        title="Pain Point Distribution"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )