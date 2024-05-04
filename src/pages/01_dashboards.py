import streamlit as st
import pandas as pd
from modules import chart_functions as cf
from modules import table_functions as tf

# Data Loading (adjust paths if needed)
df_cats = pd.read_csv("data/cleaned/cats_consultations.csv")
df_dogs = pd.read_csv("data/cleaned/dogs_consultations.csv")
df_other = pd.read_csv("data/cleaned/other_species_consultations.csv")

st.set_page_config(layout="wide")

# Inject custom CSS to improve tab readability
st.markdown(
    """
<style>
.css-1lcbmhc {
    padding: 1rem 1rem;  /* Adjust padding around the tab texts */
}
.css-1lcbmhc e1tzin5v3 {
    font-size: 16px;  /* Increase the font size */
    font-weight: bold;  /* Make the font bold */
}
.stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
    font-size:2rem;
}
</style>
""",
    unsafe_allow_html=True,
)

# Header
st.title("Veterinary Management Dashboard")

# Main Tabs for Species
cats_tab, dogs_tab, other_tab = st.tabs(["Cats", "Dogs", "Other Species"])

with cats_tab:
    row1_col1, row1_col2 = st.columns(2)

    with row1_col1:
        st.title("Consultation Counts")
        cats_table = tf.create_mpc_counts_table(df_cats)
        st.table(cats_table)

    with row1_col2:
        st.title("Consultation Distribution")
        cat_chart = cf.create_mpc_bar_chart(df_cats, "Cats: Consultation Types")
        st.plotly_chart(cat_chart, use_container_width=True)

    row2_col1, row2_col2 = st.columns(2)

    with row2_col1:
        st.title("Consultation Frequency Over Time")
        time_series_fig = cf.plot_consultation_frequency(df_cats)
        st.plotly_chart(time_series_fig, use_container_width=True)

    with row2_col2:
        st.title("Consultation Heatmap")
        heatmap_fig_cats = cf.plot_consultation_heatmap(df_cats)
        st.plotly_chart(heatmap_fig_cats, use_container_width=True)

with dogs_tab:
    row1_col1, row1_col2 = st.columns(2)

    with row1_col1:
        st.title("Consultation Counts")
        dogs_table = tf.create_mpc_counts_table(df_dogs)
        st.table(dogs_table)

    with row1_col2:
        st.title("Consultation Distribution")
        dog_chart = cf.create_mpc_bar_chart(df_dogs, "Dogs: Consultation Types")
        st.plotly_chart(dog_chart, use_container_width=True)

    row2_col1, row2_col2 = st.columns(2)

    with row2_col1:
        st.title("Consultation Frequency Over Time")
        time_series_fig = cf.plot_consultation_frequency(df_dogs)
        st.plotly_chart(time_series_fig, use_container_width=True)

    with row2_col2:
        st.title("Consultation Heatmap")
        heatmap_fig_dogs = cf.plot_consultation_heatmap(df_dogs)
        st.plotly_chart(heatmap_fig_dogs, use_container_width=True)

with other_tab:
    row1_col1, row1_col2 = st.columns(2)

    with row1_col1:
        st.title("Consultation Counts")
        other_table = tf.create_mpc_counts_table(df_other)
        st.table(other_table)

    with row1_col2:
        st.title("Consultation Distribution")
        other_chart = cf.create_mpc_bar_chart(
            df_other, "Other Species: Consultation Types"
        )
        st.plotly_chart(other_chart, use_container_width=True)

    row2_col1, row2_col2 = st.columns(2)

    with row2_col1:
        st.title("Consultation Frequency Over Time")
        time_series_fig = cf.plot_consultation_frequency(df_other)
        st.plotly_chart(time_series_fig, use_container_width=True)

    with row2_col2:
        st.title("Consultation Heatmap")
        heatmap_fig_other = cf.plot_consultation_heatmap(df_other)
        st.plotly_chart(heatmap_fig_other, use_container_width=True)
