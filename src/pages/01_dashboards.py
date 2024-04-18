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
    data_tab, chart_tab = st.tabs(["Data", "Graph"])

    with data_tab:
        st.title("Cats: Consultation Counts")
        cats_table = tf.create_mpc_counts_table(df_cats)
        st.table(cats_table)

    with chart_tab:
        st.header("Cats Consultations: Distribution of Consultations")
        cat_chart = cf.create_mpc_bar_chart(df_cats, "Cats: Consultation Types")
        st.plotly_chart(cat_chart, use_container_width=True)

with dogs_tab:
    data_tab, chart_tab = st.tabs(["Data", "Graph"])

    with data_tab:
        st.header("Dogs: Consultation Counts")
        dogs_table = tf.create_mpc_counts_table(df_dogs)
        st.table(dogs_table)

    with chart_tab:
        st.header("Dogs Consultations: Distribution of Consultations")
        dog_chart = cf.create_mpc_bar_chart(df_dogs, "Dogs: Consultation Types")
        st.plotly_chart(dog_chart, use_container_width=True)

with other_tab:
    data_tab, chart_tab = st.tabs(["Data", "Graph"])

    with data_tab:
        st.header("Other Species: Consultation Counts")
        other_table = tf.create_mpc_counts_table(df_other)
        st.table(other_table)

    with chart_tab:
        st.header("Other Species Consultations: Distribution of Consultations")
        other_chart = cf.create_mpc_bar_chart(
            df_other, "Other Species: Consultation Types"
        )
        st.plotly_chart(other_chart, use_container_width=True)
